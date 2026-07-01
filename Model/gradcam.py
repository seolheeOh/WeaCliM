import torch, math, os, csv
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from torchinfo import summary

def get_module_by_name(model, name: str):
    for n, m in model.named_modules():
        if n == name:
            return m
    raise ValueError(f"No module named {name}")

class GradCAM:
    def __init__(self, model, target_layer_name: str):
        self.model = model.eval()
        self.activations = None
        self.gradients = None

        layer = get_module_by_name(self.model, target_layer_name)

        def fwd_hook(module, inp, out):
            self.activations = out

        def bwd_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0]

        self.handle_fwd = layer.register_forward_hook(fwd_hook)
        self.handle_bwd = layer.register_full_backward_hook(bwd_hook)

    def _minmax(self, x, eps=1e-8):
        x_min = x.amin(dim=(-2,-1), keepdim=True)
        x_max = x.amax(dim=(-2,-1), keepdim=True)
        return (x - x_min) / (x_max - x_min).clamp_min(eps)

    def __call__(self, x):
        B, _, H, W = x.shape

        self.model.zero_grad(set_to_none=True)
        self.activations = None
        self.gradients = None

        with torch.enable_grad():
            y_pred = self.model(x)

            s = y_pred.sum()
            s.backward(retain_graph=False)
            if self.gradients is None or self.activations is None:
                raise RuntimeError("Grad-CAM hooks did not capture gradients/activations. "
                        "Check target_layer, no_grad, detach, and scalar target.")

            
            A = self.activations
            G = self.gradients
            w = G.mean(dim=(-2,-1), keepdim=True)
            cam = (w * A).sum(dim=1, keepdim=True)
            cam = torch.nn.functional.relu(cam)

            cam = F.interpolate(cam, size=(H,W), mode="bilinear", align_corners=False)
            cam = self._minmax(cam).squeeze(1)

        return cam, y_pred.detach()


    def save_model(self, PATH):
        torch.save({
            'BYOL_ConvNets':self.model.state_dict()
            }, PATH)

