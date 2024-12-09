# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 15:27:03 2024

@author: lcornacchione
"""

import pandas as pd
import numpy as np 
import matplotlib.pylab as plt 
import seaborn as sns 

data_dir = '../../data/round3_primer_screen/'
result_dir = '../../results/round3_primer_screen/'

data = pd.read_excel(data_dir+'SAE_707_primer_screen_round3_run1_20241031_144244_Results_20241108_103930.xlsx',header=25)
#make all undetermined Cq values zero and cast as float type
data.loc[data['Cq']=='UNDETERMINED','Cq'] = 41
data['Cq'] = data['Cq'].astype('float')
data['Target'] = data['Target'].astype('str')

primer_map = pd.read_excel(data_dir+'primer_dna_idot.xlsx')
primer_map.rename(mapper={'target_well':'Well Position'},inplace=True,axis=1)
data = data.merge(primer_map,on='Well Position')

#%%    
data.sort_values('Target',inplace=True)
colors = sns.color_palette("Set2")
for sample,subdata in data.groupby('Sample'):
    fig,ax = plt.subplots()
    fig.set_size_inches(8,5)
    sns.barplot(data=subdata,x='primer',y='Cq',color='gray')
    plt.axhline(y=41,color='r',linestyle='--',label='Undetermined (Cq = 41)')
    plt.suptitle(sample)
    plt.xticks(rotation=90)
    fig.tight_layout()
    plt.savefig(result_dir+sample+'_Cq_barplot.png',dpi=300)
    