# %%
import sys
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pandas as pd
from matplotlib.ticker import MultipleLocator

main_dir = '/home/seolhee_oh/proceeding/byol_weather'

ipath = f'{main_dir}/src/mk01_feature_cor/data'
fname1 = f'feature1_train_t2m_apr_JJA_explained_variance_2000-2019.csv'
fname2 = f'feature2_train_t2m_apr_JJA_explained_variance_2000-2019.csv'

# BYOL
byol1 = pd.read_csv(f'{ipath}/{fname1}')['explained_variance'].values
byol2 = pd.read_csv(f'{ipath}/{fname2}')['explained_variance'].values

lon2 = len(np.arange(0,  360, 5))
lat2 = len(np.arange(-70, 75, 5))

cnn1 = np.zeros((10, lat2, lon2))
cnn2 = np.zeros((10, lat2, lon2))

for i, lon in enumerate(range(0,360, 5)):
    for j, lat in enumerate(range(-70, 75, 5)):
        fname1 = f'ref_feature1_train_t2m_{lon}E_{lat}N_apr_JJA_explained_variance_2000-2019.csv'
        fname2 = f'ref_feature2_train_t2m_{lon}E_{lat}N_apr_JJA_explained_variance_2000-2019.csv'
        cnn1[:, j, i] = pd.read_csv(f'{ipath}/{fname1}')['explained_variance'].values
        cnn2[:, j, i]  = pd.read_csv(f'{ipath}/{fname2}')['explained_variance'].values

cnn1 = cnn1.reshape(10, -1)
cnn2 = cnn2.reshape(10, -1)

cnn1_p025 = np.percentile(cnn1, 0, axis=1)
cnn1_p975 = np.percentile(cnn1, 100, axis=1)
cnn1_mean = cnn1.mean(axis=1)

err_lower_1 = cnn1_mean - cnn1_p025
err_upper_1 = cnn1_p975 - cnn1_mean

cnn2_p025 = np.percentile(cnn2, 0, axis=1)
cnn2_p975 = np.percentile(cnn2, 100, axis=1)
cnn2_mean = cnn2.mean(axis=1)

err_lower_2 = cnn2_mean - cnn2_p025
err_upper_2 = cnn2_p975 - cnn2_mean

titles = ['a.', 'b.']
byols = [byol1, byol2]
cnns = [cnn1_mean, cnn2_mean]
err_lowers = [err_lower_1, err_lower_2]
err_uppers = [err_upper_1, err_upper_2]

# x축: 1~10번째 모드
modes = np.arange(1, 11)

fig, axes = plt.subplots(nrows=2, ncols=1, 
        figsize=(6, 5), sharex=True)
#        figsize=(7, 5))

for ax, title, byol, cnn, err_upper, err_lower in zip(axes, titles, byols, cnns, err_uppers, err_lowers):

    ax.set_title(title, loc='left', pad=2, fontsize=13)
    ax.plot(modes, byol, 'r-o', markersize=5, label='WeaCliM',zorder=1)
    ax.errorbar(modes,cnn, yerr=[err_lower, err_upper],
            fmt='o',
            markersize = 5,
            linestyle='--',
            capsize=4,
            color='grey',
            label='CNN'
            )
            
#    ax.set_ylabel('Variance',fontsize=12)
    ax.set_xticks(modes)
    ax.set_xticklabels(modes, fontsize=10)
    ax.set_ylim(0.01, 0.12)  # y축 범위: [0, 0.5]
    ax.set_yticks(np.arange(0, 0.12+0.001, 0.02)) 
    ax.set_yticklabels(np.arange(0, 0.12+0.001, 0.02), fontsize=10)
    ax.yaxis.set_minor_locator(MultipleLocator(0.01))

    ax.grid(True, linestyle='--', linewidth=0.7, color='gray', alpha=0.3)
    ax.legend(
            prop={
                'size': 9,
                },
            fontsize=9,
            loc='upper right',
            ncol=2,
#            title='Model',
#            title_fontsize=10
            )

    
axes[-1].set_xlabel('EOF Mode', fontsize=12)
    
plt.tight_layout(rect=(0,0,0.95,1))
#plt.show()
plt.savefig("Extended_Fig5.pdf", dpi=300, format="pdf", bbox_inches="tight")


# %%
