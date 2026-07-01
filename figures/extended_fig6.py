# %%
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
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

fname = f'combine_reg_JJA_labPC_labprcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
obs_jja = ds['ev1']
obs_jja = obs_jja.where(obs_jja != 0)

fname = f'combine_reg_apr_JJA_labPC_fcstprcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
fcst_jja = ds['ev1']
fcst_jja = fcst_jja.where(fcst_jja != 0)

fname = f'combine_reg_may_JJA_labPC_avg.dynprcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
nmme_jja = ds['ev1']
nmme_jja = nmme_jja.where(nmme_jja != 0)

jja_maps = [
        obs_jja, fcst_jja, nmme_jja
        ]

fname = f'combine_reg_DJF_labPC_labprcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
obs_djf = ds['ev1']
obs_djf = obs_djf.where(obs_djf != 0)

fname = f'combine_reg_oct_DJF_labPC_fcstprcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
fcst_djf = ds['ev1']
fcst_djf = fcst_djf.where(fcst_djf != 0)

fname = f'combine_reg_nov_DJF_labPC_avg.dynprcp_2000-2019.nc'
ds = xr.open_dataset(ipath + fname)
nmme_djf = ds['ev1']
nmme_djf = nmme_djf.where(nmme_djf != 0)

djf_maps = [
        obs_djf, fcst_djf, nmme_djf
        ]

# ─── 2) Figure & Projection 셋업 ─────────────────────────────────
fig = plt.figure(figsize=(10,  7))
gs = GridSpec(nrows=3, ncols=2, figure=fig,
        height_ratios=[1, 1, 1],
        width_ratios=[1, 1],
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
        f'c.',
        f'e.',
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
for idx, (r, c) in enumerate([(0,0), (1,0), (2,0)]):
    ax = fig.add_subplot(gs[r, c:c+1])

    da = jja_maps[idx].squeeze()            # ← 여기서 꺼내기
    values = da.values.squeeze()

    ax.set_xticks(np.arange(120, 160+360+30, 50))
    ax.set_yticks(np.arange(-90, 90+20, 20))
#    ax.set_extent([120, 160+359.9,-40,45], crs=proj)
    ax.set_xlim(120, 360+160)
    ax.set_ylim(-55, 55+5)
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
                    )
            ax.add_patch(rect)

# ─── 4) 공통 컬러바 ─────────────────────────────────────────────
caxes = fig.add_axes([0.05,0.05,0.9,0.015])
cbar = plt.colorbar(im, cax=caxes, 
        ticks=cbar_list, 
        orientation='horizontal',extendrect='True')
cbar.ax.tick_params(labelsize=9, pad=0.5)

# ─── 5) 하단 시계열 4패널 ────────────────────────────────────────
titles_ts = [
        f'b.',
        f'd.',
        f'f.',
        ]

axes_map = []
for idx, (r, c) in enumerate([(0,1), (1,1), (2,1)]):
    ax = fig.add_subplot(gs[r, c:c+1])

    da = djf_maps[idx].squeeze()            # ← 여기서 꺼내기
    values = da.values.squeeze()

    ax.set_xticks(np.arange(120, 160+360+30, 50))
    ax.set_yticks(np.arange(-90, 90+20, 20))
#    ax.set_extent([120, 160+359.9,-40,45], crs=proj)
    ax.set_xlim(120, 360+160)
    ax.set_ylim(-55, 55+5)
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

    ax.set_title(titles_ts[idx], fontsize=12, loc='left', pad=1)
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
                    )
            ax.add_patch(rect)

# ─── 6) 레이아웃 정리 및 출력 ────────────────────────────────────
#plt.tight_layout(h_pad=1.0, w_pad=0.5)
#plt.tight_layout(rect=[0,0.2,1,1])
fig.subplots_adjust(
        left=0.05, right=0.95,
        bottom=0.13, top=0.95,
        hspace=0.25, wspace=0.2
        )
#plt.show()
plt.savefig("Extended_Fig6.pdf", dpi=300, format="pdf", bbox_inches="tight")
# %%
