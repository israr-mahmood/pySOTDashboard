"""

.. module:: module_scraper
	:synopsis: Scrapes the module for classes and functions

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: module_scraper
:Author: Israr Mahmood <im278@cornell.edu>

"""


from inspect import getmembers, isclass, getargspec, isroutine, isfunction


class GetModuleClass():
	"""
	"""

	def get_class_names(self, mod_name):
		"""
		"""

		mod_name_str = mod_name.__name__
		res = [tup for tup in getmembers(mod_name) if isclass(tup[1])]
		return dict ([ tup for tup in res if dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == mod_name_str ])

	def get_arguments_and_default_values(self, val):
		"""
		"""

		res = [  getargspec(val.__init__).args[1:], getargspec(val.__init__).defaults ]
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
		"""
		"""

		mod_name_str = mod_name.__name__
		res = [tup for tup in getmembers(mod_name) if isfunction(tup[1])]
		return  ([ tup[0] for tup in res if dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == mod_name_str ])

	def belongs_to_current_module(self, method):
		pass