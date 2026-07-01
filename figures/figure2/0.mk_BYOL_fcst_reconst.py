import os, pathlib, sys
import numpy as np
from netCDF4 import Dataset

# Ensemble
num_ens = 10

for inp_month in ['apr', 'oct']:
    target_month = {
            'apr': 'JJA',
            'jul': 'SON',
            'oct': 'DJF',
            'jan': 'MAM'
            }.get(inp_month)

    pr = np.zeros((20, 10, 1, 29, 72))
    for e, ens in enumerate(range(1,num_ens+1)):
        for i, lon in enumerate(range(0, 360, 5)):
            for j, lat in enumerate(range(-70, 75, 5)):

                ipath = f'../../Outputs/BYOL/Downstream_{inp_month}_GPCP/Main_{target_month}/'
                f = Dataset(f'{ipath}/fcst_day30_ens0{ens}_{lon}E_{lat}N.nc','r')
                fvar = f.variables['p'][:,0,0,0]
                f.close()

                pr[:, e, 0, j, i] = fvar[:]
                del fvar

    oname = f'fcst_{inp_month}_{target_month}_gpcp_2000-2019'
    opath = 'data/reconst/'

    pr.astype('float32').tofile(opath+oname+'.gdat')
    
    g = open(opath+oname+'.ctl','w')
    g.write(
    'dset ^'+oname+'.gdat\n\
    undef -9.99e+08\n\
    xdef   72  linear   0.  5\n\
    ydef   29  linear -70.  5\n\
    zdef   '+str(num_ens)+'  linear 1 1\n\
    tdef   20  linear jan2000 1yr\n\
    vars   1\n\
    prcp  '+str(num_ens)+'   '+str(num_ens)+'  variable\n\
    ENDVARS\n'
    )
    g.close()
    
    os.system('cdo -f nc import_binary '+opath+oname+'.ctl '+opath+oname+'.nc')
    os.system('rm -f '+opath+oname+'.ctl '+opath+oname+'.gdat')

