class ClassInfo:
	def __init__(self):
		self.name = ''
		self.description = ''
		self.authors = []
		self.since = ''
		self.methods = []
		self.is_interface = False
		self.is_abstract = False
		self.properties = []

class MethodInfo:
	def __init__(self):
		self.name = ''
		self.description = ''
		self.scope = ''
		self.params = []
		self.return_description = ''
		self.return_type = ''
		self.is_constructor = False
		self.overload_number = 0

class ParamInfo:
	def __init__(self):
		self.name = ''
		self.description = ''
		self.param_type = ''

class Author:
	def __init__(self):
		self.name = ''
		self.email = ''

class Property:
	def __init__(self):
		self.name = ''
		self.property_type = ''
		self.scope = ''