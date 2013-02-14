class ClassInfo:
	def __init__(self):
		self.name = ''
		self.desc = ''
		self.authors = []
		self.since = ''
		self.methods = []

class MethodInfo:
	def __init__(self):
		self.name = ''
		self.description = ''
		self.scope = ''
		self.params = []
		self.return_description = ''
		self.return_type = ''

class ParamInfo:
	def __init__(self):
		self.name = ''
		self.description = ''
		self.param_type = ''

class Author:
	def __init__(self):
		self.name = ''
		self.email = ''