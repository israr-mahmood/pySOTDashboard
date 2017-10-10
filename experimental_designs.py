from pySOT import *

class experimental_designs:
	def __init__(self,parsed_json,dim):
		self.parsed_json = parsed_json
		self.dim = dim

	def run(self):
		try:
			if self.parsed_json['function'] == 'BoxBehnken':
				return True, BoxBehnken(dim=self.dim)
			elif self.parsed_json['function'] == 'LatinHypercube':
				return True, LatinHypercube(dim=self.dim, npts=self.parsed_json['samples'], criterion=self.parsed_json['criterion'])
			elif self.parsed_json['function'] == 'SymmetricLatinHypercube':
				return True, SymmetricLatinHypercube(dim=self.dim, npts=self.parsed_json['samples'])
			elif self.parsed_json['function'] == 'TwoFactorial':
				return True, TwoFactorial(dim=self.dim)
		except:	
			if self.parsed_json['function'] == 'LatinHypercube':
				return False, 'check criterion'
			elif self.parsed_json['function'] == 'TwoFactorial':
				return False, 'dim >= 15'
			else:
				return False, 'Error: experimental_design'