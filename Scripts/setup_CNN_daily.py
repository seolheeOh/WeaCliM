import torch
import numpy as np
import math
import os, pathlib, sys, argparse
from netCDF4 import Dataset
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils_src import grid_to_lonlat
from Model.trainer import ReferenceCNN

def train_model_for_grid(grid_i, grid_j, season, ens):

    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(2)
    print(f"Training on grid {grid_i} and {grid_j}")

    inp_month = {
            'JJA': 'apr',
            'SON': 'jul',
            'DJF': 'oct',
            'MAM': 'jan'
            }.get(season)

    #  Load training data______________________________
    inp = np.zeros((20, 10, 4, 29, 72))
    ipath = '../Dataset/'
    f = Dataset(ipath+f'inp_daily_{inp_month}_2000-2019.nc','r')
    inp[:,:,0] = f.variables['t2m'][:,0].reshape(20, -1, 29, 72)[:,-10:]
    inp[:,:,1] = f.variables['prcp'][:,0].reshape(20, -1, 29, 72)[:,-10:]
    inp[:,:,2] = f.variables['u200'][:,0].reshape(20, -1, 29, 72)[:,-10:]
    inp[:,:,3] = f.variables['u850'][:,0].reshape(20, -1, 29, 72)[:,-10:]
    f.close()

    inp /= (np.std(inp, 0, keepdims=True) + 1e-20)
    inp = np.array(inp, dtype=np.float32)
    tdim, day, zdim, ydim, xdim = inp.shape[:]

    f = Dataset(ipath+f'lab_{season}_gpcp_2000-2019.nc','r')
    lab = f.variables['prcp'][:]
    f.close()

    # augmentation * 10days
    lab = np.repeat(lab, repeats=10, axis=1)

    lon, lat = grid_to_lonlat(grid_i, grid_j, 0, 5, -70, 5)
    print(f"Using LON: {lon}, LAT: {lat}")

    # 20, 10, 1, 1
    lab = lab[:,:, grid_j, grid_i]
    std = np.std(lab, (0,1), keepdims=True)
    lab /= (std + 1e-20)
    lab = np.array(lab, dtype=np.float32)

    # Dataset____________________________________________
    train_inp = np.zeros((20, 19, 10, zdim, ydim, xdim))
    train_lab = np.zeros((20, 19, 10))

    for i in range(tdim):
        train_inp[i] = np.delete(inp, i, axis=0)
        train_lab[i] = np.delete(lab, i, axis=0)

    train_inp = train_inp.reshape(20, -1, zdim, ydim, xdim)
    train_lab = train_lab.reshape(20, -1, 1) 

    print('\n- Train :',train_inp.shape, '/', train_lab.shape)

    # Train__________________________________________________
    predictions = np.zeros((tdim, day, 1))
    for i in range(tdim):
        target = str(i+2000)

        exp_path = f'../Outputs/ref_CNN_daily/Main_{inp_month}_{season}/'
        opath = exp_path+'/'+target+'/ENS0'+str(ens)+'_'+str(lon)+'E_'+str(lat)+'N/'
        pathlib.Path(opath).mkdir(parents=True, exist_ok=True)

        model = ReferenceCNN(device=device, opath=opath)
        model.train([train_inp[i], train_lab[i]])

        del model
        torch.cuda.empty_cache()

        model = ReferenceCNN(device=device, opath=opath)
        predictions[i] = model.test(inp[i]).cpu().numpy()
        del model

    del train_inp, train_lab

    predictions *= (std + 1e-20)
    predictions = predictions.reshape(-1)

    oname = 'fcst_ens0'+str(ens)+'_'+str(lon)+'E_'+str(lat)+'N'
    predictions.astype('float32').tofile(exp_path+oname+'.gdat')

    a = open(exp_path+oname+'.ctl','w')
    a.write(
    'dset ^'+str(oname)+'.gdat\n\
    undef -9.99e+08\n\
    xdef   1  linear   0.  2.5\n\
    ydef   1  linear -90.  2.5\n\
    zdef   1  linear 1 1\n\
    tdef   '+str(tdim*day)+'  linear 00Z01jan2000 1yr\n\
    vars   1\n\
    p      1  1  regression\n\
    ENDVARS\n'
    )
    a.close()

    os.system('cdo -f nc import_binary '+exp_path+oname+'.ctl '+exp_path+oname+'.nc')
    os.system('rm -f '+exp_path+oname+'.ctl '+exp_path+oname+'.gdat')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BYOL Training Setup")
    parser.add_argument("--ens", type=int, required=True, help="Ensemble index")
    parser.add_argument("--season", type=str, required=True, help="Target season")
    parser.add_argument("--grid_i", type=int, required=True, help="Grid index in i direction")
    parser.add_argument("--grid_j", type=int, required=True, help="Grid index in j direction")
    args = parser.parse_args()

    train_model_for_grid(args.grid_i, args.grid_j, args.season, args.ens)


