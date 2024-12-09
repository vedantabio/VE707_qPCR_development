# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 15:27:03 2024

@author: lcornacchione
"""

import pandas as pd
import numpy as np 
import matplotlib.pylab as plt 
import seaborn as sns 

data_dir = '../../data/10L_DS_identity_powerfecalpro/'
result_dir = '../../results/10L_DS_identity_powerfecalpro/'

data = pd.read_excel('../../data/10L_DS_identity_powerfecalpro/SAE_VE707_qPCR_10L_identity_10_24_24_20241024_151911_Results_20241126_142501.xlsx',header=25)
#make all undetermined Cq values zero and cast as float type
data.loc[data['Cq']=='UNDETERMINED','Cq'] = 41
data['Cq'] = data['Cq'].astype('float')
data['Target'] = data['Target'].astype('str')

unknowns = data.loc[data['Sample'].str.contains('batchrun'),:]
for index, value in unknowns['Target'].items():
    if len(value) == 1:
        unknowns.loc[index,'Target'] = '0'+value 
    
unknowns.sort_values('Target',inplace=True)
colors = sns.color_palette("Set2")
for sample,subdata in unknowns.groupby('Sample'):
    plt.subplots()
    sns.barplot(data=subdata,x='Target',y='Cq',palette=colors)
    plt.suptitle(sample)
    plt.savefig(result_dir+sample+'_Cq_barplot.png',dpi=300)
    