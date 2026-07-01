import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F

class ConvNets(nn.Module):
    def __init__(self, output_dim = 1):
        super(ConvNets, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=4, out_channels=8, kernel_size=3, stride=2, padding=1)
        self.act1 = nn.Tanh()

        self.conv2 = nn.Conv2d(in_channels=8, out_channels=32, kernel_size=3, stride=2, padding=1)
        self.act2 = nn.Tanh()
        self.drop2 = nn.Dropout(p=0.2)

        self.flatten = nn.Flatten()
#        self.outputs = nn.Linear(2304, 1)
        self.outputs = nn.Linear(4608, output_dim)

        self.apply(self.initialize_weights)

    def initialize_weights(slef, m):
        if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
            init.xavier_uniform_(m.weight)

    def forward(self, x):
        z = self.conv1(x)
        z = self.act1(z)

        z = self.conv2(z)
        z = self.act2(z)
        z = self.drop2(z)

        z = self.flatten(z)
        return self.outputs(z)
