import os
import argparse
import apexparser
import sfdocmaker
import shutil
from sfdoc_settings import SFDocSettings
import re
import fnmatch

def parse_args():
	"""Returns parsed command line arguments."""
	parser = argparse.ArgumentParser(description='Create documentation for SFDC apex code.')
	parser.add_argument('source', metavar='source_directory', help='Source directory with class files')
	parser.add_argument('target', metavar='target_directory', help='Output directory for html files')
	parser.add_argument('-p', '--pattern', metavar='pattern', nargs='?', help='File pattern for apex classes', default="*.cls")
	parser.add_argument('-tp', '--testpattern', metavar='testpattern', nargs='?', help='File pattern for apex classes', default="*Test.cls")
	parser.add_argument('-r', '--regex', action='store_true', help='The specified patterns are regular expressions')
	parser.add_argument('-n', '--name', metavar='name', nargs='?', help='Project name', default="Apex Documentation")
	parser.add_argument('-s', '--scope', metavar='scope', nargs='?', help='The lowest scope documented (public, protected, private)', default="public")
	parser.add_argument('--noproperties', action='store_true', help='Do not display class properties')
	parser.add_argument('--nomethodlist', action='store_true', help='Do not display method sidebar')
	parser.add_argument('--noindex', action='store_true', help='Do not create index file')
	parser.add_argument('--test', action='store_true', help='Do not write files, just test generator (useful if combined with verbose)')
	parser.add_argument('-v', '--verbose', metavar='verbose', nargs='?', help='Verbosity level (0=none, 1=class, 2=method, 3=param)', type=int, default=0)
	args = parser.parse_args()
	return args

def get_files(dir, pattern="*.cls", test_pattern="*Test.cls", is_regex=False):
	"""Return a list of files.

	Keyword arguments:
	dir 		-- The directory to retrieve files from
	pattern 	-- Pattern file names must match.
	is_regex	-- Is the specified pattern a regular expression?

	"""
	files = []

	if is_regex:
		re_file = re.compile(pattern)

	for f in os.listdir(dir):
		if is_regex and re_file.match(f) and not re_file.match(f):
			files.append( os.path.join(dir, f) )
		elif not is_regex and fnmatch.fnmatchcase(f, pattern) and not fnmatch.fnmatchcase(f, test_pattern):
			files.append( os.path.join(dir, f) )

	return files

# set the settings based on defaults and command line arguments
args = parse_args()
SFDocSettings.verbose = args.verbose
SFDocSettings.test = args.test
SFDocSettings.indexfile = 'index.html' if not args.noindex else ''
SFDocSettings.project_name = args.name
if args.scope.lower() == 'protected':
	SFDocSettings.scope = ['public', 'protected']
elif args.scope.lower() == 'private':
	SFDocSettings.scope = ['public', 'protected', 'private']
SFDocSettings.no_properties = args.noproperties
SFDocSettings.no_method_list = args.nomethodlist
[source, target] = [args.source, args.target]

# get files, parse them, and create class info objects
files = get_files(source, args.pattern, args.testpattern, args.regex)
classes = [apexparser.parse_file(f) for f in files]
classlist = [cinfo.name for cinfo in classes]

if not os.path.exists(target) and not SFDocSettings.test:
	os.makedirs(target)

for c in classes:
	sfdocmaker.create_outfile(classlist, c, target + '/' + c.name + '.html')

if not args.noindex:
	sfdocmaker.create_index(classes, target + '/index.html')

if not SFDocSettings.test:
	shutil.copy('css/sfdoc.css', target)
	shutil.copy('css/normalize.css', target)