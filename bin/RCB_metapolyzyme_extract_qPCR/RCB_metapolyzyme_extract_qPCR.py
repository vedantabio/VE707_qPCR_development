# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import os 

#import results files which are the files with the Cq and other sample info like well, sample, target etc

data_dir = '../../data/RCB_metapolyzyme_extract_qPCR'
result_dir = '../../results/RCB_metapolyzyme_extract_qPCR/'

#get all results files in the data dir
result_files = []
for file in os.listdir(data_dir):
    if 'Results' in file:
        result_files.append(file)
#%%
#combine all data into one df and add annealing and plate number information contained in file name
all_cq = pd.DataFrame()
for file in result_files:
    plate_data = pd.read_excel(data_dir+'/'+file,header=25)
    all_cq = pd.concat([all_cq,plate_data])
all_cq.reset_index(inplace=True)
#make all undetermined Cq values zero and cast as float type
all_cq.loc[all_cq['Cq']=='UNDETERMINED','Cq'] = 41
all_cq = all_cq.astype({'Cq':'float'})
        
#%%
#plot the target sample Cq for each primer pair 
all_cq.sort_values('Target',inplace=True)
target_data = all_cq.loc[all_cq['Sample']!='NTC',:]
fig,ax = plt.subplots()
fig.set_size_inches(13,4)
colors = sns.color_palette("Paired")
sns.barplot(data=target_data, x='Target',y='Cq',hue='Sample',ax=ax,palette=colors,errwidth=1,capsize=0.05)
#sns.stripplot(data=target_data,x='Target',y='Cq',ax=ax, hue='Sample',dodge=True,alpha=0.5,size=3,color=sns.color_palette("Set2")[1])
plt.axhline(y=41,color='r',linestyle='--',label='Undetermined (Cq = 41)')
plt.title('Target gDNA Cq PowerFecal v Metapolyzyme')
plt.xticks(rotation=90,size=7)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',title='Extraction Method')
fig.tight_layout()
plt.savefig(result_dir+'all_target_extraction_method.png',dpi=300)

#%%
#plot each strain individually
# for strain in all_cq['Target'].unique():
#     strain_data = all_cq.loc[all_cq['Target']==strain,:]
#     fig, ax = plt.subplots()
#     colors = sns.color_palette("Set2")
#     sns.barplot(data=strain_data, x='primer_pair', y='Cq',ax=ax, palette=colors ,hue='Sample')
#     plt.axhline(y=41,color='r',linestyle='--',label='Undetermined (Cq = 41)')
#     plt.title('VE707-'+str(strain))
#     ax.legend(bbox_to_anchor=(1.05,1),loc='upper left')
#     plt.xticks(rotation=90)
#     fig.tight_layout()
#     plt.savefig(result_dir+'VE707-'+str(strain)+'_primer_cT.png',dpi=300)
    



