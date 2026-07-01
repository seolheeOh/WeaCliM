from netCDF4 import Dataset
import numpy as np
import os

def scorr (dat1, dat2):
    if dat1.ndim > 2 :
        tdim = len(dat1)
    else :
        tdim = 1

    data1 = dat1 - np.nanmean(dat1, (-1, -2), keepdims=True)
    data2 = dat2 - np.nanmean(dat2, (-1, -2), keepdims=True)

    xx = np.nanmean(data1*data1, (-1,-2))
    yy = np.nanmean(data2*data2, (-1,-2))
    xy = np.nanmean(data1*data2, (-1,-2))

    cor = xy / np.sqrt(xx*yy)
    cor = cor.reshape(tdim)

    return cor

def cor (idx1, idx2):

    idx1 = idx1-np.nanmean(idx1,axis=0)
    idx2 = idx2-np.nanmean(idx2,axis=0)

    xx = np.nanmean(idx1*idx1,axis=0)
    yy = np.nanmean(idx2*idx2,axis=0)
    xy = np.nanmean(idx1*idx2,axis=0)

    cor = xy/(np.sqrt(xx*yy)+1e-20)

    return cor

def rmse (idx1, idx2):
    diff = (idx1 - idx2)**2
    mask = np.isfinite(idx1) & np.isfinite(idx2)
    diff_valid = np.where(mask, diff, 0.0)
    sse = diff_valid.sum(axis=0)
    cnt = mask.sum(axis=0)
    mse = np.divide(sse, cnt, out=np.full_like(sse, np.nan, dtype=float), where=cnt>0)
    rmse = np.sqrt(mse)

    return rmse

def mse (idx1, idx2):

    mse = np.nanmean(pow(idx1-idx2,2),0)
    mse = np.array(mse)

    return mse

def grid_to_lonlat(x, y,
        lon_init=0.0, lon_int=5,
        lat_init=-90.0, lat_int=5,
        center=False):
    if center:
        lon = lon_init + (x + 0.5) * lon_int
        lat = lat_init + (y + 0.5) * lat_int
        
    else:
        lon = lon_init + x * lon_int
        lat = lat_init + y * lat_int
        
    return lon, lat

def lonlat_to_grid(lon, lat,
        lon_init=0.0, lon_int=5,
        lat_init=-90.0, lat_int=5):

    x = int(np.floor((lon - lon_init) / lon_int))
    y = int(np.floor((lat - lat_init) / lat_int))

    if x < 0 or y < 0:
        raise ValueError(f"좌표 ({lon}, {lat})가 격자 시작점보다 작습니다.")

#    x = int( ( ( lon - lon_init ) / lon_int ) )
#    y = int( ( lat - lat_init ) / lat_int )

    return x, y
    
def aave(dat, lon_st, lon_nd, lat_st, lat_nd,
        lon_init=0.0,  lon_int=2.5,
        lat_init=-90.0, lat_int=2.5,
        equal_area_treat=True, fill_value=-9.99e+08):
    
    print(lon_init, lon_int, lat_init, lat_int)

    # get dimension
    o_dim = dat.shape[:-2]
    ydim, xdim = dat.shape[-2:]

    x_st = int( ( ( lon_st - lon_init ) / lon_int ) )
    x_nd = int( ( ( lon_nd - lon_init ) / lon_int ) + 1)
    y_st = int( ( lat_st - lat_init ) / lat_int )
    y_nd = int( ( ( lat_nd - lat_init ) / lat_int ) + 1 )
    
    n_dim = len(dat.shape)
    
    if n_dim < 2:
        print('The input must be at least two-dimensional.')
        
    # crop
    dat = dat.reshape(-1,ydim,xdim)
    crop = dat[:,y_st:y_nd,x_st:x_nd]
   
    # get crop dimension       
    ydim2, xdim2 = crop.shape[1:]
    n_grid = crop.shape[1] * crop.shape[2]
    
    # mask missing values
    crop = np.ma.masked_equal(crop, fill_value)
    crop = np.ma.masked_where(np.isclose(crop, fill_value, atol=1e-3), crop)
    
    if equal_area_treat == True:
        # make latitude list
        lat_list = np.arange(lat_st,lat_st+lat_int*(ydim2), lat_int)
        # cosine theta
        weight = np.cos(np.deg2rad(lat_list))
        weight = weight.reshape(ydim2, 1)
        weight = np.expand_dims(np.repeat(weight, xdim2, axis=1), axis=0)
        
        # mask missing values
#        weight[crop[0].mask==True] = fill_value
        weight = np.ma.masked_equal(weight, fill_value)
        
        crop = np.nansum(crop*weight,axis=(1,2))/np.nansum(weight,axis=(1,2))
        
        if len(crop.shape) == 1 and crop.shape[0] == 1:   
            crop = np.array(crop)
        else:
            crop = crop.reshape(o_dim)
    else :
        crop = np.nanmean(crop,axis=(1,2))


    return crop



