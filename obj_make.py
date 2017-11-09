from pySOT import *
from inspect import getmembers, isclass, getargspec, isroutine
from threading import Lock
from sys import modules

class get_mod_class():
	def get_class_names(self, mod_name, mod_name_str):
		res = [tup for tup in getmembers(mod_name) if isclass(tup[1])]
		return dict ([ tup for tup in res if dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == mod_name_str ])

	def get_arguments_and_default_values(self, val):
		return [ val, getargspec(val.__init__).args[1:], getargspec(val.__init__).defaults ]

class pySOT_class_dict():
	def __init__(self):
		self.kernel_dict = {}
		self.tail_dict = {}
		self.optimization_problem_dict = {}
		self.experimental_design_dict = {}
		self.surrogate_model_dict = {}
		self.adaptive_sampling_dict = {}

		self.obj = get_mod_class()

		self.generate_dict()

	def generate_dict(self):
		self.kerel_generate_dict()
		self.tail_generate_dict()
		self.optimization_problem_generate_dict()
		self.experimental_design_generate_dict()
		self.surrogate_model_generate_dict()
		self.adaptive_sampling_generate_dict()

	# def get_class_names(self, mod_name, mod_name_str):
	# 	res = [tup for tup in getmembers(mod_name) if isclass(tup[1])]
	# 	return dict ([ tup for tup in res if dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == mod_name_str ])

	# def get_arguments_and_default_values(self, val):
	# 	return [ val, getargspec(val.__init__).args[1:], getargspec(val.__init__).defaults ]

	def kerel_generate_dict(self):
		mod_name = kernels 			# Enter Module name here only one at a time SORRY!!!!
		#self.kernel_dict = self.get_class_names(mod_name, mod_name.__name__)
		self.kernel_dict = self.obj.get_class_names(mod_name, mod_name.__name__)

		## To add a custom kerel 
		## self.kernel_dict[' kerel_name '] = kernel_object

	def tail_generate_dict(self):
		mod_name = tails 			# Enter Module name here only one at a time SORRY!!!!
		self.tail_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		
		## To add a custom tail
		## self.tail_dict[ 'tail_name' ] = tail_object

	def optimization_problem_generate_dict(self):
		mod_name = test_problems 			# Enter Module name here only one at a time SORRY!!!!
		self.optimization_problem_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		for i in self.optimization_problem_dict:
			self.optimization_problem_dict[i] = self.obj.get_arguments_and_default_values(self.optimization_problem_dict[i])
		
		## To add a custom optimization problem
		## self.optimization_problem_dict[ 'optimization_problem_name' ] = [optimization_problem_object, [argument_string_list], [defaults_list]]

	def experimental_design_generate_dict(self):
		mod_name = experimental_design
		self.experimental_design_dict = self.obj.get_class_names(mod_name, mod_name.__name__)

		for i in self.experimental_design_dict:
			self.experimental_design_dict[i] = self.obj.get_arguments_and_default_values(self.experimental_design_dict[i])

		## To add a custom experimental design
		## self.experimental_design_dict[ 'experimental_design_name' ] = [experimental_design_object, [argument_string_list], [defaults_list]]

	def surrogate_model_generate_dict(self):
		mod_name = rbf

		self.surrogate_model_dict = self.obj.get_class_names(mod_name, mod_name.__name__)

		for i in self.surrogate_model_dict:
			self.surrogate_model_dict[i] = self.obj.get_arguments_and_default_values(self.surrogate_model_dict[i])

		## To add a custom surrogate model
		## self.experimental_design_dict[ 'experimental_design_name' ] = [experimental_design_object, [argument_string_list], [defaults_list]]

	def adaptive_sampling_generate_dict(self):
		mod_name = adaptive_sampling
		self.adaptive_sampling_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		for i in self.adaptive_sampling_dict:
			self.adaptive_sampling_dict[i] = self.obj.get_arguments_and_default_values(self.adaptive_sampling_dict[i])
		print(' ')
		print(self.adaptive_sampling_dict)

	def get_dict(self):
		return { 'kernel': self.kernel_dict, 
				 'tail' : self.tail_dict, 
				 'optimization_problem' : self.optimization_problem_dict, 
				 'experimental_design' : self.experimental_design_dict, 
				 'surrogate_model' : self.surrogate_model_dict , 
				 'adaptive_sampling' : self.adaptive_sampling_dict}


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
		if parsed_json['function'] in self.class_dict['optimization_problem']:
			arguments = {}
			for c in self.class_dict['optimization_problem'][ parsed_json['function'] ][ 1 ]:
				if c in parsed_json:
					arguments[c] = parsed_json[c]
			return [ True, self.class_dict['optimization_problem'][ parsed_json['function'] ][ 0 ](**arguments) ]
		return [False, 'optimization problem not found']

	def get_adaptive_sampling(self, parsed_json):
		print(' ')
		print('hrere')
		print(self.class_dict['adaptive_sampling'])

		if parsed_json['function'] in self.class_dict['adaptive_sampling']:
			arguments = {'data' : self.data}
			for c in self.class_dict['adaptive_sampling'][ parsed_json['function'] ][ 1 ]:
				if c in parsed_json:
					arguments[c] = parsed_json[c]
			print(arguments)
			print(self.class_dict['adaptive_sampling'][ parsed_json['function'] ][ 0 ])
			return [ True, self.class_dict['adaptive_sampling'][ parsed_json['function'] ][ 0 ](**arguments) ]
		return [False, 'adaptive sampling not found']

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