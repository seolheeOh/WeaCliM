# %%
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import string

def minmax(x):
    return (x - x.min(axis=(-2,-1),keepdims=True)) / (x.max(axis=(-2,-1),keepdims=True) + 1e-8)

model = 'ref_CNN_daily'
model = 'BYOL'

lon = 125
lat = 35

#for model in ['BYOL']:
for model in ['ref_CNN_daily']:
#for model in ['BYOL', 'ref_CNN_daily']:

    ipath = '/home/seolhee_oh/proceeding/byol_weather/src/mk00_reconstruct_map/data/gradcam/'
    name = f'gradcam_heatmap_{model}_{lon}E_{lat}N_JJA_prcp_2000-2019'
    ds = xr.open_dataset(f"{ipath}/{name}.nc")
    print(ds)

    #20, 19, 10, 37, 72
    cam = ds["prcp"]

    cams_np = np.squeeze(cam.values)
#    cams_np = cams_np.reshape(20, 19, 10, 29, 72).mean((1,2))
    cams_np = cams_np.reshape(20, 10, 29, 72).mean(1)

#    mean = cams_np.mean(0, keepdims=True)
#    std = cams_np.std(0, keepdims=True)

#    cams_np = np.append(cams_np, mean,0)
#    cams_np = np.append(cams_np, std,0)
    cams_np = minmax(cams_np)

    n = cams_np.shape[0]
    cols = 4
    rows = int(np.ceil(n / cols))

    proj = ccrs.PlateCarree(central_longitude=180)

    fig, axes = plt.subplots(rows, cols, subplot_kw={'projection': proj}, figsize=(cols*3,rows*2))

#    fig, axes = plt.subplots(rows, cols, figsize=(cols*3, rows*3))
    axes = axes.flatten()

    # 공통 컬러스케일 설정 (0~1로 가정)
    vmin, vmax = 0, 1

    for i in range(n):
        lc = string.ascii_lowercase[i]
        ax = axes[i]
        im = ax.imshow(
                cams_np[i],
                origin='lower',
                cmap='jet',
                extent=(-180, 179.9, -70, 70),  # 위경도 범위 필수!
                transform=proj,
                vmin=vmin, vmax=vmax
                )
        ax.set_extent([0, 359, -70, 70], crs=proj)
        ax.set_title(f"{lc}.", fontsize=11, loc='left')
        #ax.set_title(f"{model} CAM Year {i+2000} ({lon}E-{lat}N)", fontsize=8)
        ax.coastlines(resolution='110m', color='black', linewidth=0.8)
        ax.axis("off")

    # 남은 칸은 비우기
    for j in range(i+1, len(axes)):
        axes[j].axis("off")

    # [left, bottom, width, height] : figure 좌표 (0~1)
    cax = fig.add_axes([0.05, 0.13, 0.9, 0.02])  # x,y,w,h
    fig.colorbar(im, cax=cax, orientation='horizontal')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
#plt.show()
plt.savefig("Extended_Fig4.pdf", dpi=300, format="pdf", bbox_inches="tight")


# %%
