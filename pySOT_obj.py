from pySOT import *
from pySOT_dict import pySOT_class_dict

class pySOT_obj:
	def __init__(self, parsed_json, class_dict = None):
		self.parsed_json = parsed_json

		if class_dict is None:
			obj = pySOT_class_dict()
			self.class_dict = obj.get_dict()
		else:
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
		return { 'data' : self.data,
				 'maxeval' : self.maxeval,
				 'exp_design' : self.exp_des,
				 'response_surface' : self.surrogate,
				 'sampling_method' : self.adapt_samp}
		#return [self.data, self.exp_des, self.surrogate, self.adapt_samp, self.maxeval]

	def get_optimization_problem(self, parsed_json):
		if parsed_json['function'] in self.class_dict['optimization_problem']:
			arguments = {}
			for c in self.class_dict['optimization_problem'][ parsed_json['function'] ][ 1 ]:
				if c in parsed_json:
					arguments[c] = parsed_json[c]
			#return [ True, self.class_dict['optimization_problem'][ parsed_json['function'] ][ 0 ](**arguments) ]
			return [ True, eval(parsed_json['function']) (**arguments) ]
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
			#return [ True, self.class_dict['adaptive_sampling'][ parsed_json['function'] ][ 0 ](**arguments) ]
			return [ True, eval( parsed_json['function'] ) (**arguments) ]
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
						#arguments[c] = self.class_dict['kernel'][ parsed_json[c] ]
						arguments[c] = eval( parsed_json[c] )
					elif c == 'tail':
						#arguments[c] = self.class_dict['tail'][ parsed_json[c] ]
						arguments[c] = eval( parsed_json[c] )
					else:
						arguments[c] = parsed_json[c]

			#return [ True, self.class_dict['surrogate_model'][ parsed_json['function'] ][ 0 ](**arguments) ]
			return [ True, eval( parsed_json['function'] ) (**arguments) ]
		return [False, 'surrogate model not found']

	def get_experimental_design(self, parsed_json, dim):

		if parsed_json['function'] in self.class_dict['experimental_design']:
			arguments = {}
			for c in self.class_dict['experimental_design'][ parsed_json['function'] ][ 1 ]:
				if c in parsed_json:
					arguments[c] = parsed_json[c]
			print(arguments)
			#return [ True, self.class_dict['experimental_design'][ parsed_json['function'] ][ 0 ](**arguments) ]
			return [ True, eval( parsed_json['function'] ) (**arguments) ]
		return [False, 'experimental design not found']