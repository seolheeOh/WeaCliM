# %%
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from matplotlib import gridspec
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import sys

def cor (x, y):
    x -= np.mean(x,0, keepdims=True)
    y -= np.mean(y, 0, keepdims=True)

ipath = '/home/seolhee_oh/proceeding/byol_weather/src/mk05_extremes_skill/data/'

def load_first_slice(path, var='p', idx=()):
    """파일 열고 var[idx] 값만 꺼내서 반환"""
    with Dataset(path, 'r') as ds:
        return ds.variables[var][idx].squeeze()
    
# 읽어들일 파일들과 대상 변수명 매핑
files = {
        'cor_r95p_byol': f'{ipath}/fcst_cor_apr_JJA_gpcp_r95p_mm_2000-2019.nc',
        'cor_r95p_dyn': f'{ipath}/avg.dyn_cor_may_JJA_gpcp_r95p_mm_2000-2019.nc',
        'mse_r95p_byol': f'{ipath}/fcst_mse_apr_JJA_gpcp_r95p_mm_2000-2019.nc',
        'mse_r95p_dyn': f'{ipath}/avg.dyn_mse_may_JJA_gpcp_r95p_mm_2000-2019.nc',

        'cor_r99p_byol': f'{ipath}/fcst_cor_apr_JJA_gpcp_r99p_mm_2000-2019.nc',
        'cor_r99p_dyn': f'{ipath}/avg.dyn_cor_may_JJA_gpcp_r99p_mm_2000-2019.nc',
        'mse_r99p_byol': f'{ipath}/fcst_mse_apr_JJA_gpcp_r99p_mm_2000-2019.nc',
        'mse_r99p_dyn': f'{ipath}/avg.dyn_mse_may_JJA_gpcp_r99p_mm_2000-2019.nc',

        'cor_prcptot_byol': f'{ipath}/fcst_cor_apr_JJA_gpcp_prcptot_2000-2019.nc',
        'cor_prcptot_dyn': f'{ipath}/avg.dyn_cor_may_JJA_gpcp_prcptot_2000-2019.nc',
        'mse_prcptot_byol': f'{ipath}/fcst_mse_apr_JJA_gpcp_prcptot_2000-2019.nc',
        'mse_prcptot_dyn': f'{ipath}/avg.dyn_mse_may_JJA_gpcp_prcptot_2000-2019.nc',

        'cor_rx1day_byol': f'{ipath}/fcst_cor_apr_JJA_gpcp_rx1day_2000-2019.nc',
        'cor_rx1day_dyn': f'{ipath}/avg.dyn_cor_may_JJA_gpcp_rx1day_2000-2019.nc',
        'mse_rx1day_byol': f'{ipath}/fcst_mse_apr_JJA_gpcp_rx1day_2000-2019.nc',
        'mse_rx1day_dyn': f'{ipath}/avg.dyn_mse_may_JJA_gpcp_rx1day_2000-2019.nc',

        }
    
# 한 줄로 모두 로드
results = { name: load_first_slice(path) for name, path in files.items() }

# 필요하면 개별 변수로 언패킹
cor_r95p_byol = results['cor_r95p_byol']
cor_r99p_byol = results['cor_r99p_byol']
cor_prcptot_byol = results['cor_prcptot_byol']
cor_rx1day_byol = results['cor_rx1day_byol']

mse_r95p_byol = results['mse_r95p_byol']
mse_r99p_byol = results['mse_r99p_byol']
mse_prcptot_byol = results['mse_prcptot_byol']
mse_rx1day_byol = results['mse_rx1day_byol']

cor_r95p_dyn = results['cor_r95p_dyn']
cor_r99p_dyn = results['cor_r99p_dyn']
cor_prcptot_dyn = results['cor_prcptot_dyn']
cor_rx1day_dyn = results['cor_rx1day_dyn']

mse_r95p_dyn = results['mse_r95p_dyn']
mse_r99p_dyn = results['mse_r99p_dyn']
mse_prcptot_dyn = results['mse_prcptot_dyn']
mse_rx1day_dyn = results['mse_rx1day_dyn']

