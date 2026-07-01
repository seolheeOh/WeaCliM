# %%
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from cartopy.io import shapereader
from matplotlib.gridspec import GridSpec
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.patches import Rectangle

target = 2000

main_dir = '/home/seolhee_oh/proceeding/'
opath = f'{main_dir}/byol_weather/jpeg/'
oname = f'fcst_eof_{target}'

# ─── 1) 데이터 로드  ────────────────────────────────────────
years = np.arange(target, target+19+1)

ipath = main_dir+'byol_weather/src/mk03_eof_compare/data/'

fname = f'combine_reg_mix_labPC_labprcp.nc'
ds = xr.open_dataset(ipath + fname)
obs_eof1 = ds['ev1']
obs_var = obs_eof1.std(dim=["lon", "lat"], skipna=True)  
#obs_eof1 = obs_eof1 / (obs_var  + 1e-08)
obs_eof1 = obs_eof1.where(obs_eof1 != 0)

fname = f'combine_reg_mix_labPC_fcstprcp.nc'
ds = xr.open_dataset(ipath + fname)
fcst_eof1 = ds['ev1']
fcst_var = fcst_eof1.std(dim=["lon","lat"], skipna=True)
#fcst_eof1 = fcst_eof1 / (fcst_var  + 1e-08)
fcst_eof1 = fcst_eof1.where(fcst_eof1 != 0)


data_maps = [
        obs_eof1, fcst_eof1
        ]

ipath = main_dir+'byol_weather/src/mk02_compare_skill/data/'
fname = f'fcst_scorr_apr_JJA_gpcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
fcst_jja_scor = ds['p'].squeeze()

fname = f'fcst_scorr_oct_DJF_gpcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
fcst_djf_scor = ds['p'].squeeze()

fname = f'avg.dyn_scorr_may_JJA_gpcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
dyn_jja_scor = ds['p'].squeeze()

fname = f'avg.dyn_scorr_nov_DJF_gpcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
dyn_djf_scor = ds['p'].squeeze()

# ─── 2) Figure & Projection 셋업 ─────────────────────────────────
fig = plt.figure(figsize=(10,  5))
gs = GridSpec(nrows=2, ncols=2, figure=fig,
        height_ratios=[1, 1],
        width_ratios=[2, 1],
        #width_ratios=[1, 2], ## left idx, right map
        hspace=0.4, wspace=0.2)

# 컬러맵 및 한계
cl = 1
contour_levels = np.arange(-cl,cl+0.00000001,cl/10)
contour_levels = np.delete(contour_levels, [int(len(contour_levels)/2)])
cbar_list = np.arange(-cl, cl+0.0001, cl/5)
cbar_list = np.delete(cbar_list, [int(len(cbar_list)/2)])
#cbar_list = [cl-10*(cl/10), cl-8*(cl/10),cl-6*(cl/10),cl-4*(cl/10),cl-2*(cl/10),cl]
cmap = plt.cm.get_cmap('BrBG')

lon = np.arange(120,360+160+5,5)
lat = np.arange(-55,55+5,5)

# ─── 3) 상단 지도 4패널 ───────────────────────────────────────────

titles_map = [
        f'a.',
        f'b.',
        ]

regions = {
        "Tropics": {    # 북반구 열대
            "lon": (120, 280),   # 120°E → 80°W
            "lat": (-30, 30),     # 30°S → 30°N
            "sty": '-',
            },
        "ISM": {
            "lon": (70+360, 100+360),
            "lat": (10, 30),
            "sty": '--',
            },
#        "WNPSM": {
#            "lon": (110+360, 150+360),
#            "lat": (10, 25),
#            "sty": '--',
#            },
        "EASM": {
            "lon": (100+360, 140+360),
            "lat": (0, 50),
            "sty": '--',
            },
#        "NASM": {
#            "lon": (360-110, 360-80),
#            "lat": (5, 25),
#            "sty": '--',
#            },
        "NAFSM": {
            "lon": (360-30, 360+30),
            "lat": (0, 20),
            "sty": '--',
            },
        "SASM": {
            "lon": (360-80, 360-30),
            "lat": (-45, 15),
            "sty": '-',
            },
        "SAFSM": {
            "lon": (25+360, 70+360),
            "lat": (-25, -5),
            "sty": '-',
            },
        "AUSSM": {
            "lon": (110+360, 155+360),
            "lat": (-40, -5),
            "sty": '-',
            },
        }

