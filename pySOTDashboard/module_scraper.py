"""

.. module:: module_scraper
	:synopsis: Scrapes the module for classes and functions

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: module_scraper
:Author: Israr Mahmood <im278@cornell.edu>

"""


from inspect import getmembers, isclass, getargspec, isroutine, isfunction


class GetModuleClass():
	"""Extracts specific class information from request modules.
	Like class names and their arguments.
	"""

	def get_class_names(self, mod_name):
		"""Compiles a dictionary containing class __name__ attributes as keys
		and the class objects as values.

		:param mod_name: The module from which the information is extracted

		:return: dict
		"""

		mod_name_str = mod_name.__name__
		res = [tup for tup in getmembers(mod_name) if isclass(tup[1])]
		return dict([tup for tup in res if self.is_in_current_module(tup[1], mod_name_str)])

	def get_arguments_and_default_values(self, val):
		"""Retrives the arguments for the __init__ function and their
		default values for the specified object

		:param val: The class object to extract inforamtion from
		:type val: Object

		:return: list
		"""

		res = [getargspec(val.__init__).args[1:], getargspec(val.__init__).defaults]
		if res[1] == None:
			res[1] = 'None'
		else:
			res[1] = list(res[1])
			for i in range(len(res[1])):
				if res[1][i] == None:
					res[1][i] = 'None'
				elif isclass(res[1][i]):
					res[1][i] = res[1][i].__name__
		return res

	def get_fun_names(self, mod_name):
		"""Compiles a dictionary containing module __name__ attributes as keys
		and the objects as values.

		:param mod_name: The module from which the information is extracted

		:return: list
		"""

		mod_name_str = mod_name.__name__
		res = [tup for tup in getmembers(mod_name) if isfunction(tup[1])]
		return  ([tup[0] for tup in res if self.is_in_current_module(tup[1], mod_name_str)])

	def is_in_current_module(self, method, mod_name_str):
		"""A helper method or class to check if the a object exists in a given file

		:param method: The object under question
		:type method: Object
		:param mod_name_str: The __name__ attribute of the parent file
		:type mod_name_str: String

		:return: bool
		"""
		return dict(getmembers(method, lambda a:not(isroutine(a))))['__module__']==mod_name_str