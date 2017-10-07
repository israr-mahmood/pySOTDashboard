from pySOT import *

class surrogate_models:
	def __init__(self,parsed_json):
		self.parsed_json = parsed_json
		self.kernel_dict = {'CubicKernel' : CubicKernel}
		self.tail_dict = {'LinearTail' : LinearTail}

	def run(self):
		if self.parsed_json['function'] == 'RBFInterpolant':
			return RBFInterpolant(kernel=self.kernel_dict[ self.parsed_json['kernel'] ], tail=self.tail_dict[ self.parsed_json['tail'] ], maxp=self.parsed_json['maxeval'] )