axes_map = []
#for idx, (r, c) in enumerate([(0,1), (1,1)]): ## org map position
for idx, (r, c) in enumerate([(0,0), (1,0)]):
    ax = fig.add_subplot(gs[r, c:c+1]) ## org map 

    da = data_maps[idx].squeeze()            # ← 여기서 꺼내기
    values = da.values.squeeze()

    ax.set_xticks(np.arange(120, 160+360+30, 40))
    ax.set_yticks(np.arange(-90, 90+20, 20))
#    ax.set_extent([120, 160+359.9,-40,45], crs=proj)
    ax.set_xlim(120, 360+160)
    ax.set_ylim(-55, 55)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.tick_params(axis='both', labelsize=9)
    im = ax.contourf(
            lon, lat, values,
            levels=contour_levels, cmap=cmap,
            extend='both'
            )
    shp = shapereader.natural_earth(resolution='110m',
            category='physical',
            name='coastline')
    for geom in shapereader.Reader(shp).geometries():
        lines = geom.geoms if hasattr(geom, 'geoms') else [geom]
        for line in lines:
            x, y = line.xy
            x = np.array(x)     # 리스트 → numpy 배열
            y = np.array(y)
            ax.plot(x, y, 'k-', lw=0.5)         # 원본
            ax.plot(x + 360, y, 'k-', lw=0.5)   # +360° 이동본

    ax.set_title(titles_map[idx], fontsize=12, loc='left', pad=1)
    axes_map.append(ax)

    for name, b in regions.items():
        lon_min, lon_max = b["lon"]
        lat_min, lat_max = b["lat"]
        # 래핑 구간 분할
        if lon_min <= lon_max:
            segments = [(lon_min, lon_max)]
        else:
            segments = [(lon_min, 360), (0, lon_max)]
        for seg_min, seg_max in segments:
            width  = seg_max - seg_min
            height = lat_max - lat_min
            rect = Rectangle(
                    (seg_min, lat_min),
                    width, height,
                    linewidth=1.5, edgecolor='black', facecolor='none',
                    linestyle=b["sty"],
                    )
            ax.add_patch(rect)

# ─── 4) 공통 컬러바 ─────────────────────────────────────────────
#cbar = fig.colorbar(im, ax=axes_map,
#        orientation='horizontal',
#        fraction=0.1, pad=0.2, shrink=0.6, aspect=50,
#        extendrect='True')

caxes = fig.add_axes([0.05,0.05,0.55,0.02])
cbar = plt.colorbar(im, cax=caxes, 
        ticks=cbar_list, 
        orientation='horizontal',extendrect='True')
cbar.ax.tick_params(labelsize=9, pad=0.5)

# ─── 5) 하단 시계열 4패널 ────────────────────────────────────────
titles_ts = [
        'c.',
        'd.',
        ]

fcst_scor = [
 fcst_jja_scor,
 fcst_djf_scor,
]

dyn_scor = [
 dyn_jja_scor,
 dyn_djf_scor,
]

trange = np.arange(years[0], years[-1]+1, 3)

#for idx, (r, c) in enumerate([(0,0), (1,0)]): ##org idx. position
for idx, (r, c) in enumerate([(0,1), (1,1)]):
    major_yticks = np.arange(0., 1+0.00001,0.2)
    minor_yticks = np.arange(-0.1,1+0.00001,0.1)
    ytick_labels = [str(np.round(i,2)) for i in major_yticks]
    ax = fig.add_subplot(gs[r, c:c+1])

    # 관측
    ax.plot(years, fcst_scor[idx], 'r-o', ms=5, lw=1.2, label='WeaCliM')
    ax.plot(years, dyn_scor[idx], 'b-x', ms=5, label=f'Dynamical model')
    ax.set_title(titles_ts[idx], fontsize=12, loc='left', pad=1)
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(-0.1, 1)
    ax.set_xticks(trange, trange,  rotation=30, fontsize=9)
    ax.tick_params(axis='x', which='major', pad=0.1)

    ax.set_yticks(major_yticks)
    ax.set_yticks(minor_yticks, minor = True)
    ax.set_yticklabels(ytick_labels, fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower left', prop={'size':6}, fontsize=8, ncol=2)

# ─── 6) 레이아웃 정리 및 출력 ────────────────────────────────────
#plt.tight_layout(h_pad=1.0, w_pad=0.5)
#plt.tight_layout(rect=[0,0.2,1,1])
fig.subplots_adjust(
        left=0.05, right=0.95,
        bottom=0.15, top=0.95,
        hspace=0.25, wspace=0.2
        )

#plt.show()

plt.savefig("Fig3.pdf", dpi=300, format="pdf", bbox_inches="tight")

# %%
