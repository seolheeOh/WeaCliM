import torch
import numpy as np
import math
import os, pathlib, sys, argparse
from netCDF4 import Dataset

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils_src import grid_to_lonlat
from Model.CNN import ConvNets
from Model.gradcam import GradCAM

def train_model_for_grid(grid_i, grid_j, ens):

    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(1)

    #  Load training data______________________________
    inp = np.zeros((20 * 30, 4, 29, 72))
    ipath = '../Dataset/'
    f = Dataset(f'{ipath}/inp_daily_apr_2000-2019.nc','r')
    inp[:,0] = f.variables['t2m'][:,0]
    inp[:,1] = f.variables['prcp'][:,0]
    inp[:,2] = f.variables['u200'][:,0]
    inp[:,3] = f.variables['u850'][:,0]
    f.close()

    std = np.std(inp[:20], axis=0, keepdims=True)
    inp = inp/(std + 1e-20)

    inp = inp.reshape(20, 30, 4, 29, 72)[:, -1]
    inp = np.array(inp, dtype=np.float32)
    tdim, zdim, ydim, xdim = inp.shape[:]

    lon, lat = grid_to_lonlat(grid_i, grid_j, 0, 5, -70, 5)

    # Inference______________________________________________
    heatmap = np.zeros((tdim, ydim, xdim))
    predictions = np.zeros((tdim))

    for i, target in enumerate(range(2000,2019+1)):
        exp_path = f'../Outputs/BYOL/Downstream_apr_GPCP/Main_JJA/'
        opath = f'{exp_path}/{target}/DAY30_ENS0{ens}_{lon}E_{lat}N/'

        inp_ = torch.from_numpy(inp[i:i+1]).float().to(device)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = ConvNets().to(device)
        ckpt = torch.load(
                os.path.join(opath, 'model.pth'),
                map_location=device
                )
        state = ckpt["BYOL_ConvNets"] if "BYOL_ConvNets" in ckpt else ckpt
        model.load_state_dict(state)

        Tool = GradCAM(model, 'conv2')

        heat_, pred_ = Tool(inp_)
        heatmap[i] = heat_.detach().numpy()
        predictions[i] = pred_.detach().numpy()

        del model, Tool

    tdim, ydim, xdim = heatmap.shape[:]

    save_path = f'../Outputs/BYOL_GradCam/Downstream_apr_GPCP/Main_JJA/'
    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

    oname = f'heatmap_day30_ens0{ens}_{lon}E_{lat}N'
    heatmap.astype('float32').tofile(save_path+oname+'.gdat')

    a = open(save_path+oname+'.ctl','w')
    a.write(
    'dset ^'+str(oname)+'.gdat\n\
    undef -9.99e+08\n\
    xdef   '+str(xdim)+'  linear   0.  5\n\
    ydef   '+str(ydim)+'  linear -70.  5\n\
    zdef   1  linear 1 1\n\
    tdef   '+str(tdim)+'  linear 00Z01jan2000 1yr\n\
    vars   1\n\
    p      1  1  regression\n\
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


