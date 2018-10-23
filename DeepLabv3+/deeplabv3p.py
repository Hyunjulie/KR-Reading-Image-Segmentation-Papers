import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
import tqdm 

https://lijiancheng0614.github.io/2018/02/27/2018_02_27_DeepLab-v3+/
#Modified Aligned Xception 
class Xception(nn.Module):
	def __init__(self, inplanes=3, os=16, pretrained=False):
		super(Xception,self).__init__()

		if os == 16: 
			entry_block3_stride = 2
			middle_block_rate = 1
			exit_block_rates = (1,2)
		elif os == 8: 
			entry_block3_stride = 1 
			middle_block_rate =2 
			exit_block_rates = (2,4)
		else: 
			raise NotImplementedError

		#Entry flow 
		self.conv1 = nn.Conv2d(inplanes, 32, 3, strides=2, padding=1, bias=False)
		self.bn1 = nn.Batchnorm2d(32)
		self.relu = nn.ReLU(inplace =True)
		self.conv2 = nn.Conv2d(32, 64, 3, strides=1, padding=1, bias=False)
		self.bn1 = nn.Batchnorm2d(64)

		self.block1 = Block()






https://github.com/JamesTonG321/pytorch-deeplab-xception/blob/master/networks/deeplab_xception.py






q


















