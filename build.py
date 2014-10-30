#! /usr/bin/env python
import sys
import os
import shutil
import glob

try:
	import configparser
except ImportError:
	import ConfigParser as configparser

DEFAULT_ENV = "DEFAULT"

E_USAGE = ('Usage: %s <environment>' % sys.argv[0])
NUM_ARVS = 1

#fail-fast for any but 1 commmand-line inputs
if len(sys.argv) > 1:
	ENV = os.path.normpath(sys.argv[1])
else:
	ENV = DEFAULT_ENV


CONFIG = {
	'src' : 'SourceDirectory',
	'dest' : 'OutputDirectory',
	'c_loc' : 'CompilerLocation',
	'c_run' : 'CompilerRunCommand'
}

###########
# Config Reader

class ConfigReader:
	def __init__(self, env):
		self.env = env
		self.config = configparser.ConfigParser()
		self.config.read('build.config')


	def getKey(self, key):
		return self.config.get(self.env, key)


##########
# FileManager

class FileManager:

	def getFiles(self, location):
		return glob.glob(location)

	def cleanDir(self, location):
		for f in self.getFiles(location) : os.remove(f)

	def copyJackToDest(self, src, dest):
		if os.path.exists(dest) :
			fm.cleanDir(dest)
		else:
			os.makedirs(dest)

		for f in self.getFiles(src):
				shutil.copy(f, dest)


##########
# Main

def _prepare(reader):
	fm = FileManager()

	src = reader.getKey(CONFIG.get('src'))
	dest = reader.getKey(CONFIG.get('dest'))

	fm.copyJackToDest(src, dest)


def _build(reader):
	c_loc = reader.getKey(CONFIG.get('c_loc'))
	c_run = reader.getKey(CONFIG.get('c_run'))
	dest = reader.getKey(CONFIG.get('dest'))

	print c_run + ' ' + dest

def run(reader):
	_prepare(reader)
	_build(reader)

def main():
	try:
		
		reader = ConfigReader(ENV)

		run(reader)

	except KeyboardInterrupt:
		sys.exit(0)


if __name__ == "__main__":
    main()
