"""

.. module:: pySOT_dictionary
	:synopsis: Scrapes the module for classes and functions

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: pySOT_dictionary
:Author: Israr Mahmood <im278@cornell.edu>

"""


from poap import controller
from pySOT import *

import delay_function
from module_scraper import GetModuleClass
import projection_function


class PySOTDictionary:
    """Generates a dictionary continuing all the methods/classes of PySOT

    Each method in the class parses a different file in pySOT 
    directory and extracts all the methods or classes from that 
    file along with their default values. Then appends all of 
    the extracted data to a dictionary with a unique key.

    The names of methods or classes extracted are appended to 
    the dictionary, instead of the objects. This is done because 
    the final dictionary obtained is meant to be converted to 
    json and objects can not be converted to json. The eval() 
    method can be used to call objects using their string names 
    stored in the dictionary.

    :ivar kernel_list: List of all kernel classes.
    :ivar tail_list: List of all tail classes.
    :ivar projection_list: List of user defined projection functions.
    :ivar delay_list: List of user defined delay functions.
    :ivar optimization_problem_dict: Dictionary of Optimization Problems.
    :ivar experimental_design_dict: Dictionary of Experimental Designs.
    :ivar surrogate_model_dict: Dictionary of Surrogate Models.
    :ivar adaptive_sampling_dict: Dictionary of Adaptive Sampling.
    :ivar strategy_dict: Dictionary of PySOT strategies.
    :ivar controller_dict: Dictionary of POAP controllers.
    :ivar obj: An instance of GetModuleClass used to extract all
        the information required to initialize the dictionaries.

    .. note: This code is not thread safe. A lock has to be included
        in get_dict while accessing the variables to make this code 
        thread safe.

    .. note: The dictionaries have to initialized using generate_dictionaries.

    .. note: An assumption was made that all kernel or any other types 
        of classes will always exist in a single file.
    """

    def __init__(self):
        self.kernel_list = {}
        self.tail_list = {}
        self.projection_list = {}
        self.delay_list = {}
        self.optimization_problem_dict = {}
        self.experimental_design_dict = {}
        self.surrogate_model_dict = {}
        self.adaptive_sampling_dict = {}
        self.strategy_dict = {}
        self.controller_dict = {}

        self.obj = GetModuleClass()

        self.generate_dictionaries()

    def generate_dictionaries(self):
        """Uses GetModuleClass class to initialize all dictionaries.
        """

        self.kernel_generate_list()
        self.tail_generate_list()
        self.optimization_problem_generate_dict()
        self.experimental_design_generate_dict()
        self.surrogate_model_generate_dict()
        self.adaptive_sampling_generate_dict()
        self.strategy_generate_dict()
        self.controller_generate_dict()
        self.projection_generate_list()
        self.delay_generate_list()

    def projection_generate_list(self):
        """
        Initializes projection_list with user defined projection functions.
        By using the GetModuleClass instance, it fetches the list of all 
        projection function in projection_function.py file.
        """

        mod_name = projection_function
        self.projection_list = self.obj.get_fun_names(mod_name)

    def delay_generate_list(self):
        """
        Initializes delay_list with user defined delay function.
        By using the GetModuleClass instance, it feteches the list of all 
        delay function in delay_function.py file.
        """

        mod_name = delay_function
        self.delay_list = self.obj.get_fun_names(mod_name)

    def kernel_generate_list(self):
        """
        Initialize kernel_list with all kernels objects in PySOT.
        By using the GetModuleClass instance, it fetches the list of all 
        kernel objects in kernels.py file. 
        """

        mod_name = kernels
        self.kernel_list = self.obj.get_class_names(mod_name)
        self.kernel_list = list(self.kernel_list)

    def tail_generate_list(self):
        """
        Initialize tail_list with all tail objects in PySOT
        By using the GetModuleClass instance, it fetches the list of all 
        tail objects in tails.py file.
        """

        mod_name = tails
        self.tail_list = self.obj.get_class_names(mod_name)
        self.tail_list = list(self.tail_list)

    def optimization_problem_generate_dict(self):
        """
        Initialize optimization_problem_dict with all optimization problems
        in test_problems in pySOT directory. 

        By using the GetModuleClass instance, we obtain the dictionary 
        of all optimization problems. Then we fetches all the input 
        arguments and their defaults values for each of the problem objects 
        in a loop. The objects arguments and default values are then 
        appended to the dictionary, with the problem's name attribute 
        as the key.
        """

        mod_name = test_problems
        self.optimization_problem_dict = self.obj.get_class_names(mod_name)
        for i in self.optimization_problem_dict:
            self.optimization_problem_dict[i] = \
                self.obj.get_arguments_and_default_values(self.optimization_problem_dict[i])

    def experimental_design_generate_dict(self):
        """
        Initialize experimental_design_dict with all experimental design
        in experimental_design.py file in pySOT directory. 

        By using the GetModuleClass instance, we obtain the dictionary 
        of all optimization problems. Then we fetches all the input 
        arguments and their defaults values for each of the design object 
        in a loop. The objects arguments and default values are then 
        appended to the dictionary, with the design's name attribute as 
        the key.
        """

        mod_name = experimental_design
        self.experimental_design_dict = self.obj.get_class_names(mod_name)
        for i in self.experimental_design_dict:
            self.experimental_design_dict[i] = \
                self.obj.get_arguments_and_default_values(self.experimental_design_dict[i])

    def surrogate_model_generate_dict(self):
        """
        Initialize surrogate_model_dict with surrogate model in rbf.py 
        file in pySOT directory. 

        By using the GetModuleClass instance, we obtain the dictionary 
        of surrogate model's. Then we fetches all the input 
        arguments and their defaults values for each of the model object 
        in a loop. The objects arguments and default values are then 
        appended to the dictionary, with the model's name attribute 
        as the key.
        """

        mod_name = rbf
        self.surrogate_model_dict = self.obj.get_class_names(mod_name)
        for i in self.surrogate_model_dict:
            self.surrogate_model_dict[i] = \
                self.obj.get_arguments_and_default_values(self.surrogate_model_dict[i])

    def adaptive_sampling_generate_dict(self):
        """
        Initialize surrogate_model_dict with surrogate model in rbf.py 
        file in pySOT directory. 

        By using the GetModuleClass instance, we obtain the dictionary 
        of surrogate model's. Then we fetches all the input 
        arguments and their defaults values for each of the model object 
        in a loop. The objects arguments and default values are then 
        appended to the dictionary, with the model's name attribute 
        as the key.
        """

        mod_name = adaptive_sampling
        self.adaptive_sampling_dict = self.obj.get_class_names(mod_name)
        for i in self.adaptive_sampling_dict:
            self.adaptive_sampling_dict[i] = \
                self.obj.get_arguments_and_default_values(self.adaptive_sampling_dict[i])

    def strategy_generate_dict(self):
        """
        Initialize strategy_dict with strategies in sot_sync_strategies.py 
        in pySOT directory. 

        By using the GetModuleClass instance, we obtain the dictionary 
        of strategies. Then we fetches all the input arguments and 
        their defaults values for each of the strategy object 
        in a loop. The objects arguments and default values are then 
        appended to the dictionary, with the strategy's name attribute 
        as the key.
        """

        mod_name = sot_sync_strategies
        self.strategy_dict = self.obj.get_class_names(mod_name)
        for i in self.strategy_dict:
            self.strategy_dict[i] = \
                self.obj.get_arguments_and_default_values(self.strategy_dict[i])

    def controller_generate_dict(self):
        """
        Initialize controller_dict with strategies in controller.py 
        in POAP. 

        By using the GetModuleClass instance, we obtain the dictionary 
        of controllers. It has to noted that there are classes in 
        controller.py that are not controllers. Therefore they have to
        be removed from the dictionary. An assumption is made that all
        controllers will have the key work controller in their name and
        therefore all objects were filter based on this assumption. 

        Then all the input arguments and their defaults values for 
        each of the controller object are fetched in a loop and 
        appended to the dictionary, with the controller's name attribute 
        as the key.
        """

        mod_name = controller
        self.controller_dict = self.obj.get_class_names(mod_name)

        del_list = []
        for j in self.controller_dict:
            if 'Controller' not in self.controller_dict[j].__name__:
                del_list.append(j)
        for j in del_list:
            del self.controller_dict[j]

        for i in self.controller_dict:
            self.controller_dict[i] = \
                self.obj.get_arguments_and_default_values(self.controller_dict[i])

    def get_dict(self):
        """Request the PySOT Dictionary

        :return: Dictionary
        """

        return {'kernel': self.kernel_list,
                'tail': self.tail_list,
                'optimization_problem': self.optimization_problem_dict,
                'experimental_design': self.experimental_design_dict,
                'surrogate_model': self.surrogate_model_dict,
                'adaptive_sampling': self.adaptive_sampling_dict,
                'strategy': self.strategy_dict,
                'controller': self.controller_dict,
                'delay': self.delay_list,
                'proj_fun': self.projection_list}

