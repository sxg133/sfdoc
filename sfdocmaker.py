import cgi;

def __get_class_item(classname):
	return '<li><a href="' + classname + '.html">' + classname + '</a></li>'

def __get_author_content(author):
	return '<li>' + author.name + '</li>'

def __get_param_content(param):
	return '<tr><td>' + param.name + '</td><td>' + cgi.escape(param.param_type) + '</td><td>' + param.description + '</td></tr>'

def __get_class_index(cinfo):
	return '<tr><td><a href="' + cinfo.name +'.html">' + cinfo.name + '</a></td><td>' + cinfo.description + '</td></tr>'

def __fill_in_method_content(content_method, minfo):
	new_content = content_method.replace('[methodname]', minfo.name)
	new_content = new_content.replace('[methodscope]', minfo.scope)
	new_content = new_content.replace('[constructor]', ('(constructor)' if minfo.is_constructor else ''))
	new_content = new_content.replace('[methoddescription]', minfo.description)
	param_content = [__get_param_content(p) for p in minfo.params]
	if param_content:
		new_content = new_content.replace('[params]', ''.join(param_content))
		new_content = new_content.replace('[paramsClass]', 'params')
	else:
		new_content = new_content.replace('[params]', '<em>There are no parameters</em>')
		new_content = new_content.replace('[paramsClass]', 'no-params')
	new_content = new_content.replace('[returntype]', cgi.escape(minfo.return_type))
	new_content = new_content.replace('[returndescription]',minfo.return_description)
	return new_content

def __fill_in_class_content(content_master, content_method, cinfo, project_name):
	new_content = content_master.replace('[projectname]', project_name)
	new_content = new_content.replace('[classname]', cinfo.name)
	new_content = new_content.replace('[classdescription]', cinfo.description)
	new_content = new_content.replace('[since]', cinfo.since)
	author_content = [__get_author_content(a) for a in cinfo.authors]
	new_content = new_content.replace('[authors]', ''.join(author_content))
	method_content = [__fill_in_method_content(content_method, minfo) for minfo in cinfo.methods]
	new_content = new_content.replace('[methodlist]', ''.join(method_content))
	return new_content

def create_outfile(classlist, cinfo, target, template_master='template_master.html', template_method='template_method.html', project_name='Apex Documentation', indexfile=''):
	content_master = ''
	with open(template_master) as f:
		content_master = f.read()
	content_method = ''
	with open(template_method) as f:
		content_method = f.read()
	
	new_content = __fill_in_class_content(content_master, content_method, cinfo, project_name)
	class_items = [__get_class_item(c) for c in classlist]
	new_content = new_content.replace('[classlist]', ''.join(class_items))
	new_content = new_content.replace('[indexfile]', indexfile)
	with open(target, 'w+') as f:
		f.write(new_content)

def create_index(classlist, target, template_index='template_index.html', project_name='Apex Documentation'):
	content_index = ''
	with open(template_index) as f:
		content_index = f.read()

	new_content = content_index.replace('[projectname]', project_name)
	class_content = [__get_class_index(c) for c in classlist]
	new_content = new_content.replace('[classes]', ''.join(class_content))

	with open(target, 'w+') as f:
		f.write(new_content)