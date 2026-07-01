import torch
import numpy as np
import math
import os, pathlib, sys, argparse
from netCDF4 import Dataset

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils_src import grid_to_lonlat
from Model.finetuner import BYOLTuner

def train_model_for_grid(grid_i, grid_j, season, ens):

    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(1)
    print(f"Training on grid {grid_i} and {grid_j}")

    inp_month = {
            'JJA': 'apr',
            'SON': 'jul',
            'DJF': 'oct',
            'MAM': 'jan'
            }.get(season)

    #  Load training data______________________________
    inp = np.zeros((20, 4, 29, 72))
    ipath = '../Dataset/'
    f = Dataset(f'{ipath}/inp_daily_{inp_month}_2000-2019.nc','r')
    inp[:,0] = f.variables['t2m'][:].reshape(20, -1, 29, 72)[:, -1]
    inp[:,1] = f.variables['prcp'][:].reshape(20, -1, 29, 72)[:, -1]
    inp[:,2] = f.variables['u200'][:].reshape(20, -1, 29, 72)[:, -1]
    inp[:,3] = f.variables['u850'][:].reshape(20, -1, 29, 72)[:, -1]
    f.close()

    std = np.std(inp, 0, keepdims=True)
    inp = inp / (std+1e-8)
    inp = np.array(inp, dtype=np.float32)
    tdim, zdim, ydim, xdim = inp.shape[:]

    f = Dataset(f'{ipath}/lab_{season}_gpcp_2000-2019.nc','r')
    lab = f.variables['prcp'][:]
    f.close()

    lon, lat = grid_to_lonlat(grid_i, grid_j, 0, 5, -70, 5)
    print(f"Using LON: {lon}, LAT: {lat}")

    lab = lab[:,0, grid_j, grid_i]
    obs_std = np.std(lab, 0)
    lab /= np.std(lab, 0, keepdims=True)
    lab = np.array(lab, dtype=np.float32)

    # Dataset____________________________________________
    train_inp = np.zeros((20, 19, zdim, ydim, xdim))
    train_lab = np.zeros((20, 19, 1))

    for i in range(tdim):
        train_inp[i] = np.delete(inp, i, axis=0)
        train_lab[i] = np.delete(lab, i, axis=0).reshape(-1,1)

#    print('\n- Train :',train_inp.shape, '/', train_lab.shape)

    # Train__________________________________________________
    predictions = np.zeros((tdim))
    for i in range(tdim):
        target = str(i+2000)

        exp_path = f'../Outputs/BYOL/Pre_{inp_month}/'
        pre_opath = f'{exp_path}/{target}/ENS0{ens}/'

        exp_path = f'../Outputs/BYOL/Downstream_{inp_month}_GPCP/Main_{season}/'
        opath = f'{exp_path}/{target}/DAY30_ENS0{ens}_{lon}E_{lat}N/'
        pathlib.Path(opath).mkdir(parents=True, exist_ok=True)

        model = BYOLTuner(device=device, pre_opath=pre_opath, opath=opath, training=False)
        model.train([train_inp[i], train_lab[i]])

        del model
        torch.cuda.empty_cache()

        model = BYOLTuner(device=device, pre_opath=pre_opath, opath=opath, training=False)
        predictions[i] = model.test(inp[i:i+1]).cpu().numpy()

    del train_inp, train_lab, model

    predictions *= obs_std

    oname = f'fcst_day30_ens0{ens}_{lon}E_{lat}N'
    predictions.astype('float32').tofile(exp_path+oname+'.gdat')

    a = open(exp_path+oname+'.ctl','w')
    a.write(
    f'dset ^{oname}.gdat\n\
    undef -9.99e+08\n\
    xdef   1  linear   0.  2.5\n\
    ydef   1  linear -90.  2.5\n\
    zdef   1  linear 1 1\n\
    tdef   {tdim}  linear 00Z01jan2000 1yr\n\
    vars   1\n\
    p      1  99  regression\n\
    ENDVARS\n'
    )
    a.close()

    os.system('cdo -f nc import_binary '+exp_path+oname+'.ctl '+exp_path+oname+'.nc')
    os.system('rm -f '+exp_path+oname+'.ctl '+exp_path+oname+'.gdat')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BYOL Training Setup")
    parser.add_argument("--season", type=str, required=True, help="Target season")
    parser.add_argument("--ens", type=int, required=True, help="Ensemble index")
    parser.add_argument("--grid_i", type=int, required=True, help="Grid index in i direction")
    parser.add_argument("--grid_j", type=int, required=True, help="Grid index in j direction")
    args = parser.parse_args()

    train_model_for_grid(args.grid_i, args.grid_j, args.season, args.ens)


