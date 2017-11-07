from pySOT import *

class optimization_problems:
	def __init__(self, parsed_json):
		self.parsed_json = parsed_json
		if parsed_json['function'] == 'custom':
			pass

	def run(self):
		if self.parsed_json['function'] == 'custom':
			pass
		elif self.parsed_json['function'] == 'Ackley':
			return Ackley(dim=self.parsed_json['dim'])