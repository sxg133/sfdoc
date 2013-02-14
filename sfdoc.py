#!/cygdrive/c/Python27/python.exe

import sys
import os
import glob
import argparse
import apexparser

def parse_args():
	parser = argparse.ArgumentParser(description='Create documentation for SFDC apex code.')
	# TODO FIGURE OUT HOW TO MAKE SOURCE AND TARGET REQUIRED
	parser.add_argument('-s', metavar='--source', nargs='?', help='Source directory')
	parser.add_argument('-t', metavar='--target', nargs='?', help='Target directory')
	parser.add_argument('-p', metavar='--pattern', nargs='?', help='File pattern for apex classes', default="*.cls")
	args = parser.parse_args()
	return args

def get_files(dir, pattern="*.cls"):
	files = []
	os.chdir(dir)
	files = [f for f in glob.glob(pattern) if not f.endswith('Test.cls')]	# Ignoring test classes for now
	return files

args = parse_args()
files = get_files(args.s, args.p)
classes = [apexparser.parse_file(f) for f in files]