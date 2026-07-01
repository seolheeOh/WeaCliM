# %%
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import string
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.colors as mcolors

# 모델 이름 (9개 패널용)
titles = [
        "a.", "c.",
        "e.", "g.",
        "b.", "d.",
        "f.", "h."
        ]

st_yr = 2000
en_yr = 2019

ipath = '/home/seolhee_oh/proceeding/byol_weather/src/mk05_extremes_skill/data/'

fvar = np.zeros((2, 4, 29, 72))

for e, extrs in enumerate(['r95p_mm', 'r99p_mm', 'prcptot', 'rx1day']):

    f = Dataset(ipath+f'fcst_cor_apr_JJA_gpcp_{extrs}_2000-2019.nc','r')
    dat = f.variables['p'][:].squeeze()
    #dat[dat<0.5] = np.nan # for rmse
    fvar[0,e] = dat
    f.close()

    f = Dataset(ipath+f'avg.dyn_cor_may_JJA_gpcp_{extrs}_2000-2019.nc','r')
    dat = f.variables['p'][:].squeeze()
    #dat[dat<0.2] = np.nan # for rmse
    fvar[1,e] = dat
    f.close()

fvar = np.where(np.isclose(fvar, -9.99e+08, atol=1e5), np.nan, fvar)

#fvar = np.append(fvar, fvar[:,:,:8], axis=-1)

lon = np.linspace(-180, 180, 72)
lat = np.linspace(-70, 70, 29)
lon2d, lat2d = np.meshgrid(lon, lat)

# 그리드 설정
fig, axes = plt.subplots(
            4, 2, figsize=(8, 8),
                subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)}
                )

# 위도/경도 범위
lat_min, lat_max = -70, 70
lon_min, lon_max = -180, 179.9

cl=1
contour_levels = np.arange(-cl,cl+0.00000001,cl/10)
cbar_list = [-cl,-cl+2*(cl/10),-cl+4*(cl/10),-cl+6*(cl/10),-cl+8*(cl/10),cl-8*(cl/10),cl-6*(cl/10),cl-4*(cl/10),cl-2*(cl/10),cl]
ccols = plt.cm.get_cmap('RdBu_r')

norm = mcolors.BoundaryNorm(boundaries=contour_levels, ncolors=ccols.N, clip=True)

for i in range(4):
    ax = axes[i,0]
    alpha = string.ascii_lowercase[i]
    variable = fvar[0,i]
    title = titles[i]
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree(central_longitude=180))
    ax.coastlines(zorder=2,color='grey',linewidths=0.8)
    ax.set_xticks(np.arange(-180, 180+60, 60), crs = ccrs.PlateCarree(central_longitude=180))
    ax.set_yticks(np.arange(-70, 70+20, 20), crs = ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_title(f'{title}', fontsize=14, color='black',loc='left')
    contour = ax.pcolormesh(
            lon2d, lat2d, variable,
            cmap=ccols,
            norm = norm, # 컬러맵 이름 또는 객체
            shading='auto',       # 또는 'auto'
            transform=ccrs.PlateCarree(central_longitude=180)                                                                                       )
#    contour = ax.contourf(lon2d, lat2d, variable, contour_levels, 
#            extend='both', cmap=ccols, transform=ccrs.PlateCarree(central_longitude=180))

#caxes = fig.add_axes([0.06,0.07,0.4,0.02])
#cbar = plt.colorbar(contour, cax=caxes, ticks=cbar_list, orientation='horizontal',extendrect='True')
#cbar.ax.tick_params(labelsize=11)

#cl = 2
#contour_levels = np.arange(0.2,cl+0.00000001,cl/10)
#cbar_list = contour_levels
#cbar_list = [cl-10*(cl/10), cl-8*(cl/10),cl-6*(cl/10),cl-4*(cl/10),cl-2*(cl/10),cl]
#ccols = plt.cm.get_cmap('Reds')
#norm = mcolors.BoundaryNorm(boundaries=contour_levels, ncolors=ccols.N, clip=True)

for i in range(4):
    ax = axes[i,1]
    alpha = string.ascii_lowercase[i+4]
    variable = fvar[1,i]
    title = titles[i+4]
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree(central_longitude=180))
    ax.coastlines(zorder=2,color='grey',linewidths=0.8)
    ax.set_xticks(np.arange(-180, 180+60, 60), crs = ccrs.PlateCarree(central_longitude=180))
    ax.set_yticks(np.arange(-70, 70+20, 20), crs = ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_title(f'{title}', fontsize=14, color='black',loc='left')
    contour = ax.pcolormesh(
            lon2d, lat2d, variable,
            cmap=ccols,
            norm = norm, # 컬러맵 이름 또는 객체
            shading='auto',       # 또는 'auto'
            transform=ccrs.PlateCarree(central_longitude=180)                                                                                        )
#    contour = ax.contourf(lon2d, lat2d, variable, contour_levels, 
#            extend='both', cmap=ccols, transform=ccrs.PlateCarree(central_longitude=180))

caxes = fig.add_axes([0.08,0.04,0.85,0.02])
cbar = plt.colorbar(contour, cax=caxes, ticks=cbar_list, orientation='horizontal',extendrect='True')
cbar.ax.tick_params(labelsize=11)

# 간격 조절
plt.subplots_adjust(
        left=0.07, right=0.95,
        bottom=0.1, top=0.95,
        hspace=0.15, wspace=0.2
        )
#plt.tight_layout(rect=(0,0,1,1))
#plt.show()
plt.savefig("Extended_Fig7.pdf", dpi=300, format="pdf", bbox_inches="tight")


# %%
