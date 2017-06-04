#!/usr/bin/env python

"""
"uploads" new data from file ./raw/data.zip

By "upload" here I mean that it preps the data from ./raw/ into ./data/
    (and maybe also ./db/?).
"""

# TODO: remove unused functions from library / combine/separate libraries into better modules
# TODO: put zip file somewhere safe after its been used.
# TODO: create regular backups to google docs or S3
# TODO: profile code to reduce upload times (strongly suspect df.apply() statements are bad. As in SID creation)
# TODO: add plate ID - one for each row in the provided metadata files. Should just be a randomly generated uuid.
from AssayExplorer.upload_data import (rename_column, get_normalization_config,
    get_plate_import_config, Uploader, computeMD5hash, generate_cell_sid,
    find_uploads_with_duplicate_cells, generate_message
)
from utils import get_layout_data

SECTION_DIV = "\n===========================================================\n"

plate_import_config = get_plate_import_config(get_normalization_config())

from toolz import thread_last, thread_first
import os
from raw import get_plate_data
from utils import add_dict_to_dataframe, format_timestamp
from collections import OrderedDict

# Series -> DataFrame
def gather_plate_data(plate_metadata):
    """ Given Series containing filepaths for plate and layout,
        import these files, join them, and add the series itself
        to create a master table for all the info about the plate. """

    # String -> String -> String
    def get_path(directory, column):
        """ Return path with first folder at given directory,
            and file at given column of metadata.csv file.

            (i.e. go to folder X and get file found in column Y of metadata file.)"""

        return os.path.join(
            uploader.extract_path,
            directory,
            plate_metadata[column])

    plate_data = thread_last(
        ['Plates','Plate File'],
        (apply, get_path),
        lambda path: get_plate_data(path, plate_import_config)
    )

    # Add string ID for use as primary key
    plate_data['Cell SID'] = plate_data.apply(generate_cell_sid,
                                              axis = 1)

#     plate_data['Plate SID'] = "Plate_{}".format(generate_sid())
    layout_data = thread_last(
        ['Layouts','Layout File'],
        (apply, get_path),
        lambda path: get_layout_data(path))

    # Series -> String
    def concatStrings(series):
        """ Concatenate values in all but first column. """
        return ' '.join([str(x) for x in series.values[1:]])

    layout_data['Condition'] = layout_data.apply(concatStrings, axis = 1)

    return thread_first(
        pd.merge(plate_data,layout_data,on = 'Well Name'),
        (add_dict_to_dataframe,dict(plate_metadata)))

import pandas as pd


def delete_handler(timestamp, db_data, uploader):
    """ Remove data uploaded at selected timestamp. """
    trimmed_data = db_data[db_data['Upload Timestamp'] != timestamp]
    trimmed_data.to_csv(uploader.db_path,index=False)
    print("Just deleted data.")


# def split_on_newlines(string):
#     """ Given a string which may contain \r, \n, or both,
#         split on newlines so neither character is present in output. """

#     r = '\r' in string
#     n = '\n' in string

#     if r and n:
#         return string.replace('\r','').split('\n')
#     elif r:
#         return string.split('\r')
#     else:
#         return string.split('\n')

# # String -> Boolean
# def string_is_empty(string):
#     """ Return True if string is empty. """
#     return string == ''

if __name__ == "__main__":
    uploader = Uploader(plate_import_config, gather_plate_data)

    raw_input("Ready to check data in ./raw/data.zip\n press enter to continue...")
    print("This step takes around 3 minutes.")
    uploader.check()

    print (SECTION_DIV)

    print("All files present & none of the data has already been uploaded.")
    up_choice = raw_input("save data? [y/N]").lower()
    if up_choice in ['yes', 'y']:
        uploader.add_new_data()

    print (SECTION_DIV)

    print("If you've made any mistake, and need to delete something you've "
        "uploaded, this is the place to do it.")

    db_data = pd.read_csv(uploader.db_path)
    timestamps = db_data['Upload Timestamp'].unique()

    delete_options = thread_last(
        timestamps,
        list,
        lambda x: sorted(x,reverse=True),
        (map,lambda x: (x,x)),
        (map,lambda x: (format_timestamp(x[0]),x[1])),
        OrderedDict
    )

    print("options: ", delete_options)
    print("index\ttimestamp")
    for i, option in enumerate(delete_options):
        print(str(i) + ':\t' + option)
    del_choice = raw_input("delete? [y/N]")
    if del_choice in ['yes', 'y']:
        index = raw_input("enter index to delete: ")
        delete_handler(int(index), db_data, uploader)

    print (SECTION_DIV)

    # testpath = '/notebooks/tmp/extracted-data/Plates/APB HS JS (60X) 08.06.2015 siRNA VE821.txt'
    # test = get_plate_data(testpath,uploader.plate_import_config)

    # layouttest = get_layout_data('/notebooks/tmp/extracted-data/Layouts/layout.csv')

    # test['Well Name'].unique()
    # test2 = pd.read_csv('/notebooks/tmp/imported-data/new_data.csv')

    # String -> [String]


    # l2 = thread_last(
    #      '/notebooks/tmp/extracted-data/Layouts/layout.csv',
    #      from_file,
    #      lambda string: string.replace('\r','').split('\n'),
    #      (map,lambda line: line.rstrip(',')),
    #      (partitionby, lambda line: string_only_contains(line,',')),
    #      (filter,lambda group: not string_only_contains(group[0],',')),
    #      (map,lambda strings: str.join('\n',strings)),
    #      (map,parse_label_group),
    #      (reduce,lambda left,right: pd.merge(left,right,on='Well Name')))

    # l2 = thread_last(
    #     os.path.join(PATH, 'data', 'Layouts', 'layout.csv'),
    #     from_file,
    #     split_on_newlines,
    #     (map,lambda line: line.rstrip(',')),
    #     (partitionby, string_is_empty),
    #     (filter,lambda group: not string_is_empty(group[0])),
    #     (map,lambda strings: str.join('\n',strings)),
    #     (map,parse_label_group),
    #     (reduce,lambda left,right: pd.merge(left,right,on='Well Name')))

    # for x in l2['Units (concentration)'].unique():
    #     print x

    # list(l2)
