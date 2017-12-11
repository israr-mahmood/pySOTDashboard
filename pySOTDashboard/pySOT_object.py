"""

.. module:: pySOT_object
	:synopsis: Creates a PySOT Object for PySOT dashboard

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: pySOT_object
:Author: Israr Mahmood <im278@cornell.edu>

"""

from pySOT import *

from pySOT_dictionary import PySOTDictionary


class PySOTObject:
    """Creates all object needed to initialize the PySOT experiment.

    This class will generate Optimization Problem, Experimental Design,
    Surrogate Model and Adaptive Sampling. required to perform PySOT
    experiment.

    :param parsed_json: All the object and their arguments that need
        to be initialized.
    :type parsed_json: dict
    :param class_dict: Dictionary produced by PySOTDictionary
    :type class_dict: dict

    :ivar data: Instance of Optimization Problem
    :ivar exp_des: Instance of Experimental Design
    :ivar surrogate: Instance of Surrogate Model
    :ivar adapt_samp: Instance of Adaptive Sampling
    :ivar maxeval: Number of max evaluations

    .. note: Only the back instances are implements. Other
        features such as heuristics need to be implemented.
    """

    def __init__(self, parsed_json, class_dict=None):
        self.parsed_json = parsed_json

        if class_dict is None:
            obj = PySOTDictionary()
            self.class_dict = obj.get_dict()
        else:
            self.class_dict = class_dict

        self.data = None
        self.exp_des = None
        self.surrogate = None
        self.adapt_samp = None
        self.maxeval = None

        self.maxeval = self.parsed_json['surrogate_model']['maxp']

        self.init_optimization_problem(self.parsed_json['optimization_problem'])
        self.init_experimental_design(self.parsed_json['experimental_design'], self.data.dim)
        self.init_surrogate_model(self.parsed_json['surrogate_model'])
        self.init_adaptive_sampling(self.parsed_json['adaptive_sampling'])

    def return_values(self):
        """Request the PySOT object.
        The method will return a dictionary containing the objects
        required to initialize the strategy for the Experiment.

        :return: dict
        """

        return {'data': self.data,
                'maxeval': self.maxeval,
                'exp_design': self.exp_des,
                'response_surface': self.surrogate,
                'sampling_method': self.adapt_samp}

    def init_optimization_problem(self, op_arguments):
        """Initialize Optimization Problem

        This module receives a dictionary containing the name of problem
        to be initialized along with its arguments. After confirming that
        the input problem indeed exists in PySOT. It will initialize the
        problem using the arguments provided and store the resulting
        problem in self.data.

        :param op_arguments: Name of and arguments of Optimization Problem.
        :type op_arguments: dict

        :raise ValueError: If the optimization problem specified in
            input do not exist in current PySOT version.
        """

        if op_arguments['function'] in self.class_dict['optimization_problem']:
            arguments = {}
            for class_args in self.class_dict['optimization_problem'][op_arguments['function']][0]:
                if class_args in op_arguments:
                    arguments[class_args] = op_arguments[class_args]
            self.data = eval(op_arguments['function'])(**arguments)
        else:
            raise ValueError('optimization problem not found')

    def init_adaptive_sampling(self, as_arguments):
        """Initialize Adaptive Sampling

        This module receives a dictionary containing the name arguments
        of the adaptive sampling to be initialized. After confirming that
        the input adaptive sampling indeed exists in PySOT. It will
        initialize the adaptive sampling using the arguments provided
        and store the resulting object in self.adapt_samp.

        :param as_arguments: Name of and arguments of adaptive sampling.
        :type as_arguments: dict

        :raise ValueError: If the adaptive sampling specified in
            input do not exist in current PySOT version.
        """

        if as_arguments['function'] in self.class_dict['adaptive_sampling']:
            arguments = {'data': self.data}
            for arg in self.class_dict['adaptive_sampling'][as_arguments['function']][0]:
                if arg in as_arguments:
                    arguments[arg] = as_arguments[arg]
            self.adapt_samp = eval(as_arguments['function'])(**arguments)
        else:
            raise ValueError('adaptive sampling not found')

    def init_surrogate_model(self, sm_arguments):
        """Initialize Surrogate Model

        This module receives a dictionary containing the name arguments
        of the surrogate model to be initialized. After confirming that
        the input surrogate model indeed exists in PySOT. It will
        initialize the surrogate model using the arguments provided
        and store the resulting object in self.surrogate.

        :param sm_arguments: Name of and arguments of Surrogate Model.
        :type sm_arguments: dict

        :raise ValueError: If the Surrogate Model specified in
            input do not exist.
        """

        if sm_arguments['function'] in self.class_dict['surrogate_model']:
            arguments = {}
            for arg in self.class_dict['surrogate_model'][sm_arguments['function']][0]:
                if arg in sm_arguments:
                    if arg == 'kernel':
                        arguments[arg] = eval(sm_arguments[arg])
                    elif arg == 'tail':
                        arguments[arg] = eval(sm_arguments[arg])
                    else:
                        arguments[arg] = sm_arguments[arg]

            self.surrogate = eval(sm_arguments['function'])(**arguments)
        else:
            raise ValueError('surrogate model not found')

    def init_experimental_design(self, ed_arguments, dim):
        """Initialize Experimental Design

        This module receives a dictionary containing the name arguments
        of the experimental design to be initialized. After confirming that
        the input experimental design indeed exists in PySOT. It will
        initialize the experimental design using the arguments provided
        and store the resulting object in self.exp_des.

        :param ed_arguments: Name of and arguments of experimental design.
        :type ed_arguments: dict
        :param dim: Dimensions of optimization problem data set.
        :type dim: int

        :raise ValueError: If the experimental design specified in
            input do not exist.
        """

        if ed_arguments['function'] in self.class_dict['experimental_design']:
            arguments = {}
            arguments['dim'] = dim
            for arg in self.class_dict['experimental_design'][ed_arguments['function']][0]:
                if arg in ed_arguments:
                    arguments[arg] = ed_arguments[arg]
            self.exp_des = eval(ed_arguments['function'])(**arguments)
        else:
            raise ValueError('experimental design not found')
