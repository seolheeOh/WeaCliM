import torch
import numpy as np
import math
import os, pathlib, sys, argparse
from netCDF4 import Dataset

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   
sys.path.insert(0, str(ROOT))

from utils_src import grid_to_lonlat
from Model.extractfeature import ExtractFeature

def train_model_for_grid(grid_i, grid_j, ens):

    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(1)
#    print(f"Training on grid {grid_i} and {grid_j}")

    #  Load training data______________________________
    inp = np.zeros((20 * 30, 4, 29, 72))
    ipath = '../Dataset/'
    f = Dataset(f'{ipath}/inp_daily_apr_2000-2019.nc','r')
    inp[:,0] = f.variables['t2m'][:,0]
    f.close()

    inp = inp.reshape(20, 30, 4, 29, 72)[:, -10:]
    std = np.std(inp, 0, keepdims=True) 
    inp = inp/ ( std + 1e-20 )
    inp = np.array(inp, dtype=np.float32)
    tdim, day, zdim, ydim, xdim = inp.shape[:]

    lon, lat = grid_to_lonlat(grid_i, grid_j, 0, 5, -70, 5)
#    print(f"Using LON: {lon}, LAT: {lat}")

    # Dataset____________________________________________
    train_inp = np.zeros((20, 19, 10, zdim, ydim, xdim))
    
    for i in range(tdim):
        train_inp[i] = np.delete(inp, i, axis=0)
        
    train_inp = train_inp.reshape(20, -1, zdim, ydim, xdim)

    # Train__________________________________________________
    feature1 = np.zeros((tdim, (tdim-1)*day, 8, 15, 36))
    feature2 = np.zeros((tdim, (tdim-1)*day, 32, 8, 18))

    for i in range(tdim):
        target = str(i+2000)

        exp_path = f'../Outputs/BYOL/Downstream_apr_GPCP/Main_JJA/'
        opath = f'{exp_path}/{target}/DAY30_ENS0{ens}_{lon}E_{lat}N/'

        model = ExtractFeature(device, opath)
        out1, out2 = model.test(train_inp[i])
        feature1[i] = out1.cpu().numpy()
        feature2[i] = out2.cpu().numpy()

    del model

    save_path = '../Outputs/BYOL_feature/train_t2m/'
    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

    feature1 = feature1.reshape(-1, 8, 15, 36)
    data = np.array(feature1)

    oname = 'feature1_ens0'+str(ens)+'_'+str(lon)+'E_'+str(lat)+'N'
    data.astype('float32').tofile(save_path+oname+'.gdat')

    a = open(save_path+oname+'.ctl','w')
    a.write(
    'dset ^'+str(oname)+'.gdat\n\
    undef -9.99e+08\n\
    xdef   36 linear   0.  2.5\n\
    ydef   15 linear -90.  2.5\n\
    zdef   8  linear 1 1\n\
    tdef   '+str(tdim*(tdim-1)*day)+'  linear 00Z01jan2000 1yr\n\
    vars   1\n\
    p      8  8  regression\n\
    ENDVARS\n'
    )
    a.close()

    os.system('cdo -f nc import_binary '+save_path+oname+'.ctl '+save_path+oname+'.nc')
    os.system('rm -f '+save_path+oname+'.ctl '+save_path+oname+'.gdat')

    feature2 = feature2.reshape(-1, 32, 8, 18)
    data = np.array(feature2)

    oname = 'feature2_ens0'+str(ens)+'_'+str(lon)+'E_'+str(lat)+'N'
    data.astype('float32').tofile(save_path+oname+'.gdat')

    a = open(save_path+oname+'.ctl','w')
    a.write(
    'dset ^'+str(oname)+'.gdat\n\
    undef -9.99e+08\n\
    xdef   18 linear   0.  2.5\n\
    ydef   8  linear -90.  2.5\n\
    zdef   32 linear 1 1\n\
    tdef   '+str(tdim*(tdim-1)*day)+'  linear 00Z01jan2000 1yr\n\
    vars   1\n\
    p      32 32 regression\n\
    ENDVARS\n'
    )
    a.close()

    os.system('cdo -f nc import_binary '+save_path+oname+'.ctl '+save_path+oname+'.nc')
    os.system('rm -f '+save_path+oname+'.ctl '+save_path+oname+'.gdat')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BYOL Training Setup")
    parser.add_argument("--ens", type=int, required=True, help="Ensemble index")
    parser.add_argument("--grid_i", type=int, required=True, help="Grid index in i direction")
    parser.add_argument("--grid_j", type=int, required=True, help="Grid index in j direction")
    args = parser.parse_args()

    train_model_for_grid(args.grid_i, args.grid_j, args.ens)

