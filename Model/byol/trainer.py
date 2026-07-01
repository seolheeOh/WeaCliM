import os, math, csv, sys
import torch
import torch.nn.functional as F

from .base import ConvNets
from .mlp_head import MLPHead
from torchinfo import summary

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils.data_loader import DataLoader

class BYOLTrainer:
    def __init__(self, device, opath):
        self.online_network = ConvNets().to(device)
        self.target_network = ConvNets().to(device)
        self.predictor = MLPHead(32, 32, 32).to(device)
        self.prev_target_weights = []
        self.optimizer = torch.optim.Adam(list(self.online_network.parameters()) 
                + list(self.predictor.parameters()), lr=0.001)
        self.device = device
        self.epochs = 100
        self.m = 0.99
        self.batch_size = 32
        self.opath = opath
        
    @torch.no_grad()
    def _update_target_network_parameters(self):
        for param_q, param_k in zip(self.online_network.parameters(), self.target_network.parameters()):
            param_k.data = param_k.data * self.m + param_q.data * (1. - self.m)
        self.prev_target_weights = [p.clone() for p in self.target_network.parameters()]  

    @torch.no_grad()
    def check_target_network_usage(self):
        for prev_weight, current_weight in zip(self.prev_target_weights, self.target_network.parameters()):
            if torch.equal(prev_weight, current_weight):
                print("Target network weights are consistent and in use.")
            else:
                print("Mismatch in target network weights.")

    @staticmethod
    def regression_loss(x, y):
        x = F.normalize(x, dim=1)
        y = F.normalize(y, dim=1)
        return 2 - 2 * (x * y).sum(dim=-1)

    def initializes_target_network(self):
        # init momentum network as encoder net
        for param_q, param_k in zip(self.online_network.parameters(), self.target_network.parameters()):
            param_k.data.copy_(param_q.data)  # initialize
            param_k.requires_grad = False  # not update by gradient
            
    def train(self, inp, num_pair):
        years, days, zdim, ydim, xdim = inp.shape[:]
        data = DataLoader(days, zdim, ydim, xdim)
        
        niter = 0
        
        self.initializes_target_network()

        train_view_1, train_view_2 = data.get_positive_pair(inp, num_pair)
        num_samples = len(train_view_1)

        loss_file_path = os.path.join(self.opath, 'loss_log.csv')
        with open(loss_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Epoch", "Loss"])
        
            for epoch in range(self.epochs):

                epoch_loss = 0 
                for i in range(math.ceil(num_samples/self.batch_size)):

                    batch_view_1 = torch.from_numpy(train_view_1).clone()
                    batch_view_2 = torch.from_numpy(train_view_2).clone()
                    
                    batch_view_1 = batch_view_1[self.batch_size*i:self.batch_size*(i+1)].to(self.device).float()
                    batch_view_2 = batch_view_2[self.batch_size*i:self.batch_size*(i+1)].to(self.device).float()

                    loss = self.update(batch_view_1, batch_view_2)

                    self.optimizer.zero_grad()
                    loss.backward()
                    self.optimizer.step()
                    self._update_target_network_parameters()  # update the key encoder
                    niter += 1

                    epoch_loss += loss.item()

                average_loss = epoch_loss / math.ceil(num_samples/self.batch_size)
                csv_writer.writerow([epoch + 1, average_loss])
                print(f"Epoch {epoch + 1}/{self.epochs}, Loss: {average_loss:.6f}")
                
            # save checkpoints
            self.save_model(os.path.join(self.opath, 'model.pth'))
            
    def update(self, batch_view_1, batch_view_2):
        # compute query feature
        predictions_from_view_1 = self.predictor(self.online_network(batch_view_1))
        predictions_from_view_2 = self.predictor(self.online_network(batch_view_2))
        
        # compute key features
        with torch.no_grad():
            targets_to_view_2 = self.target_network(batch_view_1)
            targets_to_view_1 = self.target_network(batch_view_2)
            
        loss = self.regression_loss(predictions_from_view_1, targets_to_view_1)
        loss += self.regression_loss(predictions_from_view_2, targets_to_view_2)
        return loss.mean()
    
    def save_model(self, PATH):
        
        torch.save({
            'online_network_state_dict': self.online_network.state_dict(),
            'target_network_state_dict': self.target_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            }, PATH)
