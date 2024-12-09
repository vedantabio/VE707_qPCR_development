# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import os 

#import results files which are the files with the Cq and other sample info like well, sample, target etc

data_dir = '../../data/qPCR_primer_specificity_dropout_pools'
result_dir = '../../results/qPCR_primer_specificity_dropout_pools/'

#get all results files in the data dir
result_files = []
for file in os.listdir(data_dir):
    if 'Results' in file:
        result_files.append(file)
#%%
#combine all data into one df and add annealing and plate number information contained in file name
all_cq = pd.DataFrame()
for file in result_files:
    annealing_temp = file.split('_')[0].split('-')[1]
    plate_num = file.split('_')[0].split('-')[0]
    plate_data = pd.read_excel(data_dir+'/'+file,header=25)
    plate_data['annealing_temp'] = annealing_temp
    plate_data['plate_number'] = plate_num
    all_cq = pd.concat([all_cq,plate_data])
all_cq.reset_index(inplace=True)
#make all undetermined Cq values zero and cast as float type
all_cq.loc[all_cq['Cq']=='UNDETERMINED','Cq'] = 41
all_cq = all_cq.astype({'Cq':'float'})
#%%
#import the idot primer protocol which has information about which primers are in which wells and combine with the all_cq data frame
primers_1 = pd.read_csv(data_dir+'/primerdispense_usethisone.csv',header=3,index_col=1, nrows=342)
primers_2 = pd.read_csv(data_dir+'/primerdispense_usethisone.csv', header=349, index_col=1)

for index in all_cq.index:
    plate_num = all_cq.loc[index,'plate_number']
    well = all_cq.loc[index,'Well Position']
    if plate_num == '1':
        primer = primers_1.loc[well,'Liquid Name']
        all_cq.loc[index,'primer_pair'] = primer
    if plate_num == '2':
        primer = primers_2.loc[well,'Liquid Name']
        all_cq.loc[index,'primer_pair'] = primer
        
#%%
#plot the target sample Cq for each primer pair 
all_cq.sort_values('Target',inplace=True)
target_data = all_cq.loc[all_cq['Sample']=='target',:]
fig,ax = plt.subplots()
fig.set_size_inches(13,4)
colors = sns.color_palette("Set2")
sns.barplot(data=target_data, x='primer_pair',y='Cq',ax=ax,color='gray')
sns.stripplot(data=target_data,x='primer_pair',y='Cq',ax=ax,alpha=0.5,size=3,hue='annealing_temp',palette=colors)
plt.axhline(y=41,color='r',linestyle='--',label='Undetermined (Cq = 41)')
plt.title('Target gDNA Cq')
plt.xticks(rotation=90,size=7)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',title='Annealing Temp (C)')
fig.tight_layout()
plt.savefig(result_dir+'all_primer_target_only.png',dpi=300)
#%%
#plot the dropout sample Cq for each primer pair
dropout_data = all_cq.loc[all_cq['Sample']=='drop_out',:]
fig,ax = plt.subplots()
fig.set_size_inches(13,4)
colors = sns.color_palette("Set2")
sns.barplot(data=dropout_data, x='primer_pair',y='Cq',ax=ax,color='gray')
sns.stripplot(data=dropout_data,x='primer_pair',y='Cq',ax=ax,alpha=0.75,size=3,hue='annealing_temp',palette=colors)
plt.axhline(y=41,color='r',linestyle='--',label='Undetermined (Cq = 41)')
plt.title('Dropout gDNA Pool Cq')
plt.xticks(rotation=90,size=7)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',title='Annealing Temp (C)')
fig.tight_layout()
plt.savefig(result_dir+'all_primer_dropout_only.png',dpi=300)
#%%
#plot each strain individually
for strain in all_cq['Target'].unique():
    strain_data = all_cq.loc[all_cq['Target']==strain,:]
    fig, ax = plt.subplots()
    colors = sns.color_palette("Set2")
    sns.barplot(data=strain_data, x='primer_pair', y='Cq',ax=ax, palette=colors ,hue='Sample')
    plt.axhline(y=41,color='r',linestyle='--',label='Undetermined (Cq = 41)')
    plt.title('VE707-'+str(strain))
    ax.legend(bbox_to_anchor=(1.05,1),loc='upper left')
    plt.xticks(rotation=90)
    fig.tight_layout()
    plt.savefig(result_dir+'VE707-'+str(strain)+'_primer_cT.png',dpi=300)
    



