import os
import glob
import argparse
import apexparser
import sfdocmaker
import shutil
from sfdoc_settings import SFDocSettings

def parse_args():
	parser = argparse.ArgumentParser(description='Create documentation for SFDC apex code.')
	parser.add_argument('source', metavar='source_directory', help='Source directory with class files')
	parser.add_argument('target', metavar='target_directory', help='Output directory for html files')
	parser.add_argument('-p', '--pattern', metavar='pattern', nargs='?', help='File pattern for apex classes', default="*.cls")
	parser.add_argument('-n', '--name', metavar='name', nargs='?', help='Project name', default="Apex Documentation")
	parser.add_argument('-s', '--scope', metavar='scope', nargs='?', help='The lowest scope documented (public, protected, private)', default="public")
	parser.add_argument('--noproperties', action='store_true', help='Do not display class properties')
	parser.add_argument('--noindex', action='store_true', help='Do not create index file')
	parser.add_argument('--test', action='store_true', help='Do not write files, just test generator (useful if combined with verbose)')
	parser.add_argument('-v', '--verbose', metavar='verbose', nargs='?', help='Verbosity level (0=none, 1=class, 2=method, 3=param)', type=int, default=0)
	args = parser.parse_args()
	return args

def get_files(dir, pattern="*.cls"):
	files = []
	os.chdir(dir)
	files = [f for f in glob.glob(pattern) if not f.endswith('Test.cls')]	# Ignoring test classes for now
	return files

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
[source, target] = [args.source, args.target]

currentdir = os.path.dirname(os.path.realpath(__file__))
files = get_files(source, args.pattern)
classes = [apexparser.parse_file(f) for f in files]
classlist = [cinfo.name for cinfo in classes]

os.chdir(currentdir)
if not os.path.exists(target) and not SFDocSettings.test:
	os.makedirs(target)

for c in classes:
	sfdocmaker.create_outfile(classlist, c, target + '/' + c.name + '.html')

if not args.noindex:
	sfdocmaker.create_index(classes, target + '/index.html')

if not SFDocSettings.test:
	shutil.copy('sfdoc.css', target)
	shutil.copy('normalize.css', target)