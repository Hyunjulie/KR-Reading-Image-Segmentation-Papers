import torch
import torch.nn as nn
from segnet_utils import *
from torchvision import models
import numpy as np 
np.random.seed(777)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#CamVid road scene data - 11 classes, RGB, 
class segnet(nn.Module):
	def __init__(self, num_classes=11, in_channels=3, is_unpooling=True):
		super(segnet, self).__init__()
		self.in_channels = in_channels
		self.is_unpooling = is_unpooling
		self.down1 = Down_2conv(self.in_channels, 64)
		self.down2 = Down_2conv(64, 128)
		self.down3 = Down_3conv(128, 256)
		self.down4 = Down_3conv(256, 512)
		self.down5 = Down_3conv(512, 512)

		self.up5 = Up_3conv(512, 512)
		self.up4 = Up_3conv(512, 256)
		self.up3 = Up_3conv(256, 128)
		self.up2 = Up_3conv(128, 64)
		self.up1 = Up_3conv(64, num_classes)

	def forward(self, inputs):
		down1, indices_1, shape1 = self.down1(inputs)
		down2, indices_2, shape2 = self.down2(down1)
		down3, indices_3, shape3 = self.down3(down2)
		down4, indices_4, shape4 = self.down4(down3)
		down5, indices_5, shape5 = self.down5(down4)

		up5 = self.up5(down5, indices_5, shape5)
		up4 = self.up4(up5, indices_4, shape4)
		up3 = self.up3(up4, indices_3, shape3)
		up2 = self.up2(up3, indices_2, shape2)
		up1 = self.up1(up2, indices_1, shape1)
		return up1

# credits to meetshah1995 
	def init_vgg16_params(self, vgg16):
		blocks = [self.down1, self.down2, self.down3, self.down4, self.down5]
		ranges = [[0, 4], [5, 9], [10, 16], [17, 23], [24, 29]]
		features = list(vgg16.features.children())
		vgg_layers = []
		for _layer in features:
			if isinstance(_layer, nn.Conv2d):
				vgg_layers.append(_layer)
		merged_layers = []
		for idx, conv_block in enumerate(blocks):
			if idx < 2:
				units = [conv_block.conv1.cbr_unit, conv_block.conv2.cbr_unit]
			else:
				units = [
					conv_block.conv1.cbr_unit, 
					conv_block.conv2.cbr_unit,
					conv_block.conv3.cbr_unit]
			for _unit in units: 
				for _layer in _unit: 
					if isinstance(_layer, nn.Conv2d):
						merged_layers.append(_layer)
		assert len(vgg_layers) ==len(merged_layers)

		for l1, l2 in zip(vgg_layers, merged_layers):
			if isinstance(l1, nn.Conv2d) and isinstance(l2, nn.Conv2d):
				assert l1.weight.size() == l2.weight.size()
				assert l1.bias.size() == l2.bias.size()
				l2.weight.data = l1.weight.data
				l2.bias.data = l1.bias.data


model = segnet()

