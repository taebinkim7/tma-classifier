import torch.nn as nn
import torch
import torchvision.models as models

from efficientnet_pytorch import EfficientNet


def load_cnn_model(pretrained_model='vgg16'):
    """
    Loads the CNN feature extraction model used in the paper.
    Global mean pool of last convolutional layer of pre-trained model.
    """
    if pretrained_model == 'vgg16':
        model = models.vgg16(pretrained=True).features.double()
    elif pretrained_model == 'efficientnet-b7':
        model = EfficientNet.from_pretrained('efficientnet-b7')
    model = append_to_sequential(model, GlobalMeanPool2D())

    return model


def reshape2D(x):
    """
    Reshapes x from (batch, channels, H, W) to (batch, channels, H * W)
    """
    return x.view(x.size(0), x.size(1), -1)


class GlobalMeanPool2D(nn.Module):
    def forward(self, x):
        return torch.mean(reshape2D(x), dim=2)


def append_to_sequential(net, mod):
    net_list = [net, mod]
    # net_list = list(net)
    # net_list.append(mod)
    return nn.Sequential(*net_list)
