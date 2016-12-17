v1 = [
    [
        'Normalized_ColocSpot_area_sum (coloc)',
        ['ColocSpots_area_sum'],
        ['FITC-TxRed_coloc_area_sum']
    ],[
        'Normalized_ColocSpot_area_sum (all)',
        ['ColocSpots_area_sum'],
        ['FITC-TxRed_all_area_sum']
    ],[
        'Normalized coloc spots (by FITC & TxRed)',
        ['# of Coloc Spots'],
        ['# of FITC spots', '# of TxRed spots']
    ],[
        'Normalized coloc spots (by FITC)',
        ['# of Coloc Spots'],
        ['# of FITC spots']
    ],[
        'Normalized coloc spots (by TxRed)',
        ['# of Coloc Spots'],
        ['# of TxRed spots']
    ],[
        'Normalized coloc spots (by FITC in coloc)',
        ['# of Coloc Spots'],
        ['# of FITC in ColocSpots']
    ],[
        'Normalized coloc spots (by TxRed in coloc)',
        ['# of Coloc Spots'],
        ['# of TxRed in ColocSpots']
    ],[
        'Normalized coloc spots (by FITC-TxRed in coloc)',
        ['# of Coloc Spots'],
        ['# of FITC-TxRed in ColocSpots']
    ]
]

v2 = [
    [
        'Normalized_ColocSpot_area_sum (coloc)',
        ['TxRed Area_Sum'],
        ['FITC-TxRed-Coloc_Area_Sum'],  # ['Cell: FITC-TxRed-Coloc_Area_Sum (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)'],
    ],[
        'Normalized_ColocSpot_area_sum (all)',
        ['TxRed Area_Sum'],
        ['FITC-Cy5-Coloc_Area_Sum']  # ['Cell: FITC-Cy5-Coloc_Area_Sum (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)'],

        # ['Cell: FITCinCy5-TxRed-FITC-Coloc_Area_Sum (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)'],
        # ['Cell: FITCinFITC-Cy5-Coloc_Area_Sum (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)'],
        # ['Cell: FITCinFITC-TxRed-Coloc_Area_Sum (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)'],
        # ['Cell: FITC-NonColoc_Area_Sum (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)'],
        # ['Cell: TxRedinCy5-TxRed-FITC-Coloc_Area_Sum (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)']
    ]
]

v3 = v1 = [
    [
        'Normalized_ColocSpot_area_sum (coloc)',
        ['TxRed Area_Sum'],
        ['FITC-TxRed-Coloc_Area_Sum']
    ],[
        'Normalized_ColocSpot_area_sum (all)',
        ['TxRed Area_Sum'],
        ['FITC-Cy5-Coloc_Area_Sum']
    ],[
        'Normalized coloc spots (by FITC & TxRed)',
        ['# Cy5-TxRed-FITC coloc spots'],   # Cell: # Cy5-TxRed-FITC coloc spots (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)
        ['# Cy5-TxRed coloc spots', '# FITC-Cy5 coloc spots']
        # Cell: # Cy5-TxRed coloc spots (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)
        # Cell: # FITC-Cy5 coloc spots (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)
    ],[
        'Normalized coloc spots (by FITC)',
        ['# Cy5-TxRed-FITC coloc spots'],
        ['# Cy5-TxRed coloc spots']
    ],[
        'Normalized coloc spots (by TxRed)',
        ['# Cy5-TxRed-FITC coloc spots'],
        ['# FITC-TxRed coloc spots']  # Cell: # FITC-TxRed coloc spots (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)
    ],[
        'Normalized coloc spots (by FITC in coloc)',
        ['# Cy5-TxRed-FITC coloc spots'],
        ['# FITC-Cy5 coloc spots']  # # FITC-Cy5 coloc spots.Total (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)
    ],[
        'Normalized coloc spots (by TxRed in coloc)',
        ['# Cy5-TxRed-FITC coloc spots'],
        ['# TxRed spots noncoloc']    # TxRed spots noncoloc.Total (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)
    ],[
        'Normalized coloc spots (by FITC-TxRed in coloc)',
        ['# Cy5-TxRed-FITC coloc spots'],
        ['# TxRed spots in FITC-TxRed coloc']   # # TxRed spots in FITC-TxRed coloc.Total (ssC-TRF2-PML (60x) HS 2.5.16 SAHA)
    ]
]
