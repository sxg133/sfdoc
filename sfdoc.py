#!/cygdrive/c/Python27/python.exe

import sys
import os
import glob
import argparse
import apexparser
import sfdocmaker
import shutil

def parse_args():
	parser = argparse.ArgumentParser(description='Create documentation for SFDC apex code.')
	# TODO FIGURE OUT HOW TO MAKE SOURCE AND TARGET REQUIRED
	parser.add_argument('-s', '--source', metavar='--source', nargs='?', help='Source directory')
	parser.add_argument('-t', '--target', metavar='--target', nargs='?', help='Target directory')
	parser.add_argument('-p', '--pattern', metavar='--pattern', nargs='?', help='File pattern for apex classes', default="*.cls")
	args = parser.parse_args()
	return args

def get_files(dir, pattern="*.cls"):
	files = []
	os.chdir(dir)
	files = [f for f in glob.glob(pattern) if not f.endswith('Test.cls')]	# Ignoring test classes for now
	return files

args = parse_args()
currentdir = os.path.dirname(os.path.realpath(__file__))
files = get_files(args.source, args.pattern)
classes = [apexparser.parse_file(f) for f in files]
os.chdir(currentdir)
classlist = [cinfo.name for cinfo in classes]
if not os.path.exists(args.target):
	os.makedirs(args.target)
for c in classes:
	sfdocmaker.create_outfile(classlist, c, args.target + '/' + c.name + '.html')

shutil.copy('sfdoc.css', args.target)
shutil.copy('normalize.css', args.target)