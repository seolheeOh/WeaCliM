import torch
import numpy as np
import math
import os, pathlib, sys, argparse
from netCDF4 import Dataset
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Model.byol.trainer import BYOLTrainer

def train_model(inp_month, ens):

    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(3)

    #  Load training data______________________________
    inp = np.zeros((20, 10, 4, 29, 72))
    ipath = '../Dataset/'
    f = Dataset(f'{ipath}/inp_daily_{inp_month}_2000-2019.nc','r')
    inp[:,:,0] = f.variables['t2m'][:,0].reshape(20, -1, 29, 72)[:, -10:]
    inp[:,:,1] = f.variables['prcp'][:,0].reshape(20, -1, 29, 72)[:, -10:]
    inp[:,:,2] = f.variables['u200'][:,0].reshape(20, -1, 29, 72)[:, -10:]
    inp[:,:,3] = f.variables['u850'][:,0].reshape(20, -1, 29, 72)[:, -10:]
    f.close()

#    print(inp[0,0,0])

    zdim, ydim, xdim = inp.shape[-3:]
    std = np.std(inp, 0, keepdims=True)
    inp = inp / (std + 1e-20)
    inp = np.array(inp, dtype=np.float32)

    # Dataset____________________________________________
    train_inp = np.zeros((20, 19, 10, 4, 29, 72))

    for i in range(len(inp)):
        train_inp[i] = np.delete(inp, i, axis=0)

    # Pre-Train_____________________________________________
    for i in range(len(inp)):
        target = str(i+2000)

        exp_path = f'../Outputs/BYOL/Pre_{inp_month}/'
        opath = f'{exp_path}/{target}/ENS0{ens}/'
        pathlib.Path(opath).mkdir(parents=True, exist_ok=True)

        model = BYOLTrainer(device, opath)
        model.train(train_inp[i], 40)

        del model
        torch.cuda.empty_cache()

    del train_inp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BYOL Pre-training Setup")
    parser.add_argument("--inp_month", type=str, required=True, help="Train month")
    parser.add_argument("--ens", type=int, required=True, help="Ensemble index")
    args = parser.parse_args()

    train_model(args.inp_month, args.ens)

