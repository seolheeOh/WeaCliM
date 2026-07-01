# %%
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from matplotlib import gridspec
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import sys

ipath = 'data/skills/'
ipath2 = 'data/monsoon_idx/'

def load_first_slice(path, var='p', idx=()):
    with Dataset(path, 'r') as ds:
        return ds.variables[var][idx].squeeze()
    
files = {
        'corr_jja_byol': f'{ipath}/fcst_cor_apr_JJA_gpcp_2000-2019.nc',
        'corr_jja_cnn':  f'{ipath}/ref_cnn_monthly_cor_apr_JJA_gpcp_2000-2019.nc',
        'corr_jja_dyn': f'{ipath}/avg.dyn_cor_may_JJA_gpcp_2000-2019.nc',

        'corr_djf_byol': f'{ipath}/fcst_cor_oct_DJF_gpcp_2000-2019.nc',
        'corr_djf_cnn': f'{ipath}/ref_cnn_monthly_cor_oct_DJF_gpcp_2000-2019.nc',
        'corr_djf_dyn': f'{ipath}/avg.dyn_cor_nov_DJF_gpcp_2000-2019.nc',

        'mse_jja_byol': f'{ipath}/fcst_mse_apr_JJA_gpcp_2000-2019.nc',
        'mse_jja_cnn':  f'{ipath}/ref_cnn_monthly_mse_apr_JJA_gpcp_2000-2019.nc',
        'mse_jja_dyn': f'{ipath}/avg.dyn_mse_may_JJA_gpcp_2000-2019.nc',

        'mse_djf_byol': f'{ipath}/fcst_mse_oct_DJF_gpcp_2000-2019.nc',
        'mse_djf_cnn':  f'{ipath}/ref_cnn_monthly_mse_oct_DJF_gpcp_2000-2019.nc',
        'mse_djf_dyn': f'{ipath}/avg.dyn_mse_nov_DJF_gpcp_2000-2019.nc',

        'in_jja_obs':f'{ipath2}/lab_JJA_gpcp_IN_2000-2019.nc',
        'in_jja_byol':f'{ipath2}/fcst_apr_JJA_gpcp_IN_2000-2019.nc',
        'in_jja_dyn':f'{ipath2}/avg.dyn_may_JJA_prcp_IN_2000-2019.nc',

        'ea_jja_obs':f'{ipath2}/lab_JJA_gpcp_EA_2000-2019.nc',
        'ea_jja_byol':f'{ipath2}/fcst_apr_JJA_gpcp_EA_2000-2019.nc',
        'ea_jja_dyn':f'{ipath2}/avg.dyn_may_JJA_prcp_EA_2000-2019.nc',

        'nam_jja_obs':f'{ipath2}/lab_JJA_gpcp_NAM_2000-2019.nc',
        'nam_jja_byol':f'{ipath2}/fcst_apr_JJA_gpcp_NAM_2000-2019.nc',
        'nam_jja_dyn':f'{ipath2}/avg.dyn_may_JJA_prcp_NAM_2000-2019.nc',

        'sam_djf_obs':f'{ipath2}/lab_DJF_gpcp_SAM_2000-2019.nc',
        'sam_djf_byol':f'{ipath2}/fcst_oct_DJF_gpcp_SAM_2000-2019.nc',
        'sam_djf_dyn':f'{ipath2}/avg.dyn_nov_DJF_prcp_SAM_2000-2019.nc',

        'saf_djf_obs':f'{ipath2}/lab_DJF_gpcp_SAF_2000-2019.nc',
        'saf_djf_byol':f'{ipath2}/fcst_oct_DJF_gpcp_SAF_2000-2019.nc',
        'saf_djf_dyn':f'{ipath2}/avg.dyn_nov_DJF_prcp_SAF_2000-2019.nc',

        'naf_jja_obs':f'{ipath2}/lab_JJA_gpcp_NAF_2000-2019.nc',
        'naf_jja_byol':f'{ipath2}/fcst_apr_JJA_gpcp_NAF_2000-2019.nc',
        'naf_jja_dyn':f'{ipath2}/avg.dyn_may_JJA_prcp_NAF_2000-2019.nc',
        }
    
results = { name: load_first_slice(path) for name, path in files.items() }

corr_jja_byol = results['corr_jja_byol']
corr_jja_cnn  = results['corr_jja_cnn']
corr_jja_dyn = results['corr_jja_dyn']

mse_jja_byol = results['mse_jja_byol']
mse_jja_cnn  = results['mse_jja_cnn']
mse_jja_dyn = results['mse_jja_dyn']

