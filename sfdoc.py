#!/cygdrive/c/Python27/python.exe

import sys
import os
import glob
import argparse
import apexparser

def parseArgs():
	parser = argparse.ArgumentParser(description='Create documentation for SFDC apex code.')
	# TODO FIGURE OUT HOW TO MAKE SOURCE AND TARGET REQUIRED
	parser.add_argument('-s', metavar='--source', nargs='?', help='Source directory')
	parser.add_argument('-t', metavar='--target', nargs='?', help='Target directory')
	parser.add_argument('-p', metavar='--pattern', nargs='?', help='File pattern for apex classes', default="*.cls")
	args = parser.parse_args()
	return args

def getFiles(dir, pattern="*.cls"):
	files = []
	os.chdir(dir)
	for f in glob.glob(pattern):
		files.append(f)
	return files

args = parseArgs()
files = getFiles(args.s, args.p)
apexparser.parseFile(files[0])