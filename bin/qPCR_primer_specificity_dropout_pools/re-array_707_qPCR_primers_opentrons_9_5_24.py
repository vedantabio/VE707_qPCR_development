# -*- coding: utf-8 -*-
"""

"""
metadata = {
'protocolName': 'VE707_qPCR_rearray_primers',
'author': 'Name <email@address.com>',
'Version': 'Version 2',
'Completed On': 'Jan 1, 2023',
'description': 'VE707_qPCR_rearray_primers',
'apiLevel': '2.10'
}
from opentrons import protocol_api;import csv ; import json;import re;import math
from collections import Counter
# import pandas as pd

# data_dir = '../../data/qPCR_primer_specificity_dropout_pools'

# #import the idot primer protocol which has information about which primers are in which wells and combine with the all_cq data frame
# primers_1 = pd.read_csv(data_dir+'/primerdispense_usethisone.csv',header=3,index_col=1, nrows=342)
# primers_2 = pd.read_csv(data_dir+'/primerdispense_usethisone.csv', header=349, index_col=1)

# primer_candidates = pd.read_excel(data_dir+'/consolidated_primer_candidates.xlsx',index_col=0)

# new_array = pd.DataFrame(data=None)
# for primer in primer_candidates.index:
#     if primer in primers_1['Liquid Name'].unique():
#         new_array.loc[primer,'source_well'] = primers_1.loc[primers_1['Liquid Name'] == primer,'Source Well'].unique()[0]
#         new_array.loc[primer,'plate_num'] = '1'
#     else:
#         new_array.loc[primer,'source_well'] = primers_2.loc[primers_2['Liquid Name'] == primer,'Source Well'].unique()[0]
#         new_array.loc[primer,'plate_num'] = '2'
        
# source_wells = []
# for primer in new_array.index:
#     well = new_array.loc[primer,'source_well']+'_'+str(new_array.loc[primer,'plate_num'])
#     source_wells.append(well)

# print(source_wells)
#%%

wells = ['A1_1', 'D1_1', 'G1_1', 'B2_1', 'E2_1', 'H2_1', 'C3_1', 'D3_1', 'A4_1', 'C4_1', 'D4_1', 'F4_1', 'B5_1', 'D5_1', 'H5_1', 'B6_1', 'F6_1', 'G6_1', 'C7_1', 'F7_1', 'H7_1', 'B1_2', 'C1_2', 'E1_2', 'A2_2', 'B2_2', 'D2_2', 'H2_2', 'C3_2', 'D3_2', 'F3_2', 'H3_2', 'C4_2', 'D4_2', 'H4_2', 'A5_2', 'E5_2', 'H5_2', 'B6_2', 'D6_2', 'G6_2', 'A7_2', 'C7_2']

def run(protocol: protocol_api.ProtocolContext):
	#Labware definitions 
    tiprack_300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '4')

   #Pipette
    pipette_300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack_300_1])
	#Plates
    #plate source is normalized 1ng/uL plate
    primer_source_1 = protocol.load_labware('biorad_96_wellplate_200ul_pcr','1')
    primer_source_2 = protocol.load_labware('biorad_96_wellplate_200ul_pcr','2')
    dest_plate = protocol.load_labware('biorad_96_wellplate_200uL_pcr','3')

    plates = [primer_source_1,primer_source_2]
    i = 0
    for well in wells:
        plate = int(well.split('_')[1])
        well = well.split('_')[0]
        pipette_300.transfer(50,plates[plate-1][well],dest_plate.wells()[i])
        i = i+1
        
        
#%%

        

    



