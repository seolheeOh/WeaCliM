# %%
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import string
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.colors as mcolors

#target = 'JJA'
target = 'DJF'
if target == 'JJA':
    dl_month = 'apr'
    dyn_month = 'may'
else:
    dl_month = 'oct'
    dyn_month = 'nov'

# 모델 이름 (6개 패널용)
cor_titles = ["a.", "c.", "e."]
rmse_titles = ["b.","d.","f."]

cor = np.zeros((3, 29, 72))
rmse = np.zeros((3, 29, 72))

ipath = '/home/seolhee_oh/proceeding/byol_weather/src/mk02_compare_skill/data/'
f = Dataset(f'{ipath}/fcst_cor_{dl_month}_{target}_gpcp_2000-2019.nc','r')
cor[0] = f.variables['p'][0,0]
f.close()

f = Dataset(f'{ipath}/ref_cnn_monthly_cor_{dl_month}_{target}_gpcp_2000-2019.nc','r') #monthly
cor[1] = f.variables['p'][0,0]
f.close()

f = Dataset(f'{ipath}/avg.dyn_cor_{dyn_month}_{target}_gpcp_2000-2019.nc','r')
cor[2] = f.variables['p'][0,0]
f.close()

f = Dataset(f'{ipath}/fcst_rmse_{dl_month}_{target}_gpcp_2000-2019.nc','r')
rmse[0] = f.variables['p'][0,0]
f.close()

f = Dataset(f'{ipath}/ref_cnn_monthly_rmse_{dl_month}_{target}_gpcp_2000-2019.nc','r') #monthly
rmse[1] = f.variables['p'][0,0]
f.close()

#f = Dataset(f'{ipath}/avg.NMME_rmse_{dyn_month}_{target}_gpcp_2000-2019.nc','r')
f = Dataset(f'{ipath}/avg.dyn_rmse_{dyn_month}_{target}_gpcp_2000-2019.nc','r')
rmse[2] = f.variables['p'][0,0]
f.close()

#fvar = np.append(fvar, fvar[:,:,:8], axis=-1)

cor[cor==np.nan] = 0
rmse[rmse==np.nan] = 0
rmse[rmse<=0.2] = np.nan
#cor[cor<0.5] = np.nan

lon = np.linspace(-180, 180, 72)
lat = np.linspace(-70, 70, 29)
lon2d, lat2d = np.meshgrid(lon, lat)

# 그리드 설정
fig, axes = plt.subplots(
            3, 2, figsize=(10, 8),
                subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)},
                constrained_layout=True
                )

# 위도/경도 범위
lat_min, lat_max = -70, 70
lon_min, lon_max = -180, 179.9

# 내가 원하는 컬러 단계(levels)
cl=1
#ccols = plt.cm.get_cmap('Reds')
#contour_levels = np.arange(0, cl+0.001, cl/10)  # 10개 구간
contour_levels = np.arange(-cl, cl+0.001, cl/10)  # 10개 구간
c_levels = np.arange(-cl, cl+0.001, cl/5)  # 10개 구간
ccols = plt.cm.get_cmap('RdBu_r')

# BoundaryNorm 으로 levels에 맞춘 norm 생성
norm = mcolors.BoundaryNorm(boundaries=contour_levels, ncolors=plt.get_cmap('RdBu_r').N, clip=True)

for ax, variable, title  in zip(axes[:,0], cor, cor_titles):
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree(central_longitude=180))
    ax.coastlines(zorder=2,color='grey',linewidths=0.8)
    ax.set_xticks(np.arange(-180, 180+40, 50), crs = ccrs.PlateCarree(central_longitude=180))
    ax.set_yticks(np.arange(-70, 70+20, 20), crs = ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_title(f'{title}', fontsize=14, color='black',loc='left')
    contour = ax.pcolormesh(
            lon2d, lat2d, variable,
            cmap=ccols,
            norm = norm, # 컬러맵 이름 또는 객체
            shading='auto',       # 또는 'auto'
            transform=ccrs.PlateCarree(central_longitude=180)
            )

caxes = fig.add_axes([0.05,0.05,0.4,0.015])
cbar = plt.colorbar(contour, cax=caxes, ticks=c_levels, orientation='horizontal',extendrect='True')
cbar.ax.tick_params(labelsize=11)
cbar.set_ticklabels([f"{lv:.1f}" for lv in c_levels])

# 내가 원하는 컬러 단계(levels)
cl=3
ccols = plt.cm.get_cmap('Reds')
contour_levels = np.arange(0.2, cl+0.001, cl/10)  # 10개 구간

# BoundaryNorm 으로 levels에 맞춘 norm 생성
norm = mcolors.BoundaryNorm(boundaries=contour_levels, ncolors=plt.get_cmap('RdBu_r').N, clip=True)

for ax, variable, title in zip(axes[:,1], rmse, rmse_titles):
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree(central_longitude=180))
    ax.coastlines(zorder=2,color='grey',linewidths=0.8)
    ax.set_xticks(np.arange(-180, 180+40, 50), crs = ccrs.PlateCarree(central_longitude=180))
    ax.set_yticks(np.arange(-70, 70+20, 20), crs = ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_title(f'{title}', fontsize=14, color='black',loc='left')
    contour = ax.pcolormesh(
            lon2d, lat2d, variable,
            cmap=ccols,
            norm = norm, # 컬러맵 이름 또는 객체
            shading='auto',       # 또는 'auto'
            transform=ccrs.PlateCarree(central_longitude=180)
                                                                                        )
#    contour = ax.contourf(lon2d, lat2d, variable, contour_levels, 
#            extend='max', cmap=ccols, transform=ccrs.PlateCarree(central_longitude=180))

caxes = fig.add_axes([0.55,0.05,0.4,0.015])
cbar = plt.colorbar(contour, cax=caxes, ticks=contour_levels, orientation='horizontal',extendrect='True')
cbar.ax.tick_params(labelsize=11)
cbar.set_ticklabels([f"{lv:.1f}" for lv in contour_levels])

# 간격 조절
fig.subplots_adjust(
        left=0.05, right=0.95,
        bottom=0.1, top=0.95,
        hspace=0.25, wspace=0.2
        )
#plt.show()
plt.savefig("Extended_Fig2.pdf", dpi=300, format="pdf", bbox_inches="tight")

# %%
