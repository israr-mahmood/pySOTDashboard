from pySOT import *
from inspect import getmembers, isclass, getargspec, isroutine
from threading import Lock
from sys import modules

class pySOT_class_dict():
	def __init__(self):
		self.kernel_dict = {}
		self.tail_dict = {}
		self.optimization_problem_dict = {}
		self.experimental_design_dict = {}
		self.surrogate_model_dict = {}

		self.generate_dict()

	def generate_dict(self):
		self.kerel_generate_dict()
		self.tail_generate_dict()
		self.optimization_problem_generate_dict()
		self.experimental_design_generate_dict()
		self.surrogate_model_generate_dict()

	def kerel_generate_dict(self):
		self.kernel_dict = dict( [tup for tup in getmembers(kernels) if isclass(tup[1])] )

		## To add a custom kerel 
		## self.kernel_dict[' kerel_name '] = kernel_object

	def tail_generate_dict(self):
		self.tail_dict = dict( [tup for tup in getmembers(tails) if isclass(tup[1])] )
		
		## To add a custom tail
		## self.tail_dict[ 'tail_name' ] = tail_object

	def optimization_problem_generate_dict(self):
		self.optimization_problem_dict = dict( [ tup for tup in getmembers(test_problems) if isclass(tup[1])] )
		for i in self.optimization_problem_dict:
			self.optimization_problem_dict[i] = [ self.optimization_problem_dict[i], getargspec(self.optimization_problem_dict[i].__init__).args[1:], getargspec(self.optimization_problem_dict[i].__init__).defaults ]

		## To add a custom optimization problem
		## self.optimization_problem_dict[ 'optimization_problem_name' ] = [optimization_problem_object, [argument_string_list], [defaults_list]]

	def experimental_design_generate_dict(self):
		mod_name = experimental_design
		mod_name_str = 'experimental_design'

		self.experimental_design_dict = [ tup for tup in getmembers(mod_name) if isclass(tup[1])]
		self.experimental_design_dict = dict ([ tup for tup in self.experimental_design_dict if dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == 'pySOT.'+mod_name_str or dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == mod_name_str ])
		
		for i in self.experimental_design_dict:
			self.experimental_design_dict[i] = [ self.experimental_design_dict[i], getargspec(self.experimental_design_dict[i].__init__).args[1:], getargspec(self.experimental_design_dict[i].__init__).defaults ]

		## To add a custom experimental design
		## self.experimental_design_dict[ 'experimental_design_name' ] = [experimental_design_object, [argument_string_list], [defaults_list]]

	def surrogate_model_generate_dict(self):
		mod_name = rbf
		mod_name_str = 'rbf'

		self.surrogate_model_dict = [ tup for tup in getmembers(mod_name) if isclass(tup[1])]
		self.surrogate_model_dict = dict ([ tup for tup in self.surrogate_model_dict if dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == 'pySOT.'+mod_name_str or dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == mod_name_str ])

		for i in self.surrogate_model_dict:
			print(i)
			print('remember me')
			self.surrogate_model_dict[i] = [ self.surrogate_model_dict[i], getargspec(self.surrogate_model_dict[i].__init__).args[1:], getargspec(self.surrogate_model_dict[i].__init__).defaults ]

		## To add a custom surrogate model
		## self.experimental_design_dict[ 'experimental_design_name' ] = [experimental_design_object, [argument_string_list], [defaults_list]]

	def get_dict(self):
		return { 'kernel': self.kernel_dict, 'tail' : self.tail_dict, 'optimization_problem' : self.optimization_problem_dict, 'experimental_design' : self.experimental_design_dict, 'surrogate_model' : self.surrogate_model_dict }


class pySOT_obj:
	def __init__(self, parsed_json, class_dict):
		self.parsed_json = parsed_json
		self.class_dict = class_dict
		self.data = 0
		self.exp_des = 0
		self.surrogate = 0
		self.adapt_samp = 0
		self.maxp = 0
		self.sucess = True
		self.fail_msg = 'none'


		#self.kernel_dict = {'CubicKernel' : CubicKernel}
		#self.tail_dict = {'LinearTail' : LinearTail}


	def run(self):
		print('Starting long haul\n\n\n')

		try:
			self.maxeval = self.parsed_json['surrogate_model']['maxp']
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
		print('\n\n\n'+str(self.class_dict['optimization_problem'][ parsed_json['function'] ] )+'\n') #-------------------------

		#if parsed_json['function'] == 'custom':
		#	return [False, 'Custom OPtimaizaton Problem Not Implemented']
		#elif parsed_json['function'] in self.class_dict['optimization_problem']:

		# A option for a cutom problem was not implemented on the client side so no option is available here
		if parsed_json['function'] in self.class_dict['optimization_problem']:
			arguments = {}
			for c in self.class_dict['optimization_problem'][ parsed_json['function'] ][ 1 ]:
				if c in parsed_json:
					arguments[c] = parsed_json[c]
			return [ True, self.class_dict['optimization_problem'][ parsed_json['function'] ][ 0 ](**arguments) ]
		return [False, 'optimization problem not found']

		# Delete the following code if the above code works

		# if parsed_json['function'] == 'custom':
		# 	return [True, 1]
		# elif parsed_json['function'] in self.class_dict['optimization_problem']:
		# 	return [True, self.class_dict['optimization_problem'][ parsed_json['function'] ][0] (dim=parsed_json['dim'])]
		# else:
		# 	return [not True, 'optimization problem not found']

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
		print('this s')
		print(self.class_dict['surrogate_model'])
		print('that s')

		if parsed_json['function'] in self.class_dict['surrogate_model']:
			arguments = {}
			print(self.class_dict['surrogate_model'][ parsed_json['function'] ][1])
			for c in self.class_dict['surrogate_model'][ parsed_json['function'] ][ 1 ]:
				print(c)
				if c in parsed_json:
					print(c)
					if c == 'kernel':
						arguments[c] = self.class_dict['kernel'][ parsed_json[c] ]
					elif c == 'tail':
						arguments[c] = self.class_dict['tail'][ parsed_json[c] ]
					else:
						arguments[c] = parsed_json[c]

			return [ True, self.class_dict['surrogate_model'][ parsed_json['function'] ][ 0 ](**arguments) ]
		return [False, 'surrogate model not found']

	def get_experimental_design(self, parsed_json, dim):

		if parsed_json['function'] in self.class_dict['experimental_design']:
			arguments = {}
			for c in self.class_dict['experimental_design'][ parsed_json['function'] ][ 1 ]:
				if c in parsed_json:
					arguments[c] = parsed_json[c]
			print(arguments)
			return [ True, self.class_dict['experimental_design'][ parsed_json['function'] ][ 0 ](**arguments) ]
		return [False, 'experimental design not found']

		# try:
		# 	if parsed_json['function'] == 'BoxBehnken':
		# 		return True, BoxBehnken(dim=dim)
		# 	elif parsed_json['function'] == 'LatinHypercube':
		# 		return True, LatinHypercube(dim=dim, npts=parsed_json['samples'], criterion=parsed_json['criterion'])
		# 	elif parsed_json['function'] == 'SymmetricLatinHypercube':
		# 		return True, SymmetricLatinHypercube(dim=dim, npts=parsed_json['samples'])
		# 	elif parsed_json['function'] == 'TwoFactorial':
		# 		return True, TwoFactorial(dim=dim)
		# except:	
		# 	if parsed_json['function'] == 'LatinHypercube':
		# 		return False, 'check criterion'
		# 	elif parsed_json['function'] == 'TwoFactorial':
		# 		return False, 'dim >= 15'
		
		return False, 'Invalid Experimental Design'
