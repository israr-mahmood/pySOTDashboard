from inspect import getmembers, isclass, getargspec, isroutine

class get_mod_class():
	def get_class_names(self, mod_name, mod_name_str):
		res = [tup for tup in getmembers(mod_name) if isclass(tup[1])]
		return dict ([ tup for tup in res if dict( getmembers(tup[1], lambda a:not(isroutine(a))) ) ['__module__'] == mod_name_str ])

	def get_arguments_and_default_values(self, val):
		return [ val, getargspec(val.__init__).args[1:], getargspec(val.__init__).defaults ]