corr_djf_byol = results['corr_djf_byol']
corr_djf_cnn = results['corr_djf_cnn']
corr_djf_dyn = results['corr_djf_dyn']
mse_djf_byol = results['mse_djf_byol']
mse_djf_cnn = results['mse_djf_cnn']
mse_djf_dyn = results['mse_djf_dyn']

in_jja_obs = results['in_jja_obs']
in_jja_byol = results['in_jja_byol']
in_jja_dyn = results['in_jja_dyn']
ea_jja_obs = results['ea_jja_obs']
ea_jja_byol = results['ea_jja_byol']
ea_jja_dyn = results['ea_jja_dyn']
nam_jja_obs = results['nam_jja_obs']
nam_jja_byol = results['nam_jja_byol']
nam_jja_dyn = results['nam_jja_dyn']

sam_djf_obs = results['sam_djf_obs']
sam_djf_byol = results['sam_djf_byol']
sam_djf_dyn = results['sam_djf_dyn']
saf_djf_obs = results['saf_djf_obs']
saf_djf_byol = results['saf_djf_byol']
saf_djf_dyn = results['saf_djf_dyn']
naf_jja_obs = results['naf_jja_obs']
naf_jja_byol = results['naf_jja_byol']
naf_jja_dyn = results['naf_jja_dyn']

# MSSS
msss_jja_dyn = (mse_jja_dyn-mse_jja_byol)/mse_jja_dyn
msss_djf_dyn = (mse_djf_dyn-mse_djf_byol)/mse_djf_dyn

fig = plt.figure(figsize=(12, 7))
outer_gs = gridspec.GridSpec(
        nrows=2, ncols=1,
        height_ratios=[1, 1],
        hspace=0.25,
        figure=fig)

top_gs = gridspec.GridSpecFromSubplotSpec(
        nrows=1, ncols=2,
        subplot_spec=outer_gs[0],
        width_ratios=[1, 1],
        wspace=0.1, hspace=0.05
        )

lat = np.arange(-70, 70+0.01, 5)
deg_fmt = mticker.FuncFormatter(lambda x, pos: f"{x:.0f}°")

# (1-1) JJA Correlation
ax_corr_jja = fig.add_subplot(top_gs[0, 0])
ax_corr_jja.set_title("a.", loc='left',pad=3)
ax_corr_jja.set_xlabel("Latitude")
#ax_corr_jja.set_ylabel("Correlation")

models = {
        'WeaCliM': corr_jja_byol,        # shape (n_lon, n_lat)
        }
colors = {'WeaCliM':'red','MonthlyCNN':'green','Dynamical models':'blue'}
colors2 = {'WeaCliM':'red','MonthlyCNN':'none','Dynamical models':'skyblue'}
offsets = {'WeaCliM': 0.0, 'MonthlyCNN': 0.0, 'Dynamical models': +1}

linestys = {'WeaCliM':'-','MonthlyCNN':'None','Dynamical models':'-'}
linecols = {'WeaCliM':'-','MonthlyCNN':'green','Dynamical models':'none'}

zorders = {'WeaCliM': 10, 'MonthlyCNN' : 5, 'Dynamical models': 1}
yticks = np.arange(-0.4, 1.01, 0.2)
xticks = np.arange(-70, 70.01, 20)

