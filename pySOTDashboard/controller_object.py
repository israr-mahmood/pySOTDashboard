"""

.. module:: controller_object
	:synopsis: Creates a POAP Controller Object for PySOT dashboard

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: controller_object
:Author: Israr Mahmood <im278@cornell.edu>

"""
from gevent import sleep
from flask_socketio import emit
from poap.controller import *
from poap.strategy import *
from pySOT import *

from pySOT_dictionary import PySOTDictionary


class MonitorSubClass(Monitor):
    """Captures and sends the values of each evaluation.

    MoniterSubClass inherits from the Monitor class. It hooks into the 
    controller and monitors it's progress. every time the controller 
    registers a record completion event after appending the value of 
    the current	evaluation EvalRecord.value. The on_complete method 
    is invoked, sending the value of the latest evaluation to the 
    client.

    :param controller: The controller object to be monitored
    :type controller: controller

    """

    def __init__(self, controller):
        """Initialize the Monitor super class
        """

        super(MonitorSubClass, self).__init__(controller)
        for calls in controller.term_callbacks:
            controller.remove_term_callback(calls)
        controller.add_term_callback(self.on_terminate)

    def on_complete(self, record):
        """Send the value of the recently completed evaluation to the client

        :param record: Data structure containing information about the 
            completed evaluation
        :type record: EvalRecord
        """

        emit('abc', record.value)
        sleep(0.000000001)

    def on_terminate(self):
        """Handle terminates
        """

        pass


class ControllerObject:
    """Initialize a POAP controller using user's input parameters

    This class receives parameters for the controller in the form of a 
    dictionary. The dictionary contains all the data needed, including 
    the types of controller and strategy to be used and all of their 
    required input arguments.

    :param input_argument: Parameters needed for setting up the 
        controller and strategy
    :type input_argument: dict
    :param pysot_object: Optimization Problem, Adaptive Sampling, 
        Surrogate Model and Experimental Design objects
    :type pysot_object: dict
    :param pysot_dict: Categorised List of all classes in PySOT
    :type pysot_dict: dict

    :raise ValueError: If any of the controller or strategy picked does
        not exit

    :ivar monitor: Instance of MonitorSubClass
    :ivar input_argument: Parameter for setting up controller object
    :ivar pySOT_Object: PySOT objects needed for the problem
    :ivar PySOT_dict: Categorised List of all classes in PySOT
    :ivar strategy: Instance of PySOT strategy 
    :ivar controller: Instance of POAP controller

    .. note: The init process is further broken in two methods
        init_controller and init_strategy

    .. note: Before the controller object can be obtined. The strategy
        and then the controller have to be intilized in that order, 
        using the init_strategy and init_controller methods. Currently
        both the methods are called from within __init__ but they can 
        be called seperatly based on usage.
    """

    def __init__(self, input_argument, pysot_object, pysot_dict=None):

        if pysot_dict is None:
            obj = PySOTDictionary()
            self.PySOT_dict = obj.get_dict()
        else:
            self.PySOT_dict = pysot_dict

        self.controller = None
        self.strategy = None
        self.monitor = None
        self.input_argument = input_argument
        self.pySOT_Object = pysot_object

        self.init_strategy(input_argument['strategy'])
        self.init_controller(input_argument['controller'])

    def init_controller(self, controller_argument):
        """Initialize the Controller using input arguments.

        If the controller specified by the user exists in POAP then the 
        arguments name for the controller and their values are extracted 
        from PySOT_dict and controller_argument respectively. These arguments 
        are then used to initialize the controller object.

        The eval() method is used to execute the controller, as the user 
        only provides the server with the strings containing the controllers 
        name. 

        :param controller_argument: Information required to initialize 
            controller
        :type controller_argument: dict
        """

        if controller_argument['function'] in self.PySOT_dict['controller']:
            arguments = {}

            for args in self.PySOT_dict['controller'][controller_argument['function']][0]:
                if args in controller_argument:
                    arguments[args] = controller_argument[args]
                elif args == 'objective':
                    arguments[args] = self.pySOT_Object['data'].objfunction

            self.controller = eval(controller_argument['function'])(**arguments)
            self.controller.strategy = self.strategy
            self.monitor = MonitorSubClass(self.controller)

        else:
            raise ValueError('Controller not Found')

    def init_strategy(self, strategy_argument):
        """Initializes the Strategy using input arguments.

        If the strategy specified by the user exists in PySOT then the 
        arguments name for the strategy and their values are extracted 
        from PySOT_dict and controller_argument respectively. These 
        arguments are then used to initialize the strategy object.

        The eval() function is used to execute the strategy, as the user 
        only provides the server with the strings containing the controllers 
        name. 

        :param strategy_argument: Information required to initialize 
            strategy
        :type strategy_argument: dict
        """

        if strategy_argument['function'] in self.PySOT_dict['strategy']:
            if 'MultiSampling' == strategy_argument['function']:
                arguments['strategy_list'] = []
                for strategy_ in strategy_argument['strategy_list']:
                    self.init_strategy(strategy_argument['strategy_list'][strategy_])
                    arguments['strategy_list'].append(self.strategy)

                if 'cycle' in strategy_argument:
                    arguments['cycle'] = strategy_argument['cycle']
            else:
                arguments = {'worker_id': 0}
                for c in self.PySOT_dict['strategy'][strategy_argument['function']][0]:
                    if c in strategy_argument:
                        if c == 'proj_fun':
                            arguments[c] = eval(strategy_argument[c])
                        else:
                            arguments[c] = strategy_argument[c]

                for c in self.PySOT_dict['strategy'][strategy_argument['function']][0]:
                    if c in self.pySOT_Object:
                        arguments[c] = self.pySOT_Object[c]

            self.strategy = eval(strategy_argument['function'])(**arguments)

        else:
            raise ValueError('Strategy not Found')

    def get_controller(self):
        """Request the initialized controller object

        :return: Controller Object
        """

        return self.controller
