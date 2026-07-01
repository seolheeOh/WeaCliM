import os, pathlib, sys
import numpy as np
from netCDF4 import Dataset
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from utils_src import cor, lonlat_to_grid

model_list = ['ECMWF', 'Meteo_France', 'ECCC', 'DWD', 
        'GFDL-CM2p5-FLOR-B01', 'GFDL-CM2p5-FLOR-A06', 'GFDL-CM2p1-aer04',
        'CCSM4', 'CanCM4i']

for target in ['JJA', 'DJF']:
    if target == 'JJA':
        inp_month = 'may'
    else :
        inp_month = 'nov'

    oname = f'avg.dyn_cor_{inp_month}_{target}_gpcp_2000-2019'
    opath = 'data/skills/'

    fcst = np.zeros((len(model_list),20,29,72))
    for m, model in enumerate(model_list) :
        if model in ['ECMWF', 'Meteo_France', 'ECCC', 'DWD']:
            folder = 'Dyn'
            iname = f'{model}_5x5_ano_{target}_prcp_{inp_month}_init_2000-2019.nc'
        else:
            folder = 'NMME'
            iname = f'{model}_ano_{target}_prcp_{inp_month}_init_2000-2019.nc'

        ipath = f'../../Dataset/{folder}/'
        f = Dataset(f'{ipath}/{iname}','r')
        fcst[m] = f.variables['prcp'][:].squeeze()
        f.close()

    ipath = '../../Dataset/'
    f = Dataset(ipath+f'lab_{target}_gpcp_2000-2019.nc','r')
    lab = f.variables['prcp'][:]
    f.close()

    fcst = np.where(fcst<-1e8, np.nan, fcst)

    lab = lab.squeeze()

    fcst = np.nanmean(fcst, 0)
    r = cor(fcst, lab)
    r = np.array(r)

    r.astype('float32').tofile(opath+oname+'.gdat')

    g = open(opath+oname+'.ctl','w')
    g.write(
    'dset ^'+oname+'.gdat\n\
    undef -9.99e+08\n\
    xdef  72  linear   0.  5\n\
    ydef  29  linear -70.  5\n\
    zdef   1  linear 1 1\n\
    tdef   1  linear jan2000 1yr\n\
    vars   1\n\
    p      1     99   variable\n\
    ENDVARS\n'
    )
    g.close()

    os.system('cdo -f nc import_binary '+opath+oname+'.ctl '+opath+oname+'.nc')
    os.system('rm -f '+opath+oname+'.ctl '+opath+oname+'.gdat')


    # %%
