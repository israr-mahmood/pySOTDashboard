from pySOT import *
from poap import controller
from mod_scraper import get_mod_class
import projection_fun
import delay_fun


class pySOT_class_dict():
	def __init__(self):
		self.flag = True
		self.kernel_dict = {}
		self.tail_dict = {}
		self.optimization_problem_dict = {}
		self.experimental_design_dict = {}
		self.surrogate_model_dict = {}
		self.adaptive_sampling_dict = {}
		self.strategy_dict = {}
		self.controller_dict = {}
		self.projection_dict = {}
		self.delay_dict = {}

		self.obj = get_mod_class()

		self.generate_dict()

	def generate_dict(self):
		try:
			self.kerel_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find kernel Module'
			return
		try:
			self.tail_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find tail Module'
			return
		try:
			self.optimization_problem_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find optimization problem Module'
			return
		try:
			self.experimental_design_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find experimental design Module'
			return
		try:
			self.surrogate_model_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find surrogate model Module'
			return
		try:
			self.adaptive_sampling_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find adaptive sampling Module'
			return
		try:
			self.strategy_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find strategy Module'
			return
		try:
			self.controller_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find controller Module'
			return
		print('proj here')
		try:
			print('good 0')
			self.projection_generate_dict()
			print('good')
		except: 
			self.flag = False
			self.msg = 'Could not find projection_fun Module'
			print('bad')
			return
		print('delay here')
		try:
			self.delay_generate_dict()
		except: 
			self.flag = False
			self.msg = 'Could not find delay_fun Module'
			return


	def projection_generate_dict(self):
		mod_name = projection_fun 			# Enter Module name here only one at a time SORRY!!!!
		self.projection_dict = self.obj.get_fun_names(mod_name, mod_name.__name__)

		## To add a custom projection function go to projection_fun.py 

	def delay_generate_dict(self):
		mod_name = delay_fun 			# Enter Module name here only one at a time SORRY!!!!
		self.delay_dict = self.obj.get_fun_names(mod_name, mod_name.__name__)

		## To add a custom projection function go to delay_fun.py
		
	def kerel_generate_dict(self):
		mod_name = kernels 			# Enter Module name here only one at a time SORRY!!!!
		#self.kernel_dict = self.get_class_names(mod_name, mod_name.__name__)
		self.kernel_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		self.kernel_dict = list(self.kernel_dict)

		## To add a custom kerel 
		## self.kernel_dict[' kerel_name '] = kernel_object

	def tail_generate_dict(self):
		mod_name = tails 			# Enter Module name here only one at a time SORRY!!!!
		self.tail_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		self.tail_dict = list(self.tail_dict)
		## To add a custom tail
		## self.tail_dict[ 'tail_name' ] = tail_object

	def optimization_problem_generate_dict(self):
		mod_name = test_problems 			# Enter Module name here only one at a time SORRY!!!!
		self.optimization_problem_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		for i in self.optimization_problem_dict:
			self.optimization_problem_dict[i] = self.obj.get_arguments_and_default_values(self.optimization_problem_dict[i])

		print(' ')
		print(self.optimization_problem_dict)

		
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
		print('why happeing')
		print(self.adaptive_sampling_dict)

		## To add a custom adaptive sample
		## self.adaptive_sampling_dict[ 'adaptive_sample_name' ] = [adaptive_sampling_object, [argument_string_list], [defaults_list]]

	def strategy_generate_dict(self):
		mod_name = sot_sync_strategies
		self.strategy_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		for i in self.strategy_dict:
			self.strategy_dict[i] = self.obj.get_arguments_and_default_values(self.strategy_dict[i])
		print(' ')
		print('why zis happed')

		print(self.strategy_dict)

		## To add a custom strategy
		## self.strategy_dict[ 'strategy_name' ] = [strategy_object, [argument_string_list], [defaults_list]]

	def controller_generate_dict(self):
		mod_name = controller
		self.controller_dict = self.obj.get_class_names(mod_name, mod_name.__name__)
		
		del_list = []
		for j in self.controller_dict:
			if 'Controller' not in self.controller_dict[j].__name__:
				del_list.append(j)
		for j in del_list:
			del self.controller_dict[j]

		for i in self.controller_dict:
			self.controller_dict[i] = self.obj.get_arguments_and_default_values(self.controller_dict[i])
		print(' ')
		print('why zis happed')

		print(self.controller_dict)

		## To add a custom controller
		## self.controller_dict[ 'controller_name' ] = [controller_object, [argument_string_list], [defaults_list]]

	def get_dict(self):
		if self.flag:
			return self.flag, {  'kernel': self.kernel_dict, 
								 'tail' : self.tail_dict, 
								 'optimization_problem' : self.optimization_problem_dict, 
								 'experimental_design' : self.experimental_design_dict, 
								 'surrogate_model' : self.surrogate_model_dict , 
								 'adaptive_sampling' : self.adaptive_sampling_dict,
								 'strategy' : self.strategy_dict,
								 'controller' : self.controller_dict,
								 'delay' : self.delay_dict,
								 'proj_fun' : self.projection_dict}
		else:
			return self.flag, self.msg
