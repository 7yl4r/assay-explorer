import os
import shutil
import zipfile
import hashlib

import arrow
from numpy.random import random
import pandas as pd

from toolz import partition, partitionby, thread_last
from utils import (snd, exists_at_path, add_dict_to_dataframe,
                   add_col, maprows, format_num, from_file, 
                   parse_label_group, string_only_contains, generate_sid)

from raw import get_plate_data
from conf import PATH

from IPython.display import clear_output

# String -> String
def rename_column(col):
    """ Rename column col to remove whitespace, backslashes, prefixes,
        and suffixes (esp. large parenthetic suffix). """
    if col.startswith('Cell:'):
        return col.split('(')[0].lstrip("Cell:").rstrip('/').strip(' ')
    else:
        return col.split('(')[0].rstrip('/').strip(' ')

def get_normalization_config():
    import config.columns as conf
    return conf.v2

class Uploader():
    def __init__(self, plate_import_config, gather_plate_data):
        self.plate_import_config = plate_import_config
        self.gather_plate_data = gather_plate_data

        self.zipfile_path = os.path.join(PATH, 'raw', 'data.zip') #'/notebooks/add-data/data.zip'
        self.extract_path = os.path.join(PATH, 'data') #'/notebooks/tmp/extracted-data/'
        self.temp_save_path = os.path.join(PATH, 'data') # '/notebooks/tmp/imported-data/'
        self.db_path = os.path.join(PATH, 'db', 'db.csv') #'/notebooks/moldev-data/db/db.csv'

        self.folders = ['raw', 'data', 'db', 'tmp']

        self.make_temp_files()

    def make_temp_files(self):
        # Extract files into temporary working directory
        for folder in self.folders:
            folder_path = os.path.join(PATH, folder)
            if not os.path.exists(folder_path):
                print('Creating "%s".' % folder_path)
                os.mkdir(folder_path)

    def check(self, eventObj=None):
        """ Extract zip and prepare for import into main dataset.
            If data can be imported, then create a new csv in a temp directory.
            Returns string of any warning or errors in this process. """

        if os.path.exists(self.extract_path):
            shutil.rmtree(self.extract_path) # clear out existing files

        with zipfile.ZipFile(self.zipfile_path, "r") as z:
            z.extractall(self.extract_path)

        # Check files for correctness
        exists = exists_at_path(self.extract_path) # curried function
        nonempty = lambda entity: len(os.listdir(os.path.join(self.extract_path,entity))) > 0
        initial_tests = \
            [exists('metadata.csv'), "File missing: metadata.csv",
             exists('Plates/'), "Folder missing: Plates",
             exists('Layouts/'), "Folder missing: Layouts",
             nonempty('Plates/'), "It looks like you haven't got any plates in your Plates folder.",
             nonempty('Layouts/'), "It looks like you haven't got any layouts in your Layouts folder."]

        err = generate_message(initial_tests)
        clear_output()

        if err != '':
            print("### ERROR ###")
            print(err)
        else:
            # Read metadata
            metadata_path = os.path.join(self.extract_path,'metadata.csv')
            metadata = pd.read_csv(metadata_path).dropna(how='all',axis=0).dropna(how='all',axis=1)

            # Get all data
            all_data = thread_last(
                metadata,
                (maprows, self.gather_plate_data),
                pd.concat)

            all_data['Upload Timestamp'] = arrow.now().timestamp

            # Check for duplicated cells
            try:
                db_dataframe = pd.read_csv(self.db_path)
                duplicate_timestamps = find_uploads_with_duplicate_cells(db_dataframe,all_data)
                if len(duplicate_timestamps) > 0:
                    for ts in duplicate_timestamps:
                        time = arrow.get(ts).to('US/Pacific').format('MMMM DD, YYYY, h:mm a')
                        time_ago = arrow.get(ts).humanize()
                        print("It looks like you already uploaded some of this data on {} ({})".format(time,time_ago))
                    print("If you'd like to overwrite this data, you'll need to remove the data for these dates first.")
                else:
                    print("Ready to upload {} cells!".format(format_num(len(all_data))))
            except Exception as e:
                print(e)
            # Save data to temporary location
            if os.path.exists(self.temp_save_path):
                shutil.rmtree(self.temp_save_path)
            os.makedirs(self.temp_save_path)
            all_data.to_csv(os.path.join(self.temp_save_path,'new_data.csv'),
                            index=False)
        return

    def add_new_data(self, eventObj=None):
        """ Add new data (from temp file) to db file.
            Fails if there are duplicate cells."""
        try:
            db_data = [pd.read_csv(self.db_path)]
        except Exception as e:
            print(e)
            db_data = []
        new_data = pd.read_csv(os.path.join(self.temp_save_path,'new_data.csv'))
        all_data = pd.concat(db_data+[new_data])
        contains_duplicated_cells = all_data.duplicated('Cell SID').any()

        clear_output()

        if contains_duplicated_cells:
            print("It looks like the data's already been added.")
        else:
            all_data.to_csv(self.db_path,index = False)
            print("Just saved data!")

def get_plate_import_config(normalization_config):
    return dict(
        delimiter = '\t',
        skiprows = 4,
        dropcols = ['Laser focus score',
                    '\.[0-9]*\Z'],
        colrename = rename_column,
        normcols = normalization_config
    )

# String -> String
def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

# Series -> String
def generate_cell_sid(cell_data):
    """ Given Series containing cell information,
        generate hash string to use as string id. """

    columns_to_hash = ['Plate ID', 'Well Name', 'Site ID', 'Cell ID']

    return thread_last(
        cell_data[columns_to_hash].tolist(),
        (map,str),
        (str.join,' '),
        computeMD5hash,
        lambda string: 'CELL_' + string)

# DataFrame -> DataFrame -> [Timestamp]
def find_uploads_with_duplicate_cells(db_dataframe,new_dataframe):
    """ Given a primary dataframe acting as central information store,
        and a new dataframe containing data to be incorporated into the primary store,
        check if there are any duplicated cells, and when they were added.

        Returns list of timestamps for days when duplicate cells were uploaded.
        (Returns empty list if there are no duplicate cells.) """

    new_cell_sids = new_dataframe['Cell SID']
    duplicate_cells = db_dataframe['Cell SID'].isin(new_cell_sids)
    return db_dataframe[duplicate_cells]['Upload Timestamp'].unique()

def generate_message(tests):
    """ Print out statements for all tests that fail. """
    return thread_last(
        tests,
        (partition,2),
        (filter,lambda pair: pair[0] == False),
        (map,snd),
        (str.join,'\n'))
