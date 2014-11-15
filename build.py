#! /usr/bin/env python
import sys
import os
import shutil
import glob
import subprocess

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
	def __init__(self):
		pass

	def getFiles(self, location, filetype = "*"):
		return [f for f in os.listdir(location) if f.endswith(filetype)]

	def removeDir(self, location):
		shutil.rmtree(location)

	def cleanDir(self, location, filetype="*"):
		for f in self.getFiles(location, filetype) : os.remove(os.path.join(location, f))

	def copyJackToDest(self, src, dest):
		if os.path.exists(dest) :
			self.cleanDir(dest)
		else:
			os.makedirs(dest)

		for f in self.getFiles(src, ".jack"):
			shutil.copy2(os.path.join(src, f), dest)

##########
# Builder

class Builder:
	def __init__(self, env, config):
		reader = ConfigReader(env)
		self.fm = FileManager()

		self.src = reader.getKey(config.get('src'))
		self.dest = reader.getKey(config.get('dest'))
		self.c_run= reader.getKey(config.get('c_run'))

	def _prepare(self):
		self.fm.copyJackToDest(self.src, self.dest)

	def _build(self):
		# blindly run compiler command
		os.system(self.c_run + ' ../../' + self.dest)

	def _clean(self):
		self.fm.cleanDir(self.dest, ".jack")

	def run(self):
		self._prepare()
		self._build()
		self._clean()
	
##########
# Main

def main():
	try:
		
		builder = Builder(ENV, CONFIG)

		builder.run()

	except KeyboardInterrupt:
		sys.exit(0)


if __name__ == "__main__":
    main()