for name, data in models.items():
    med = np.mean(data, 1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_corr_jja.errorbar(lat, med,yerr=[med - p25, p75 - med],
            fmt='none', capsize=0, elinewidth=3,
            marker=None, label=name,color=colors[name], alpha=1,
            zorder=zorders[name],
            clip_on=False)
    ax_corr_jja.errorbar(lat, med,yerr=[med - p10, p90 - med],
            fmt='-', capsize=2, elinewidth=1,
            marker='o', markersize=5,label=name,
            markeredgecolor='black', # 마커 테두리 색
            markeredgewidth=1,
            color=colors[name], alpha=1, 
            clip_on=False,
            zorder = zorders[name]+1
            )
    
models = {
        'MonthlyCNN': corr_jja_cnn,
        'Dynamical models': corr_jja_dyn
        }

for name, data in models.items():
    med = np.mean(data,1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_corr_jja.plot(lat, med, color=colors[name], lw=1, label=name, zorder=zorders[name]+1)
    if name != 'MonthlyCNN':
        ax_corr_jja.fill_between(lat, p10, p90,
                label=f'{name} 10-90%',
                facecolor=colors2[name],
                alpha=0.6,              
                edgecolor=linecols[name],       
                linestyle=linestys[name],
                linewidth=1.3,
                zorder = zorders[name]
                )
    
    ax_corr_jja.set_xlim(-70, 70)
    ax_corr_jja.set_xticks(xticks)
    ax_corr_jja.xaxis.set_major_formatter(deg_fmt)

    ax_corr_jja.set_ylim(-0.4, 1)
    ax_corr_jja.set_yticks(yticks)
    ax_corr_jja.set_yticklabels([f"{t:.1f}" for t in yticks])

    ax_corr_jja.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_corr_jja.tick_params(axis='both', labelsize=8, pad = 0.1)

handles, labels = ax_corr_jja.get_legend_handles_labels()
handles = [handles[i] for i in [-1, 0, 1]]
labels  = [labels[i]  for i in [-1, 0, 1]]
ax_corr_jja.legend(handles, labels, loc='upper right', prop={'size':7}, ncol=3)

# (1-2) DJF Correlation
ax_corr_djf = fig.add_subplot(top_gs[0, 1])
ax_corr_djf.set_title("b.", loc='left',pad=3)
ax_corr_djf.set_xlabel("Latitude")

models = {
        'WeaCliM': corr_djf_byol,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'MonthlyCNN' : 2, 'Dynamical models': 1}
for name, data in models.items():
    med = np.mean(data, 1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_corr_djf.errorbar(lat, med,yerr=[med - p25, p75 - med],
            fmt='none', capsize=0, elinewidth=3,
            marker=None, label=name,color=colors[name], alpha=1,
            clip_on = False,
            zorder = zorders[name])
    ax_corr_djf.errorbar(lat, med,yerr=[med - p10, p90 - med],
            fmt='-', capsize=2, elinewidth=1,
            marker='o', markersize=5,
#            markerfacecolor='white',
            markeredgecolor='black',
            markeredgewidth=1,
            label=name,
            color=colors[name], 
            alpha=1,
            zorder = zorders[name]+1,
            clip_on = False)
    
models = {
        'MonthlyCNN': corr_djf_cnn,
        'Dynamical models': corr_djf_dyn
        }

for name, data in models.items():
    med = np.percentile(data, 50, axis=1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_corr_djf.plot(lat, med, color=colors[name], lw=1, label=name)
    if name != 'MonthlyCNN':
        ax_corr_djf.fill_between(lat, p10, p90,
                label=f'{name} 10-90%',
                facecolor=colors2[name],
                alpha=0.6,        
                edgecolor=linecols[name],      
                linestyle=linestys[name],         
                linewidth=1.3,
                zorder = zorders[name])
        
    ax_corr_djf.set_ylim(-0.4, 1)
    ax_corr_djf.set_yticks(yticks)
    ax_corr_djf.set_yticklabels([f"{t:.1f}" for t in yticks])
    ax_corr_djf.set_xlim(-70, 70)
    ax_corr_djf.set_xticks(xticks)
    ax_corr_djf.xaxis.set_major_formatter(deg_fmt)
    ax_corr_djf.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_corr_djf.tick_params(axis='both', labelsize=8, pad = 0.1)

ax_corr_djf.legend(handles, labels, loc='upper right', prop={'size':7}, ncol=3)

bot_gs = gridspec.GridSpecFromSubplotSpec(
        nrows=2, ncols=2,
        subplot_spec=outer_gs[1],
        width_ratios=[1, 3],
        height_ratios=[1, 1],
        wspace=0.07, hspace=0.5
        )

# (3) JJA RSR
ax_msss_jja = fig.add_subplot(bot_gs[0, 0])
ax_msss_jja.set_title("c.", loc='left',pad=3)
models = {
        'WeaCliM': msss_jja_dyn,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'MonthlyCNN' : 2, 'Dynamical models': 1}
for name, data in models.items():
    med = np.mean(data, 1)
#    med = np.percentile(data, 50, axis=1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_msss_jja.plot(lat, med, color='red', lw=2, label=name, zorder=2)
    ax_msss_jja.fill_between(lat, p10, p90,
            label=f'{name} 10-90%',
            facecolor='red', 
            alpha=0.2,            
            zorder = 1
            )

    ax_msss_jja.axhline(0, color='k', linewidth=0.5, zorder=0)
    ax_msss_jja.set_ylim(-1.5, 1)
    ax_msss_jja.set_xlim(-70, 70)
    ax_msss_jja.set_xticks(xticks)
    ax_msss_jja.xaxis.set_major_formatter(deg_fmt)
    ax_msss_jja.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_msss_jja.tick_params(axis='both', labelsize=8, pad = 0.1)

# (4) DJF RSR
ax_msss_djf = fig.add_subplot(bot_gs[1, 0])
ax_msss_djf.set_title("d.", loc='left',pad=3)
#ax_msss_djf.set_xlabel("Latitude")
models = {
        'WeaCliM': msss_djf_dyn,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'MonthlyCNN' : 2, 'Dynamical models': 1}
for name, data in models.items():
    med = np.mean(data, 1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    
    ax_msss_djf.plot(lat, med, color='red', lw=2, label=name, zorder=2)
    ax_msss_djf.fill_between(lat, p10, p90,
            label=f'{name} 10-90%',
            facecolor='red',  
            alpha=0.2,         
            zorder = 1)# 선 굵기
    ax_msss_djf.axhline(0, color='k', linewidth=0.5, zorder=0)
    ax_msss_djf.set_ylim(-1.5, 1)
    ax_msss_djf.set_xticks(xticks)
    ax_msss_djf.set_xlim(-70, 70)
    ax_msss_djf.xaxis.set_major_formatter(deg_fmt)
    ax_msss_djf.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_msss_djf.tick_params(axis='both', labelsize=8, pad = 0.1)

# (3)
ts_gs = gridspec.GridSpecFromSubplotSpec(
        nrows=2, ncols=3,
        subplot_spec=bot_gs[:, 1],
        wspace=0.15, hspace=0.5
        )

axes_ts = []
for i in range(2):
    for j in range(3):
        ax = fig.add_subplot(ts_gs[i, j])
        axes_ts.append(ax)

jja_time = np.arange(2000, 2020)
djf_time = np.arange(2001, 2021)

# 1) 
regions   = ['e.','f.','g.',
        'h.','i.','j.']
obs_list  = [ea_jja_obs, in_jja_obs, naf_jja_obs,
        nam_jja_obs, sam_djf_obs,saf_djf_obs]

byol_list  = [ea_jja_byol, in_jja_byol, naf_jja_byol,
        nam_jja_byol, sam_djf_byol,saf_djf_byol]

dyn_list = [ea_jja_dyn, in_jja_dyn, naf_jja_dyn,
        nam_jja_dyn, sam_djf_dyn, saf_djf_dyn]

upper_range_list = [4.7, 4.7, 4.7, 5, 4.7, 4.7]
lower_range_list = [-3.5, -3.5, -3.5, -3.5, -3.5, -3.5]

xticks = np.arange(2000, 2019, 5)

# 2) 
for ax, region, obs_ts, byol_ts, dyn_ts, upp_ranges, low_ranges in zip(axes_ts, regions, obs_list, byol_list, dyn_list, upper_range_list, lower_range_list):
    # Obs:
    ax.bar(jja_time, obs_ts,
            color='k', align='center', width=0.6, alpha=0.5, label='ERA5', zorder=0)
    ax.plot(jja_time, byol_ts,
            color='r', linestyle='-', linewidth=1, 
            marker = 'o', markersize=3,
            label=f'WeaCliM (r={np.corrcoef(byol_ts, obs_ts)[0,1].round(2)})',
            zorder = 2)
    
    # Dynamical models :
    ax.plot(jja_time, dyn_ts,
            color='blue', linestyle='-', linewidth=1, 
            marker = None, markersize=5,
            label=f'Dyn. (r={np.corrcoef(dyn_ts, obs_ts)[0,1].round(2)})',
            zorder=1)

    #yticks = np.arange(np.ceil(low_ranges), np.ceil(upp_ranges), 2)
    yticks = np.arange(-2, 4+0.0001, 2)
    ax.axhline(0, color='black', linewidth=0.5)

    ax.set_title(region, loc='left', fontsize=12, pad=3)
    ax.set_ylim(low_ranges, upp_ranges)
    ax.set_yticks(yticks)
    ax.set_xticks(xticks)

    
#    ax.set_yticklabels([f"{t:.2f}" for t in yticks])
    ax.tick_params(axis='both', labelsize=8, pad = 0.1)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

    order = [2, 0, 1]
        
    handles, labels = ax.get_legend_handles_labels()
    ax.legend([handles[i] for i in order], [labels[i] for i in order],
            loc='upper left', prop={'size':6.51}, ncol=3,
            labelspacing=0.1,   
            columnspacing=0.5,
            handlelength=1.5,
            handletextpad=0.4,
            borderpad=0.4
            )

plt.tight_layout()
fig.subplots_adjust(
        left=0.05, 
        right=0.98, 
        top=0.95,   
        bottom=0.05, 
        hspace=0.25,
        wspace=0.20,
        )

plt.show()

