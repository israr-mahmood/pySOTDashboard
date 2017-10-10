from pySOT import *

class ensemble_surrogates:
	def __init__(self, parsed_json):
		self.parsed_json = parsed_json

	def run(self):
		if self.parsed_json['function'] == 'EnsembleSurrogate':
			return EnsembleSurrogate(model_list=self.parsed_json['model_list'], maxp=self.parsed_json['maxp'])