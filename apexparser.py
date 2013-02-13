import re
import methodinfo

pattern_header = r'/\*[^{]*{'
re_header = re.compile(pattern_header, re.MULTILINE | re.DOTALL)
pattern_param = r'@param\s+(?P<name>[a-zA-Z]+)\s+(?P<desc>.*)'
re_param = re.compile(pattern_param)
pattern_return = r'@return\s+(?P<desc>.*)\s+'
re_return = re.compile(pattern_return)
pattern_method = r'(?P<scope>public|private|protected)\s+(?P<returntype>[a-zA-Z\<\>]+)\s+(?P<name>[a-zA-Z]+)\s*(?P<args>\(.*\))'
re_method = re.compile(pattern_method)
pattern_arg = r'(?P<argtype>[a-zA-Z\<\>]+)\s+(?P<name>[a-zA-Z]+)'
re_arg = re.compile(pattern_arg)

def __readFile(file):
	with open(file) as f:
		return f.read()

def __parse_class_header(header):	# TODO IMPLEMENT METHOD
	pass

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
		match_method = re_method.search(line)
		if match_param:
			param_desc_dict[match_param.group('name')] = match_param.group('desc')
		elif match_return:
			pass
		elif match_method:
			minfo.scope = match_method.group('scope')
			minfo.returntype = match_method.group('returntype')
			minfo.name = match_method.group('name')
			params = __parse_params(match_method.group('args'))
			for p in params:
				if p.name in param_desc_dict:
					p.description = param_desc_dict[p.name]
			minfo.params.extend(params)
		elif line:
			desc += re.sub('(/\*+|\*/)', '', line.strip())
	minfo.description = re.sub('^' + minfo.name + '\s+', '', desc.strip())
	return minfo

def parse_file(file):
	content = __readFile(file)
	result = re_header.findall(content)
	cinfo = methodinfo.ClassInfo()
	# TODO PARSE INITIAL HEADER FOR CLASS OR TRIGGER
	methods = []
	if len(result) > 1:
		methods = [__parse_method_header(r) for r in result[1:]]
	for m in methods:
		print(m.description)
	cinfo.methods = methods
	return cinfo