mse_r95p_dyn = mse_r95p_dyn.filled(np.nan)
mse_r95p_dyn = np.asarray(mse_r95p_dyn, dtype=float)
mse_r95p_byol = mse_r95p_byol.filled(np.nan)
mse_r95p_byol = np.asarray(mse_r95p_byol, dtype=float)

mse_r99p_dyn = mse_r99p_dyn.filled(np.nan)
mse_r99p_dyn = np.asarray(mse_r99p_dyn, dtype=float)
mse_r99p_byol = mse_r99p_byol.filled(np.nan)
mse_r99p_byol = np.asarray(mse_r99p_byol, dtype=float)

mse_prcptot_dyn = mse_prcptot_dyn.filled(np.nan)
mse_prcptot_dyn = np.asarray(mse_prcptot_dyn, dtype=float)
mse_prcptot_byol = mse_prcptot_byol.filled(np.nan)
mse_prcptot_byol = np.asarray(mse_prcptot_byol, dtype=float)

mse_rx1day_dyn = mse_rx1day_dyn.filled(np.nan)
mse_rx1day_dyn = np.asarray(mse_rx1day_dyn, dtype=float)
mse_rx1day_byol = mse_rx1day_byol.filled(np.nan)
mse_rx1day_byol = np.asarray(mse_rx1day_byol, dtype=float)

# MSSS
msss_r95p_dyn = (mse_r95p_dyn-mse_r95p_byol)/mse_r95p_dyn
msss_r99p_dyn = (mse_r99p_dyn-mse_r99p_byol)/mse_r99p_dyn
msss_prcptot_dyn = (mse_prcptot_dyn-mse_prcptot_byol)/mse_prcptot_dyn
msss_rx1day_dyn = (mse_rx1day_dyn-mse_rx1day_byol)/mse_rx1day_dyn

# ─────────────────────────────────────────────────────────────
# 1) 외부 GridSpec: 상단(1행) / 하단(1행) — 높이 비율 1:2
# ─────────────────────────────────────────────────────────────
#fig = plt.figure(figsize=(14, 8), constrained_layout=True)
fig = plt.figure(figsize=(12, 7))
outer_gs = gridspec.GridSpec(
        nrows=2, ncols=1,
        height_ratios=[3, 1],
        hspace=0.25,
        figure=fig)

# ─────────────────────────────────────────────────────────────
# 2) 상단: 1×2 내부 GridSpec — 너비 비율 1:1
# ─────────────────────────────────────────────────────────────
top_gs = gridspec.GridSpecFromSubplotSpec(
        nrows=2, ncols=2,
        subplot_spec=outer_gs[0],
        width_ratios=[1, 1],
        wspace=0.1, hspace=0.3
        )

lat = np.arange(-70, 70+0.01, 5)
deg_fmt = mticker.FuncFormatter(lambda x, pos: f"{x:.0f}°")

# (1-1) JJA Correlation (상단 왼쪽)
ax_cor_r95p = fig.add_subplot(top_gs[0, 0])
ax_cor_r95p.set_title("a.", loc='left',pad=3)
ax_cor_r95p.set_xlabel("Latitude")
#ax_cor_r95p.set_ylabel("Correlation")

models = {
        'WeaCliM': cor_r95p_byol,        # shape (n_lon, n_lat)
        }
colors = {'WeaCliM':'red','Dynamical models':'blue'}
colors2 = {'WeaCliM':'red','Dynamical models':'skyblue'}
offsets = {'WeaCliM': 0.0, 'Dynamical models': +1}

linestys = {'WeaCliM':'-','Dynamical models':'-'}
linecols = {'WeaCliM':'-','Dynamical models':'none'}

zorders = {'WeaCliM': 10, 'Dynamical models': 1}
yticks = np.arange(-0.4, 1.01, 0.2)
xticks = np.arange(-70, 70.01, 20)

for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_cor_r95p.errorbar(lat, med,yerr=[med - p25, p75 - med],
            fmt='none', capsize=0, elinewidth=3,
            marker=None, label=name,color=colors[name], alpha=1,
            zorder=zorders[name],
            clip_on=False)
    ax_cor_r95p.errorbar(lat, med,yerr=[med - p10, p90 - med],
            fmt='-', capsize=2, elinewidth=1,
            marker='o', markersize=5,label=name,
            markeredgecolor='black', # 마커 테두리 색
            markeredgewidth=1,
            color=colors[name], alpha=1, 
            clip_on=False,
            zorder = zorders[name]+1
            )
    
