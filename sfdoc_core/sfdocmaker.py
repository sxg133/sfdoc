import cgi
from sfdoc_settings import SFDocSettings
import re

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
	new_content = new_content.replace('[methodoverloadnumber]', str(minfo.overload_number))
	new_content = new_content.replace('[methodscope]', minfo.scope)
	new_content = new_content.replace('[constructor]', ('(constructor)' if minfo.is_constructor else ''))
	new_content = new_content.replace('[methoddescription]', minfo.description)
	param_content = [__get_param_content(p) for p in minfo.params]
	if param_content:
		new_content = new_content.replace('[params]', ''.join(param_content))
		new_content = new_content.replace('[paramsClass]', 'params')
	else:
		new_content = new_content.replace('[params]', '<em>None</em>')
		new_content = new_content.replace('[paramsClass]', 'no-params')
	new_content = new_content.replace('[returntype]', cgi.escape(minfo.return_type))
	new_content = new_content.replace('[returndescription]',minfo.return_description)
	return new_content

def __fill_in_property_content(pinfo):
	row = '<tr class="' + pinfo.scope + '">'
	row += '<td class="name">' + pinfo.name + '</td>'
	row += '<td class="scope">' + pinfo.scope + '</td>'
	row += '<td class="type">' + cgi.escape(pinfo.property_type) + '</td>'
	row += '</tr>'
	return row

def __fill_in_interface_content(interface):
	return '<li><a href="%s.html" title="%s">%s</a></li>' % (interface, interface, interface)

def __fill_in_class_content(content_master, content_method, content_parent_class, content_interfaces, content_property, cinfo):
	new_content = content_master.replace('[projectname]', SFDocSettings.project_name)
	new_content = new_content.replace('[classname]', cinfo.name)
	new_content = new_content.replace('[classdescription]', cinfo.description)
	new_content = new_content.replace('[since]', cinfo.since)
	new_content = new_content.replace('[versionnumber]', cinfo.version_number)
	new_content = new_content.replace('[versiondate]', cinfo.version_date)
	author_content = [__get_author_content(a) for a in cinfo.authors]
	new_content = new_content.replace('[authors]', ''.join(author_content))
	method_content = [__fill_in_method_content(content_method, minfo) for minfo in cinfo.methods if minfo.scope.lower() in SFDocSettings.scope]
	new_content = new_content.replace('[methodlist]', ''.join(method_content))

	if SFDocSettings.no_properties:
		new_content = new_content.replace('<h3>Properties</h3>','')
		new_content = new_content.replace('[propertytable]', '')
	else:
		prop_content = [__fill_in_property_content(pinfo) for pinfo in cinfo.properties if pinfo.scope.lower() in SFDocSettings.scope]
		prop_table = content_property.replace('[properties]', ''.join(prop_content))
		new_content = new_content.replace('[propertytable]', prop_table)

	if cinfo.parent_class:
		new_content = new_content.replace('[parentclass]', content_parent_class.replace('[parentclassname]', cinfo.parent_class))
	else:
		new_content = new_content.replace('[parentclass]', '')

	if cinfo.interfaces:
		new_content = new_content.replace('[interfaces]', content_interfaces.replace('[interfaces]', ''.join([__fill_in_interface_content(interface) for interface in cinfo.interfaces])))
	else:
		new_content = new_content.replace('[interfaces]', '')

	return new_content

def create_outfile(classlist, cinfo, target):
	content_master = ''
	with open(SFDocSettings.template_master) as f:
		content_master = f.read()
		
	content_method = ''
	with open(SFDocSettings.template_method) as f:
		content_method = f.read()
		
	content_property = ''
	with open(SFDocSettings.template_property) as f:
		content_property = f.read()
		
	content_parent_class = ''
	with open(SFDocSettings.template_parent_class) as f:
		content_parent_class = f.read()
		
	content_interfaces = ''
	with open(SFDocSettings.template_interfaces) as f:
		content_interfaces = f.read()
		
	
	new_content = __fill_in_class_content(content_master, content_method, content_parent_class, content_interfaces, content_property, cinfo)
	class_items = [__get_class_item(c) for c in classlist]
	new_content = new_content.replace('[classlist]', ''.join(class_items))
	new_content = new_content.replace('[indexfile]', SFDocSettings.indexfile)
	if not SFDocSettings.no_method_list:
		mnamelist = ''.join(['<li class="' + m.scope + '"><a href="#' + m.name + str(m.overload_number) + '">' + m.name + '</a>' for m in cinfo.methods if m.scope in SFDocSettings.scope])
		new_content = new_content.replace('[methodnamelist]', mnamelist)
	else:
		new_content = re.sub(r'\<aside[^\<]*method-list-container.*/aside\>', '', new_content, count=2, flags = re.MULTILINE | re.DOTALL)
	
	if not SFDocSettings.test:
		with open(target, 'w+') as f:
			f.write(new_content)

def create_index(classlist, target):
	content_index = ''
	with open(SFDocSettings.template_index) as f:
		content_index = f.read()

	new_content = content_index.replace('[projectname]', SFDocSettings.project_name)
	class_content = [__get_class_index(c) for c in classlist]
	new_content = new_content.replace('[classes]', ''.join(class_content))

	if not SFDocSettings.test:
		with open(target, 'w+') as f:
			f.write(new_content)
