from pySOT import *

class adaptive_samplings:
	def __init__(self,data,parsed_json):
		self.data = data
		self.parsed_json = parsed_json

	def run(self):
		if self.parsed_json['function'] == 'CandidateDYCORS':
			return CandidateDYCORS(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim)
		