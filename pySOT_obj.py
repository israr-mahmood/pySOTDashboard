from pySOT import *
from inspect import getmembers, isclass

class pySOT_class_dict():
	def __init__(self):
		self.kernel_dict = {}

	def generate_dict(self):

		

class pySOT_obj:
	def __init__(self, parsed_json):
		self.parsed_json = parsed_json
		self.data = 0
		self.exp_des = 0
		self.surrogate = 0
		self.adapt_samp = 0
		self.maxeval = 0
		self.sucess = True
		self.fail_msg = 'none'


		self.kernel_dict = {'CubicKernel' : CubicKernel}
		self.tail_dict = {'LinearTail' : LinearTail}


	def run(self):
		print('Starting long haul\n\n\n')
		try:
			self.maxeval = self.parsed_json['surrogate_model']['maxeval']
		except:
			self.sucess = False
			self.fail_msg = 'Could not find maxeval'
			return[self.sucess, self.fail_msg]
		print('maxeval: '+str(self.maxeval)+'\n\n\n')
		try:
			[self.sucess, self.data] = self.get_optimization_problem( self.parsed_json['optimization_problem'] )
			if not self.sucess:
				self.fail_msg = self.data
				return [self.sucess, self.fail_msg]
		except:
			self.sucess = False
			self.fail_msg = 'Could not compute optimization problem'
			return[self.sucess, self.fail_msg]
		print('have optimazation problem\n\n\n')
		try:
			[self.sucess, self.exp_des] = self.get_experimental_design( self.parsed_json['experimental_design'], self.data.dim ) 
			if not self.sucess:
				self.fail_msg = self.exp_des
				return [self.sucess, self.fail_msg]
		except:
			self.sucess = False
			self.fail_msg = 'Could not compute sampling experimental design'
			return[self.sucess, self.fail_msg]
		print('have experimental design\n\n\n')
		try:
			[self.sucess, self.surrogate] = self.get_surrogate_model( self.parsed_json['surrogate_model'] ) 
			if not self.sucess:
				self.fail_msg = self.surrogate
				return [self.sucess, self.fail_msg]
		except:
			self.sucess = False
			self.fail_msg = 'Could not compute surrogate'
			return[self.sucess, self.fail_msg]
		print('have surrogate model')
		try:
			[self.sucess, self.adapt_samp] = self.get_adaptive_sampling(self.parsed_json['adaptive_sampling'])
			if not self.sucess:
				self.fail_msg = self.adapt_samp
				return [self.sucess, self.fail_msg]
		except:
			self.sucess = False
			self.fail_msg = 'Could not compute sampling stratagy'
			return[self.sucess, self.fail_msg]
		print('all set here')
		return self.sucess, 'Good to GO'

	def return_values(self):		
		return [self.data, self.exp_des, self.surrogate, self.adapt_samp, self.maxeval]

	def get_optimization_problem(self, parsed_json):
		if parsed_json['function'] == 'custom':
			return [True, 1]
		elif parsed_json['function'] == 'Ackley':
			return [True, Ackley(dim=parsed_json['dim'])]
		else:
			return [not True, 'optimization problem not found']

	def get_adaptive_sampling(self, parsed_json):
		if parsed_json['function'] == 'CandidateDDS':
			return True, CandidateDDS(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateDDS_CONT':
			return True, CandidateDDS_CONT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])		
		elif parsed_json['function'] == 'CandidateDDS_INT':
			return True, CandidateDDS_INT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateDYCORS':
			return True, CandidateDYCORS(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateDYCORS_CONT':
			return True, CandidateDYCORS_CONT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateDYCORS_INT':
			return True, CandidateDYCORS_INT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateSRBF':
			return True, CandidateSRBF(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateSRBF_CONT':
			return True, CandidateSRBF_CONT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateSRBF_INT':
			return True, CandidateSRBF_INT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateUniform':
			return True, CandidateUniform(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateUniform_CONT':
			return True, CandidateUniform_CONT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'CandidateUniform_INT':
			return True, CandidateUniform_INT(data=self.data, numcand=parsed_json['numcand']*self.data.dim, weights=parsed_json['weights'])
		elif parsed_json['function'] == 'GeneticAlgorithm':
			return True, GeneticAlgorithm(data=self.data)
		elif parsed_json['function'] == 'MultiSampling':
			return True, MultiSampling(strategy_list=parsed_json['strategy_list'], cycle=parsed_json['cycle']) 
		elif parsed_json['function'] == 'MultiStartGradient':
			return True, MultiStartGradient(self.data, method=parsed_json['method'], num_restarts=parsed_json['num_restarts'])
		
		return False, 'Invalid Adaptive Sampling'

	def get_surrogate_model(self, parsed_json):
		if parsed_json['function'] == 'RBFInterpolant':
			return True, RBFInterpolant(kernel=self.kernel_dict[ parsed_json['kernel'] ], tail=self.tail_dict[ parsed_json['tail'] ], maxp=parsed_json['maxeval'] ) 

		return False, 'Invalid Surrogate Model'

	def get_experimental_design(self, parsed_json, dim):
		try:
			if parsed_json['function'] == 'BoxBehnken':
				return True, BoxBehnken(dim=dim)
			elif parsed_json['function'] == 'LatinHypercube':
				return True, LatinHypercube(dim=dim, npts=parsed_json['samples'], criterion=parsed_json['criterion'])
			elif parsed_json['function'] == 'SymmetricLatinHypercube':
				return True, SymmetricLatinHypercube(dim=dim, npts=parsed_json['samples'])
			elif parsed_json['function'] == 'TwoFactorial':
				return True, TwoFactorial(dim=dim)
		except:	
			if parsed_json['function'] == 'LatinHypercube':
				return False, 'check criterion'
			elif parsed_json['function'] == 'TwoFactorial':
				return False, 'dim >= 15'
		
		return False, 'Invalid Experimental Design'
 