models = {
        'Dynamical models': cor_r95p_dyn
        }

for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_cor_r95p.plot(lat, med, color=colors[name], lw=1, label=name, zorder=zorders[name]+1)
    if name != 'MonthlyCNN':
        ax_cor_r95p.fill_between(lat, p10, p90,
                label=f'{name} 10–90%',
                facecolor=colors2[name],   # 내부 채우기 색
                alpha=0.6,                # 내부 투명도
                edgecolor=linecols[name],        # 테두리 선 색
                linestyle=linestys[name],           # 선 스타일 (점선)
                linewidth=1.3,
                zorder = zorders[name]
                )
    
    ax_cor_r95p.set_xlim(-70, 70)
    ax_cor_r95p.set_xticks(xticks)
    ax_cor_r95p.xaxis.set_major_formatter(deg_fmt)

    ax_cor_r95p.set_ylim(-0.4, 1)
    ax_cor_r95p.set_yticks(yticks)
    ax_cor_r95p.set_yticklabels([f"{t:.1f}" for t in yticks])

    ax_cor_r95p.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_cor_r95p.tick_params(axis='both', labelsize=8, pad = 0.1)

handles, labels = ax_cor_r95p.get_legend_handles_labels()
handles = [handles[i] for i in [-1, 0]]
labels  = [labels[i]  for i in [-1, 0]]
ax_cor_r95p.legend(handles, labels, loc='upper right', prop={'size':7}, ncol=3)

# (1-2) DJF Correlation (상단 왼쪽)
ax_cor_r99p = fig.add_subplot(top_gs[0, 1])
ax_cor_r99p.set_title("b.", loc='left',pad=3)
ax_cor_r99p.set_xlabel("Latitude")

models = {
        'WeaCliM': cor_r99p_byol,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'Dynamical models': 1}
for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_cor_r99p.errorbar(lat, med,yerr=[med - p25, p75 - med],
            fmt='none', capsize=0, elinewidth=3,
            marker=None, label=name,color=colors[name], alpha=1,
            clip_on = False,
            zorder = zorders[name])
    ax_cor_r99p.errorbar(lat, med,yerr=[med - p10, p90 - med],
            fmt='-', capsize=2, elinewidth=1,
            marker='o', markersize=5,
#            markerfacecolor='white',      # 마커 내부 색
            markeredgecolor='black', # 마커 테두리 색
            markeredgewidth=1,
            label=name,
            color=colors[name], 
            alpha=1,
            zorder = zorders[name]+1,
            clip_on = False)
    
models = {
        'Dynamical models': cor_r99p_dyn
        }

