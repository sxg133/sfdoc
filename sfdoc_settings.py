import os

class SFDocSettings:
	verbose = 0
	test = False
	no_properties = True
	no_method_list = False
	base_path, filename = os.path.split(os.path.realpath(__file__))
	template_master = os.path.join(base_path, 'templates', 'template_master.html')
	template_method = os.path.join(base_path, 'templates', 'template_method.html')
	template_property = os.path.join(base_path, 'templates', 'template_property.html')
	template_parent_class = os.path.join(base_path, 'templates', 'template_parent_class.html')
	template_interfaces = os.path.join(base_path, 'templates', 'template_interfaces.html')
	template_index = os.path.join(base_path, 'templates', 'template_index.html')
	project_name = 'Apex Documentation'
	indexfile = ''
	scope = ['global', 'public']
	resource_css_sfdoc = os.path.join(base_path, 'css', 'sfdoc.css')
	resource_css_normalize = os.path.join(base_path, 'css', 'normalize.css')