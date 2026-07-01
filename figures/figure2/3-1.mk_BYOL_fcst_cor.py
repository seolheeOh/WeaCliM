import os, pathlib, sys
import numpy as np
from netCDF4 import Dataset

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from utils_src import cor, lonlat_to_grid

# Experiments #

for inp_month in ['apr', 'oct']:
    target_month = {
            'apr' : 'JJA',
            'jul' : 'SON',
            'oct' : 'DJF',
            'jan' : 'MAM'
            }.get(inp_month)

    oname = f'fcst_cor_{inp_month}_{target_month}_gpcp_2000-2019'
    opath = 'data/skills/'

    ipath = '../../Dataset/'
    f = Dataset(ipath+f'lab_{target_month}_gpcp_2000-2019.nc','r')
    lab = f.variables['prcp'][:]
    f.close()

    ipath = 'data/reconst/'
    f = Dataset(ipath+f'fcst_{inp_month}_{target_month}_gpcp_2000-2019.nc','r')
    fcst = f.variables['prcp'][:]
    f.close()

    x = np.mean(fcst, 1).squeeze()
    y = lab[:].squeeze()

    r = cor(x, y)
    r = np.array(r)

    r.astype('float32').tofile(opath+oname+'.gdat')
    
    g = open(opath+oname+'.ctl','w')
    g.write(
    'dset ^'+oname+'.gdat\n\
    undef -9.99e+08\n\
    xdef  72  linear   0.  5\n\
    ydef  29  linear -70.  5\n\
    zdef   1  linear 1 1\n\
    tdef   1  linear jan2008 1yr\n\
    vars   1\n\
    p      1     1    variable\n\
    ENDVARS\n'
    )
    g.close()
    
    os.system('cdo -f nc import_binary '+opath+oname+'.ctl '+opath+oname+'.nc')
    os.system('rm -f '+opath+oname+'.ctl '+opath+oname+'.gdat')

