import torch, math, os, csv
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from torchinfo import summary

from .CNN import ConvNets

class BYOLTuner:
    def __init__(self, device, pre_opath, opath, training=True, output_dim=1):
        self.device = device
        self.pre_opath = pre_opath
        self.opath = opath
        self.model = ConvNets(output_dim).to(device)
        self.optimizer = torch.optim.Adam(self.model.parameters(),
                lr=0.001, betas=(0.9, 0.999), eps=1e-7)
        self.loss_fn = torch.nn.MSELoss()
        self.batch_size = 8
        self.epochs = 100

        checkpoint = torch.load(os.path.join(os.path.join(self.pre_opath, 'model.pth')),
                map_location=torch.device(torch.device(device)))
        
        with torch.no_grad():
            self.model.conv1.weight.copy_(checkpoint['online_network_state_dict']['conv1.weight'])
            self.model.conv1.bias.copy_(checkpoint['online_network_state_dict']['conv1.bias'])
            self.model.conv2.weight.copy_(checkpoint['online_network_state_dict']['conv2.weight'])
            self.model.conv2.bias.copy_(checkpoint['online_network_state_dict']['conv2.bias'])

        for param in self.model.parameters():
            param.requires_grad = True

        # It is needed to sensitivity test for generalization
        self.model.conv1.weight.requires_grad = training
        self.model.conv1.bias.requires_grad = training
        self.model.conv2.weight.requires_grad = training
        self.model.conv2.bias.requires_grad = training

#        print(self.model)
#        summary(self.model, input_size=(1, 4, 15, 72))

    def to_tensor(self, data):
        return torch.from_numpy(data).to(self.device).float()

    def train(self, train_dataset):
        self.model.train()

        inputs, labels = train_dataset
        num_samples = len(inputs)

        loss_file_path = os.path.join(self.opath, 'loss_log.csv')
        with open(loss_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Epoch", "Loss"])

            for epoch in range(self.epochs):

                epoch_loss = 0
                for i in range(math.ceil(num_samples/self.batch_size)):

                    batch_inputs = self.to_tensor(inputs[self.batch_size * i : self.batch_size * (i + 1)])
                    batch_labels = self.to_tensor(labels[self.batch_size * i : self.batch_size * (i + 1)])

                    outputs = self.model(batch_inputs)
                    loss = self.loss_fn(outputs, batch_labels)
                    
                    self.optimizer.zero_grad()
                    loss.backward()
                    self.optimizer.step()

                    epoch_loss += loss.item()

                average_loss = epoch_loss / math.ceil(num_samples / self.batch_size)
                csv_writer.writerow([epoch + 1, average_loss])
#                print(f"Epoch {epoch + 1}/{self.epochs}, Loss: {average_loss:.6f}")

            self.save_model(os.path.join(self.opath, 'model.pth'))

    def test(self, test_dataset):
        ##### new (25.12.30)
        self.model.eval()
        with torch.no_grad():
            self.load_model(self.opath)
            test_inp = self.to_tensor(test_dataset)
            outputs = self.model(test_inp)
        return outputs

    def save_model(self, PATH):
        torch.save({
            'BYOL_ConvNets':self.model.state_dict()
            }, PATH)

    def load_model(self, PATH):
        load_params = torch.load(os.path.join(os.path.join(PATH, 'model.pth')),
                map_location=torch.device(torch.device(self.device)))

        self.model.load_state_dict(load_params['BYOL_ConvNets'])
