import importlib

def myfactory(module_name):
   module = importlib.import_module("plugins." + module_name)
   return getattr(module, module_name.capitalize())