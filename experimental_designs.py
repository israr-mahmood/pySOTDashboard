from pySOT import *

class experimental_designs:
	def __init__(self,parsed_json,dim):
		self.parsed_json = parsed_json
		self.dim = dim

	def run(self):
		if self.parsed_json['function'] == 'SymmetricLatinHypercube':
			return SymmetricLatinHypercube(dim=self.dim, npts=self.parsed_json['samples'])