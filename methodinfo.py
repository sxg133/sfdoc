class ClassInfo:
	def __init__(self):
		self.name = ''
		self.desc = ''
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