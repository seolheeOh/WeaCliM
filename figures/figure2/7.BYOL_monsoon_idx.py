import os, pathlib, sys
import numpy as np
from netCDF4 import Dataset

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from utils_src import aave

for season in ['JJA', 'DJF']:
    if season == 'JJA':
        inp_month = 'apr'
    else :
        inp_month = 'oct'

    for area in ['IN', 'EA', 'NAF', 'NAM', 'SAM', 'SAF']:
        area_bounds = {
                'IN':  ( 70, 105,  10,  30),
                'EA':  (110, 135, 22.5, 45),
                'NAM': (250, 280,  7.5, 22.5),
                'NAF': (330, 390,  5,   15),
                'SAM': (290, 320, -25,  -5),
                'SAF': ( 25,  70,  7.5, 25),
                }
        try:
            print(area)
            lon_st, lon_en, lat_st, lat_en = area_bounds[area]
            
        except KeyError:
            raise ValueError(f"error for: {area}")

        ipath = 'data/reconst/'
        fname = f'fcst_{inp_month}_{season}_gpcp_2000-2019.nc'

        f = Dataset(ipath+fname, 'r')
        data = f.variables['prcp'][:].squeeze()

        #ensemble mean
        data = np.mean(data, 1)

        app_dat = np.concatenate([data, data], -1)

        avg = aave(app_dat, lon_st, lon_en, lat_st, lat_en, 0, 5, -70, 5)
        avg /= np.std(avg, 0)
        avg = np.array(avg)

        opath = 'data/monsoon_idx/'

        oname = f'fcst_{inp_month}_{season}_gpcp_{area}_2000-2019'
        avg.astype('float32').tofile(opath+oname+'.gdat')

        g = open(opath+oname+'.ctl','w')
        g.write(
        'dset ^'+oname+'.gdat\n\
        undef -9.99e+08\n\
        xdef   1  linear   0.  5\n\
        ydef   1  linear -30.  5\n\
        zdef   1  linear 1 1\n\
        tdef   20  linear jan2000 1yr\n\
        vars   1\n\
        p    1     1    variable\n\
        ENDVARS\n'
        )
        g.close()

        os.system('cdo -f nc import_binary '+opath+oname+'.ctl '+opath+oname+'.nc')
        os.system('rm -f '+opath+oname+'.ctl '+opath+oname+'.gdat')
