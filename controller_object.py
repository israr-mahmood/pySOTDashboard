"""

.. module:: controller_object
	:synopsis: Creates a POAP Controller Object for PySOT dashboard

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: controller_object
:Author: Israr Mahmood <im278@cornell.edu>

"""


from pySOT import *
from pySOT_dict import pySOT_class_dict
from poap.strategy import *
from poap.controller import *
from flask_socketio import SocketIO, send, emit


class MonitorSubClass(Monitor):
	"""Caputes and sends the values of each evaluation.

	MoniterSubClass inherits from the Monitor class. It hooks into the 
	controller and moniters it's progress. everytime the controller registers 
	a record completion event after appending the value of the current	
	evaluation EvalRecord.value. The on_complete function is invoked, sending
	the value of the lastest evaluation to the client.

	:param controller: The controller object to be monitered
	:type controller: controller

	"""

	def __init__(self, controller):
		"""Initilize the Monitor super class
		"""

		super(MonitorSubClass, self).__init__(controller)
		
	def on_complete(self, record):
		"""Send the value of the recently completed evaluation to the client

		:param record: Data structure containing information about the completed evaluation
		:type record: EvalRecord
		"""

		emit('abc',record.value)
	

class ControllerObject:
	"""Initilize a POAP controller using user's input parameters

	This class recieves parameters for the controller in the form of a 
	dictionary. The dictionary contains all the data needed, including 
	the types of controller and stratagy to be used and all of their 
	required input arguments.

	:param input_argument: Parameters needed for setting up the controller and strategy
	:type input_argument: dict
	:param pySOTObj: Optimization Problem, Adaptive Sampling, Surrogate Model and Experimental Design objects
	:type pySOT_Object: dict
	:param class_dict: Catogarised List of all classes in PySOT
	:type class_dict: dict

	:ivar input_argument: Parameter for setting up controller object
	:ivar pySOT_Object: PySOT objects needed for the problem
	:ivar class_dict: Catogarised List of all classes in PySOT
	"""

	def __init__(self, input_argument, pySOT_Object, class_dict=None):
		self.flag = False
		self.msg = ''

		if class_dict == None:
			obj = pySOT_class_dict()
			self.class_dict = obj.get_dict()
		else:
			self.class_dict = class_dict
		
		self.input_argument = input_argument
		self.pySOT_Object = pySOT_Object

		print('starting strat')
		try:
			print('stratagy_begin')
			self.stratagy = self.init_stratagy(input_argument['strategy'])
			print('stratagy_close')
		except:
			self.msg = 'Could not initilize stratagy'
			return

		try:
			self.controller = self.init_controller(input_argument['controller'])
		except:
			self.msg = 'Could not initilize Controller'
			return

		self.flag = True

	def init_controller(self, input_argument):
		if input_argument['function'] in self.class_dict['controller']:
			arguments = {}
			for c in self.class_dict['controller'][ input_argument['function'] ][ 0 ]:
				if c in input_argument:
					arguments[c] = input_argument[c]
				elif c == 'objective':
					arguments[c] = self.pySOT_Object['data'].objfunction
			print(arguments)
			print(eval (input_argument['function'] ))
			
			

			controller = eval( input_argument['function'] ) (**arguments) 
			controller.strategy = self.stratagy
			self.monitor = MonitorSubClass(controller)

			return controller
		return 'controller not found'

	def init_stratagy(self, input_argument):
		print(input_argument)

		if input_argument['function'] in self.class_dict['strategy']:
			arguments = { 'worker_id' : 0 }
			for c in self.class_dict['strategy'][ input_argument['function'] ][ 0 ]:
				if c in input_argument:
					if c == 'proj_fun':
						arguments[c] = eval(input_argument[c])
					else: 
						arguments[c] = input_argument[c]

			for c in self.class_dict['strategy'][ input_argument['function'] ][ 0 ]:
				if c in self.pySOT_Object:
					arguments[c] = self.pySOT_Object[c]
			
			return eval(input_argument['function'])(**arguments)
		return 'strategy not found'


	def get_controller(self):
		if self.flag:
			return self.flag, self.controller
		else: 
			return self.flag, self.msg
