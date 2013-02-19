import re
import methodinfo
from sfdoc_settings import SFDocSettings

pattern_header = r'/\*[^{;]*[{;]'
re_header = re.compile(pattern_header, re.MULTILINE | re.DOTALL)
pattern_param = r'@param\s+(?P<name>[a-zA-Z]+)\s+(?P<desc>.*)'
re_param = re.compile(pattern_param)
pattern_return = r'@return\s+(?P<desc>.*)'
re_return = re.compile(pattern_return)
pattern_constructor = r'(?P<scope>public|private|protected)\s+(?P<name>[a-zA-Z_]+)\s*(?P<args>\(.*\))'
re_constructor = re.compile(pattern_constructor)
pattern_method = r'(?P<scope>public|private|protected)?\s?(abstract\s+)?(virtual\s+)?(static\s+)?(?P<returntype>[a-zA-Z\<\>,_\s]+)\s+(?P<name>[a-zA-Z_]+)\s*(?P<args>\(.*\))'
re_method = re.compile(pattern_method)
pattern_arg = r'(?P<argtype>[a-zA-Z\<\>,_\s]+)\s+(?P<name>[a-zA-Z]+)'
re_arg = re.compile(pattern_arg)
pattern_author = r'@author\s+(?P<name>[^\<]*)\<(?P<email>[a-zA-Z0-9@\.]+)\>'
re_author = re.compile(pattern_author)
pattern_since = r'@since\s+(?P<date>[0-9\-/]+)'
re_since = re.compile(pattern_since)
pattern_class = r'(?P<scope>public|private|protected)\s+((abstract|interface)\s+)?(with\s+sharing\s+)?(class\s+)?(?P<name>[a-zA-Z]+)'
re_class = re.compile(pattern_class)

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
		elif line:
			desc += re.sub('(/\*+|\*/)', '', line.strip())
	cinfo.description = re.sub('^' + cinfo.name + '\s+', '', desc.strip())
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

def __parse_method_header(header):
	minfo = methodinfo.MethodInfo()
	param_desc_dict = {}
	desc = ''
	for line in header.split('\n'):
		line = line.strip()
		match_param = re_param.search(line)
		match_return = re_return.search(line)
		match_constructor = re_constructor.search(line)
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
			minfo.scope = match_method.group('scope')
			if not minfo.scope:
				minfo.scope = ''
			minfo.return_type = match_method.group('returntype').strip()
			minfo.name = match_method.group('name')
			params = __parse_params(match_method.group('args'))
			for p in params:
				if p.name in param_desc_dict:
					p.description = param_desc_dict[p.name]
			minfo.params.extend(params)
		elif line:
			desc += re.sub('(/\*+|\*/)', '', line.strip())
	minfo.description = re.sub('^' + minfo.name + '\s+', '', desc.strip())
	if SFDocSettings.verbose >= 2:
		print('\t' + minfo.name + ' (' + minfo.scope + ' ' + minfo.return_type + ')')
	if SFDocSettings.verbose >= 3:
		for p in minfo.params:
			print('\t\t' + p.name + '(' + p.param_type + ')')
	return minfo

def parse_file(file):
	content = __readFile(file)
	result = re_header.findall(content)
	cinfo = methodinfo.ClassInfo()
	if len(result) > 0:
		cinfo = __parse_class_header(result[0])
	methods = []
	if len(result) > 1:
		methods = [__parse_method_header(r) for r in result[1:]]

	# Hack for methods w/o headers (probably need to rethink this entire module)
	allmethods = re_method.findall(content)
	mnames = [m.name for m in methods]
	for m in allmethods:
		if m[5] not in mnames:
			meth = methodinfo.MethodInfo()
			meth.scope = m[0]
			meth.return_type = m[4]
			meth.name = m[5]
			meth.params = __parse_params(m[6])
			methods.append(meth)

	cinfo.methods = methods
	return cinfo