for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.nanpercentile(data, [25,75], axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    p5, p95  = np.nanpercentile(data, [5,95], axis=1)
    
    ax_cor_r99p.plot(lat, med, color=colors[name], lw=1, label=name)
    if name != 'MonthlyCNN':
        ax_cor_r99p.fill_between(lat, p10, p90,
                label=f'{name} 10–90%',
                facecolor=colors2[name],   # 내부 채우기 색
                alpha=0.6,              # 내부 투명도
                edgecolor=linecols[name],        # 테두리 선 색
                linestyle=linestys[name],           # 선 스타일 (점선)
                linewidth=1.3,
                zorder = zorders[name])
        
    ax_cor_r99p.set_ylim(-0.4, 1)
    ax_cor_r99p.set_yticks(yticks)
    ax_cor_r99p.set_yticklabels([f"{t:.1f}" for t in yticks])
    ax_cor_r99p.set_xlim(-70, 70)
    ax_cor_r99p.set_xticks(xticks)
    ax_cor_r99p.xaxis.set_major_formatter(deg_fmt)
    ax_cor_r99p.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_cor_r99p.tick_params(axis='both', labelsize=8, pad = 0.1)

ax_cor_r99p.legend(handles, labels, loc='upper right', prop={'size':7}, ncol=3)

# (2-1) PRCPTOT Correlation (상단 왼쪽)
ax_cor_prcptot = fig.add_subplot(top_gs[1, 0])
ax_cor_prcptot.set_title("c.", loc='left',pad=3)
ax_cor_prcptot.set_xlabel("Latitude")

models = {
        'WeaCliM': cor_prcptot_byol,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'Dynamical models': 1}
for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.nanpercentile(data, [25,75], axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    p5, p95  = np.nanpercentile(data, [5,95], axis=1)
    
    ax_cor_prcptot.errorbar(lat, med,yerr=[med - p25, p75 - med],
            fmt='none', capsize=0, elinewidth=3,
            marker=None, label=name,color=colors[name], alpha=1,
            clip_on = False,
            zorder = zorders[name])
    ax_cor_prcptot.errorbar(lat, med,yerr=[med - p10, p90 - med],
            fmt='-', capsize=2, elinewidth=1,
            marker='o', markersize=5,
#            markerfacecolor='white',      # 마커 내부 색
            markeredgecolor='black', # 마커 테두리 색
            markeredgewidth=1,
            label=name,
            color=colors[name], 
            alpha=1,
            zorder = zorders[name]+1,
            clip_on = False)
    
models = {
        'Dynamical models': cor_prcptot_dyn
        }

for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.nanpercentile(data, [25,75], axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    p5, p95  = np.nanpercentile(data, [5,95], axis=1)
    
    ax_cor_prcptot.plot(lat, med, color=colors[name], lw=1, label=name)
    if name != 'MonthlyCNN':
        ax_cor_prcptot.fill_between(lat, p10, p90,
                label=f'{name} 10–90%',
                facecolor=colors2[name],   # 내부 채우기 색
                alpha=0.6,              # 내부 투명도
                edgecolor=linecols[name],        # 테두리 선 색
                linestyle=linestys[name],           # 선 스타일 (점선)
                linewidth=1.3,
                zorder = zorders[name])
        
    ax_cor_prcptot.set_ylim(-0.4, 1)
    ax_cor_prcptot.set_yticks(yticks)
    ax_cor_prcptot.set_yticklabels([f"{t:.1f}" for t in yticks])
    ax_cor_prcptot.set_xlim(-70, 70)
    ax_cor_prcptot.set_xticks(xticks)
    ax_cor_prcptot.xaxis.set_major_formatter(deg_fmt)
    ax_cor_prcptot.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_cor_prcptot.tick_params(axis='both', labelsize=8, pad = 0.1)

ax_cor_prcptot.legend(handles, labels, loc='upper right', prop={'size':7}, ncol=3)

# (2-2) RX1DAY Correlation (상단 왼쪽)
ax_cor_rx1day = fig.add_subplot(top_gs[1, 1])
ax_cor_rx1day.set_title("d.", loc='left',pad=3)
ax_cor_rx1day.set_xlabel("Latitude")

models = {
        'WeaCliM': cor_rx1day_byol,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'Dynamical models': 1}
for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.nanpercentile(data, [25,75], axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    p5, p95  = np.nanpercentile(data, [5,95], axis=1)
    
    ax_cor_rx1day.errorbar(lat, med,yerr=[med - p25, p75 - med],
            fmt='none', capsize=0, elinewidth=3,
            marker=None, label=name,color=colors[name], alpha=1,
            clip_on = False,
            zorder = zorders[name])
    ax_cor_rx1day.errorbar(lat, med,yerr=[med - p10, p90 - med],
            fmt='-', capsize=2, elinewidth=1,
            marker='o', markersize=5,
#            markerfacecolor='white',      # 마커 내부 색
            markeredgecolor='black', # 마커 테두리 색
            markeredgewidth=1,
            label=name,
            color=colors[name], 
            alpha=1,
            zorder = zorders[name]+1,
            clip_on = False)
    
models = {
        'Dynamical models': cor_rx1day_dyn
        }

for name, data in models.items():
    med = np.percentile(data, 50, axis=1)
    p25, p75 = np.percentile(data, [25,75], axis=1)
    p10, p90 = np.percentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_cor_rx1day.plot(lat, med, color=colors[name], lw=1, label=name)
    if name != 'MonthlyCNN':
        ax_cor_rx1day.fill_between(lat, p10, p90,
                label=f'{name} 10–90%',
                facecolor=colors2[name],   # 내부 채우기 색
                alpha=0.6,              # 내부 투명도
                edgecolor=linecols[name],        # 테두리 선 색
                linestyle=linestys[name],           # 선 스타일 (점선)
                linewidth=1.3,
                zorder = zorders[name])
        
    ax_cor_rx1day.set_ylim(-0.4, 1)
    ax_cor_rx1day.set_yticks(yticks)
    ax_cor_rx1day.set_yticklabels([f"{t:.1f}" for t in yticks])
    ax_cor_rx1day.set_xlim(-70, 70)
    ax_cor_rx1day.set_xticks(xticks)
    ax_cor_rx1day.xaxis.set_major_formatter(deg_fmt)
    ax_cor_rx1day.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_cor_rx1day.tick_params(axis='both', labelsize=8, pad = 0.1)

ax_cor_rx1day.legend(handles, labels, loc='upper right', prop={'size':7}, ncol=3)

# ─────────────────────────────────────────────────────────────
# 3) 하단: 2×2 내부 GridSpec — 너비 비율 1:2, 높이 비율 1:1
# ─────────────────────────────────────────────────────────────
bot_gs = gridspec.GridSpecFromSubplotSpec(
        nrows=1, ncols=4,
        subplot_spec=outer_gs[1],
        width_ratios=[1, 1, 1, 1],
        wspace=0.2
        )

# (1) R95p MSSS
ax_msss_r95p = fig.add_subplot(bot_gs[0, 0])
ax_msss_r95p.set_title("e.", loc='left',pad=3)
models = {
        'WeaCliM': msss_r95p_dyn,        # shape (n_lon, n_lat)
#        'Dynamical models': mse_r95p_dyn,        # shape (n_lon, n_lat)
#        'WeaCliM': mse_r95p_byol,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'Dynamical models': 1}
for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.nanpercentile(data, [25,75], axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    p5, p95  = np.nanpercentile(data, [5,95], axis=1)
    
    ax_msss_r95p.plot(lat, med, color='red', lw=2, label=name, zorder=2)
    ax_msss_r95p.fill_between(lat, p10, p90,
            label=f'{name} 10-90%',
            facecolor='red',   # 내부 채우기 색
            alpha=0.2,             # 내부 투명도
            zorder = 1# 선 굵기
            )

    ax_msss_r95p.axhline(0, color='k', linewidth=0.5, zorder=0)
    ax_msss_r95p.set_ylim(-1.5, 1)
    ax_msss_r95p.set_xlim(-70, 70)
    ax_msss_r95p.set_xticks(xticks)
    ax_msss_r95p.xaxis.set_major_formatter(deg_fmt)
    ax_msss_r95p.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_msss_r95p.tick_params(axis='both', labelsize=8, pad = 0.1)

# (2) R99p MSSS
ax_msss_r99p = fig.add_subplot(bot_gs[0, 1])
ax_msss_r99p.set_title("f.", loc='left',pad=3)
#ax_msss_r99p.set_xlabel("Latitude")
models = {
        'WeaCliM': msss_r99p_dyn,        # shape (n_lon, n_lat)
#        'WeaCliM': mse_r99p_byol,        # shape (n_lon, n_lat)
#        'Dynamical models': mse_r99p_dyn,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'Dynamical models': 1}
for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    
    ax_msss_r99p.plot(lat, med, color='red', lw=2, label=name, zorder=2)
    ax_msss_r99p.fill_between(lat, p10, p90,
            label=f'{name} 10-90%',
            facecolor='red',   # 내부 채우기 색
            alpha=0.2,             # 내부 투명도
            zorder = 1)# 선 굵기
    ax_msss_r99p.axhline(0, color='k', linewidth=0.5, zorder=0)
    ax_msss_r99p.set_ylim(-1.5, 1)
    ax_msss_r99p.set_xticks(xticks)
    ax_msss_r99p.set_xlim(-70, 70)
    ax_msss_r99p.xaxis.set_major_formatter(deg_fmt)
    ax_msss_r99p.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_msss_r99p.tick_params(axis='both', labelsize=8, pad = 0.1)

# (3) PRCPTOT MSSS
ax_msss_prcptot = fig.add_subplot(bot_gs[0, 2])
ax_msss_prcptot.set_title("g.", loc='left',pad=3)
models = {
        'WeaCliM': msss_prcptot_dyn,        # shape (n_lon, n_lat)
#        'Dynamical models': mse_prcptot_dyn,        # shape (n_lon, n_lat)
#        'WeaCliM': mse_prcptot_byol,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'Dynamical models': 1}
for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.nanpercentile(data, [25,75], axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    p5, p95  = np.percentile(data, [5,95], axis=1)
    
    ax_msss_prcptot.plot(lat, med, color='red', lw=2, label=name, zorder=2)
    ax_msss_prcptot.fill_between(lat, p10, p90,
            label=f'{name} 10-90%',
            facecolor='red',   # 내부 채우기 색
            alpha=0.2,             # 내부 투명도
            zorder = 1# 선 굵기
            )

    ax_msss_prcptot.axhline(0, color='k', linewidth=0.5, zorder=0)
    ax_msss_prcptot.set_ylim(-1.5, 1)
    ax_msss_prcptot.set_xlim(-70, 70)
    ax_msss_prcptot.set_xticks(xticks)
    ax_msss_prcptot.xaxis.set_major_formatter(deg_fmt)
    ax_msss_prcptot.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_msss_prcptot.tick_params(axis='both', labelsize=8, pad = 0.1)

# (4) RX1day MSSS
ax_msss_rx1day = fig.add_subplot(bot_gs[0, 3])
ax_msss_rx1day.set_title("h.", loc='left',pad=3)
models = {
        'WeaCliM': msss_rx1day_dyn,        # shape (n_lon, n_lat)
#        'Dynamical models': mse_rx1day_dyn,        # shape (n_lon, n_lat)
#        'WeaCliM': mse_rx1day_byol,        # shape (n_lon, n_lat)
        }
zorders = {'WeaCliM': 3, 'Dynamical models': 1}
for name, data in models.items():
    med = np.nanpercentile(data, 50, axis=1)
    p25, p75 = np.nanpercentile(data, [25,75], axis=1)
    p10, p90 = np.nanpercentile(data, [10,90], axis=1)
    p5, p95  = np.nanpercentile(data, [5,95], axis=1)
    
    ax_msss_rx1day.plot(lat, med, color='red', lw=2, label=name, zorder=2)
    ax_msss_rx1day.fill_between(lat, p10, p90,
            label=f'{name} 10-90%',
            facecolor='red',   # 내부 채우기 색
            alpha=0.2,             # 내부 투명도
            zorder = 1# 선 굵기
            )

    ax_msss_rx1day.axhline(0, color='k', linewidth=0.5, zorder=0)
    ax_msss_rx1day.set_ylim(-1.5, 1)
    ax_msss_rx1day.set_xlim(-70, 70)
    ax_msss_rx1day.set_xticks(xticks)
    ax_msss_rx1day.xaxis.set_major_formatter(deg_fmt)
    ax_msss_rx1day.grid(True, which='both',linestyle='--',color='gray',linewidth=0.5)
    ax_msss_rx1day.tick_params(axis='both', labelsize=8, pad = 0.1)

# ─────────────────────────────────────────────────────────────
# 5) 범례, 레이아웃 정리
# ─────────────────────────────────────────────────────────────
# 한 번에 전체 범례를 그리려면, 축 중 하나에 handles, labels 받아와서 fig.legend() 사용
# handles, labels = ax_cor_r95p.get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper center', ncol=4)

plt.tight_layout()
fig.subplots_adjust(
        left=0.05,   # 좌측 여백
        right=0.98,  # 우측 여백
        top=0.95,    # 상단 여백
        bottom=0.05, # 하단 여백
        hspace=0.25, # 행 간 간격
        wspace=0.20, # 열 간 간격
        )

#plt.show()

plt.savefig("Fig4.pdf", dpi=300, format="pdf", bbox_inches="tight")


# %%
