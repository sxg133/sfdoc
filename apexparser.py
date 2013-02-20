import re
import methodinfo
from sfdoc_settings import SFDocSettings
import sfconstants

pattern_header = r'/\*[^{;]*[{;]'
re_header = re.compile(pattern_header, re.MULTILINE | re.DOTALL | re.I)
pattern_param = r'@param\s+(?P<name>[a-zA-Z]+)\s+(?P<desc>.*)'
re_param = re.compile(pattern_param, re.I)
pattern_return = r'@return\s+(?P<desc>.*)'
re_return = re.compile(pattern_return, re.I)
pattern_constructor = r'(?P<scope>public|private|protected)\s+(?P<name>[a-zA-Z_]+)\s*(?P<args>\(.*\))'
re_constructor = re.compile(pattern_constructor, re.I)
pattern_method = r'(?P<scope>public|private|protected)\s+(abstract\s+)?(virtual\s+)?(static\s+)?(override\s+)?(?P<returntype>[a-zA-Z\<\>,_\s]+)\s+(?P<name>[a-zA-Z_]+)\s*(?P<args>\(.*\))'
re_method = re.compile(pattern_method, re.I)
pattern_interface_method = r'(?P<returntype>[a-zA-Z\<\>,_\s]+)\s+(?P<name>[a-zA-Z_]+)\s*(?P<args>\(.*\))'
re_interface_method = re.compile(pattern_interface_method, re.I)
pattern_arg = r'(?P<argtype>[a-zA-Z\<\>,_\s]+)\s+(?P<name>[a-zA-Z]+)'
re_arg = re.compile(pattern_arg, re.I)
pattern_author = r'@author\s+(?P<name>[^\<]*)\<(?P<email>[a-zA-Z0-9@\.]+)\>'
re_author = re.compile(pattern_author, re.I)
pattern_since = r'@since\s+(?P<date>[0-9\-/]+)'
re_since = re.compile(pattern_since, re.I)
pattern_class = r'(?P<scope>public|private|protected)\s+((abstract|interface)\s+)?(with\s+sharing\s+)?(class\s+)?(?P<name>[a-zA-Z]+)'
re_class = re.compile(pattern_class, re.I)
pattern_property = r'(?P<scope>public|private|protected)\s+(?P<paramtype>[a-zA-Z\<\>,_\s]+)\s+(?P<name>[a-zA-Z]+)\s*{'
re_property = re.compile(pattern_property, re.MULTILINE | re.DOTALL | re.I)

def __readFile(file):
	with open(file) as f:
		return f.read()

def __parse_class_header(header):
	cinfo = methodinfo.ClassInfo()
	desc = ''
	for line in header.split('\n'):
		line = line.strip()
		match_author = re_author.search(line)
		match_since = re_since.search(line)
		match_class = re_class.search(line)
		if match_author:
			author = methodinfo.Author()
			author.name = match_author.group('name').strip()
			author.email = match_author.group('email')
			cinfo.authors.append(author)
		elif match_since:
			cinfo.since = match_since.group('date')	# TODO CHECK OUT PYTHON DATE TYPES
		elif match_class:
			cinfo.name = match_class.group('name')
			if sfconstants.INTERFACE in match_class.group().lower():
				cinfo.is_interface = True
			elif sfconstants.ABSTRACT in match_class.group().lower():
				cinfo.is_abstract = True
		elif line:
			desc += re.sub('(/\*+|\*/)', '', line.strip())
	cinfo.description = re.sub('^' + cinfo.name + '\s+', '', desc.strip())	# remove class name from beginning of description
	if SFDocSettings.verbose >= 1:
		print(cinfo.name)
	return cinfo

def __parse_params(args):
	params = []
	for arg in args.split(','):
		arg_match = re_arg.search(arg)
		if arg_match:
			p = methodinfo.ParamInfo()
			p.name = arg_match.group('name')
			p.param_type = arg_match.group('argtype')
			params.append(p)
	return params

def __parse_method_header(header, is_interface=False):
	minfo = methodinfo.MethodInfo()
	param_desc_dict = {}
	desc = ''
	for line in header.split('\n'):
		line = line.strip()
		match_param = re_param.search(line)
		match_return = re_return.search(line)
		match_constructor = re_constructor.search(line)
		if is_interface:
			match_method = re_interface_method.search(line)
		else:
			match_method = re_method.search(line)
		if match_param:
			param_desc_dict[match_param.group('name')] = match_param.group('desc')
		elif match_return:
			minfo.return_description = match_return.group('desc')
		elif match_constructor:
			minfo.scope = match_constructor.group('scope')
			minfo.name = match_constructor.group('name')
			params = __parse_params(match_constructor.group('args'))
			for p in params:
				if p.name in param_desc_dict:
					p.description = param_desc_dict[p.name]
			minfo.params.extend(params)
			minfo.is_constructor = True
		elif match_method:
			if not is_interface:
				minfo.scope = match_method.group('scope')
			minfo.return_type = match_method.group('returntype').strip()
			minfo.name = match_method.group('name')
			params = __parse_params(match_method.group('args'))
			for p in params:
				if p.name in param_desc_dict:
					p.description = param_desc_dict[p.name]
			minfo.params.extend(params)
		elif line:
			desc += re.sub('(/\*+|\*/)', '', line.strip())
	minfo.description = re.sub('^' + minfo.name + '\s+', '', desc.strip())	# remove method name from beginning of description
	if SFDocSettings.verbose >= 2:
		print('\t' + minfo.name + ' (' + minfo.scope + ' ' + minfo.return_type + ')')
	if SFDocSettings.verbose >= 3:
		for p in minfo.params:
			print('\t\t' + p.name + '(' + p.param_type + ')')
	return minfo

def __parse_all_methods(content, cinfo, methods):
	allmethods = []
	if cinfo.is_interface:
		allmethods = re_interface_method.findall(content)
	else:
		allmethods = re_method.findall(content)
	mnames = [m.name for m in methods]
	for m in allmethods:
		mname = m[1] if cinfo.is_interface else m[6]
		if mname not in mnames:
			meth = methodinfo.MethodInfo()
			meth.name = mname
			if cinfo.is_interface:
				meth.return_type = m[0].strip.replace('\n', '').replace('\t', '')
				meth.params = __params_params(m[2])
			else:
				meth.scope = m[0]
				meth.return_type = m[5]
				meth.params = __parse_params(m[7])
				methods.append(meth)

def __parse_properties(content):
	props = []
	properties = re_property.findall(content)
	for p in properties:
		if all(x not in p[1].lower() for x in [sfconstants.CLASS, sfconstants.INTERFACE]):
			prop = methodinfo.Property()
			prop.scope = p[0]
			prop.property_type = p[1]
			prop.name = p[2]
			props.append(prop)
	return props

def parse_file(file):
	content = __readFile(file)
	result = re_header.findall(content)
	cinfo = methodinfo.ClassInfo()
	if len(result) > 0:
		cinfo = __parse_class_header(result[0])
	methods = []
	if len(result) > 1:
		methods = [__parse_method_header(r, cinfo.is_interface) for r in result[1:]]

	# Hack for methods w/o headers (probably need to rethink this entire module)
	__parse_all_methods(content, cinfo, methods)

	cinfo.properties = __parse_properties(content)

	cinfo.methods = methods
	return cinfo