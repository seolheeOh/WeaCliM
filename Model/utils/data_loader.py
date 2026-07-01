import numpy as np
import os, pathlib
import math

class DataLoader(object):
    def __init__(self, dydim, zdim, ydim, xdim):

        self.dydim, self.zdim, self.ydim, self.xdim = dydim, zdim, ydim, xdim

    def get_positive_pair(self, inp, num_pair):

        inp = inp.reshape(-1, self.dydim, self.zdim, self.ydim, self.xdim) # year, day, x, y, z
        years = inp.shape[0]

        pair_inp = np.zeros((years, num_pair * 2, self.zdim, self.ydim, self.xdim))
        for i in range(years): 
            rd_view = []
            while len(rd_view) < (num_pair * 2):
                rd_view.append(np.random.choice(self.dydim, self.dydim, replace=False))
            rd = np.array(rd_view).reshape(-1)[:num_pair*2]
            pair_inp[i] = np.array(inp)[i, rd]

        pair_inp = pair_inp.reshape(years*num_pair, 2, self.zdim, self.ydim, self.xdim)

        view_1 = pair_inp[:,0]
        view_2 = pair_inp[:,1]

        return [view_1, view_2]

