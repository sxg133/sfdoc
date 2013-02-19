import sys
import os
import glob
import argparse
import apexparser
import sfdocmaker
import shutil

def parse_args():
	parser = argparse.ArgumentParser(description='Create documentation for SFDC apex code.')
	parser.add_argument('dirs', metavar='directories', nargs=2, help='Source and target directories')
	parser.add_argument('-p', '--pattern', metavar='pattern', nargs='?', help='File pattern for apex classes', default="*.cls")
	parser.add_argument('-n', '--name', metavar='name', nargs='?', help='Project name', default="Apex Documentation")
	args = parser.parse_args()
	return args

def get_files(dir, pattern="*.cls"):
	files = []
	os.chdir(dir)
	files = [f for f in glob.glob(pattern) if not f.endswith('Test.cls')]	# Ignoring test classes for now
	return files

args = parse_args()
[source, target] = args.dirs;
currentdir = os.path.dirname(os.path.realpath(__file__))
files = get_files(source, args.pattern)
classes = [apexparser.parse_file(f) for f in files]
os.chdir(currentdir)
classlist = [cinfo.name for cinfo in classes]
if not os.path.exists(target):
	os.makedirs(target)
for c in classes:
	sfdocmaker.create_outfile(classlist, c, target + '/' + c.name + '.html', project_name=args.name)
sfdocmaker.create_index(classes, target + '/index.html', project_name=args.name)

shutil.copy('sfdoc.css', target)
shutil.copy('normalize.css', target)