"""

.. module:: controller_object
	:synopsis: Creates a Controller Object for PySOT dashboard

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: controller_object
:Author: Israr Mahmood <im278@cornell.edu>

"""


from pySOT import *
from pySOT_dict import pySOT_class_dict
from poap.strategy import *
from poap.controller import *


class MonitorSubClass(Monitor):
	def __init__(self, controller, callback_fun):
		super(MonitorSubClass, self).__init__(controller)
		self.callback_fun = callback_fun
		
	def on_complete(self, record):
		print('-----------------------------------------------------')
		callback_fun(record)
	
def this_fun(record):
	print('**********************************')
	while 1:
		pass

class controller_obj:
	def __init__(self, parsed_json, pySOTObj, feval_callbacks=None, class_dict=None):
		print('in controller')
		self.flag = False
		self.msg = ''

		if class_dict == None:
			obj = pySOT_class_dict()
			self.class_dict = obj.get_dict()
		else:
			self.class_dict = class_dict
		
		print('still here')
		self.feval_callbacks = feval_callbacks
		self.parsed_json = parsed_json
		self.pySOTObj = pySOTObj

		print('starting strat')
		try:
			print('stratagy_begin')
			self.stratagy = self.init_stratagy(parsed_json['strategy'])
			print('stratagy_close')
		except:
			self.msg = 'Could not initilize stratagy'
			return

		try:
			self.controller = self.init_controller(parsed_json['controller'])
		except:
			self.msg = 'Could not initilize Controller'
			return

		self.flag = True

	def init_controller(self, parsed_json):
		if parsed_json['function'] in self.class_dict['controller']:
			arguments = {}
			for c in self.class_dict['controller'][ parsed_json['function'] ][ 0 ]:
				if c in parsed_json:
					arguments[c] = parsed_json[c]
				elif c == 'objective':
					arguments[c] = self.pySOTObj['data'].objfunction
			print(arguments)
			print(eval (parsed_json['function'] ))
			controller = eval( parsed_json['function'] ) (**arguments) 
			controller.strategy = self.stratagy
			#controller.add_term_callback(self.feval_callbacks)
			#self.monitor = Monitor(controller)
			#self.monitor.on_complete = this_fun
			self.monitor = MonitorSubClass(controller, this_fun)
			#self.monitor.on_complete = on_complete#self.feval_callbacks
			return controller
		return 'controller not found'


	def init_stratagy(self, parsed_json):
		print(parsed_json)

		if parsed_json['function'] in self.class_dict['strategy']:
			arguments = { 'worker_id' : 0 }
			for c in self.class_dict['strategy'][ parsed_json['function'] ][ 0 ]:
				if c in parsed_json:
					if c == 'proj_fun':
						arguments[c] = eval(parsed_json[c])
					else: 
						arguments[c] = parsed_json[c]

			for c in self.class_dict['strategy'][ parsed_json['function'] ][ 0 ]:
				if c in self.pySOTObj:
					arguments[c] = self.pySOTObj[c]
			

			return eval(parsed_json['function'])(**arguments)
		return 'strategy not found'


	def get_controller(self):
		if self.flag:
			return self.flag, self.controller
		else: 
			return self.flag, self.msg
