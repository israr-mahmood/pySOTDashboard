from pySOT import *

class adaptive_samplings:
	def __init__(self,data,parsed_json):
		self.data = data
		self.parsed_json = parsed_json

	def run(self):
		try:

			if self.parsed_json['function'] == 'CandidateDDS':
				return True, CandidateDDS(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateDDS_CONT':
				return True, CandidateDDS_CONT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])		
			elif self.parsed_json['function'] == 'CandidateDDS_INT':
				return True, CandidateDDS_INT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateDYCORS':
				return True, CandidateDYCORS(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateDYCORS_CONT':
				return True, CandidateDYCORS_CONT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateDYCORS_INT':
				return True, CandidateDYCORS_INT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateSRBF':
				return True, CandidateSRBF(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateSRBF_CONT':
				return True, CandidateSRBF_CONT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateSRBF_INT':
				return True, CandidateSRBF_INT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateUniform':
				return True, CandidateUniform(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateUniform_CONT':
				return True, CandidateUniform_CONT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'CandidateUniform_INT':
				return True, CandidateUniform_INT(data=self.data, numcand=self.parsed_json['numcand']*self.data.dim, weights=self.parsed_json['weights'])
			elif self.parsed_json['function'] == 'GeneticAlgorithm':
				return True, GeneticAlgorithm(data=self.data)
			elif self.parsed_json['function'] == 'MultiSampling':
				return True, MultiSampling(strategy_list=self.parsed_json['strategy_list'], cycle=self.parsed_json['cycle']) 
			elif self.parsed_json['function'] == 'MultiStartGradient':
				return True, MultiStartGradient((self.data, method=self.parsed_json['method'], num_restarts=self.parsed_json['num_restarts']))
			else:
				return False 'Invalid Adaptive Sampling'

		except:
			return False 'candidate points are incorrect or weights aren’t a list in [0, 1]'

