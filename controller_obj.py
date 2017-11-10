from pySOT import *
from pySOT_dict import pySOT_class_dict
from poap.strategy import *
from poap.controller import *

class controller_obj:
	def __init__(self, parsed_json, pySOTObj, feval_callbacks = None, class_dict = None):
		self.flag = True
		self.msg = ''

		if class_dict == None:
			obj = pySOT_class_dict()
			self.class_dict = obj.get_dict()
		else:
			self.class_dict = class_dict
		
		self.feval_callbacks = feval_callbacks
		self.parsed_json = parsed_json
		self.pySOTObj = pySOTObj

		try:
			self.stratagy = self.init_stratagy(parsed_json['strategy'])
		except:
			self.flag = False
			self.msg = 'Could not initilize stratagy'

		if self.flag:
			try:
				self.controller = self.init_controller(parsed_json['controller'])
			except:
				self.flag = False
				self.msg = 'Could not initilize Controller'

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
			controller.feval_callbacks = self.feval_callbacks
			return controller
		return 'controller not found'



		# print(parsed_json['function'])
		# print('hffhf')
		# if parsed_json['function'] == 'SerialController':
		# 	controller = SerialController(self.pySOTObj['data'].objfunction)
		# else:
		# 	controller = ThreadController()

		# controller.strategy = self.stratagy
		# controller.feval_callbacks = self.feval_callbacks
		# print(self.class_dict['controller'])
		# # while 1:
		# # 	pass
		# return controller 
		# return [ True, self.class_dict['strategy'][ parsed_json['function'] ][ 0 ](**arguments) ]
		# return [ False, 'controller not found' ]



		






	def init_stratagy(self, parsed_json):
		nsamples = parsed_json['nsamples']

		print(' ')
		print('hrere')
		print(self.class_dict['strategy'])

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
			
			# print(' ')
			# print(parsed_json['function'])
			# print(' ')
			# print(self.class_dict['strategy'])
			# print(' ')
			# print(self.pySOTObj)
			# print(' ')
			# print(self.class_dict['strategy'][ parsed_json['function'] ][ 1 ])
			# print(' ')
			# print(arguments)
			# print(self.class_dict['strategy'][ parsed_json['function'] ][ 0 ])
			# print('somthing somthing')
			# while 1:
			# 	pass
			return eval( parsed_json['function'] ) (**arguments)
		return 'strategy not found'

		# strategy = SyncStrategyNoConstraints(
#         worker_id=0, data=data, maxeval=maxeval, nsamples=1,
#         exp_design=exp_des, response_surface=surrogate,
#         sampling_method=adapt_samp)
# controller.strategy = strategy

	def get_controller(self):
		if self.flag:
			return self.flag, self.controller
		else: 
			return self.flag, self.msg
