#! /usr/bin/python2

import os
import sys
import re

E_USAGE = ('Usage: %s <input>' % sys.argv[0])
NUM_ARVS = 4

#fail-fast for any but 1 commmand-line inputs
if len(sys.argv) is not NUM_ARVS:
	print E_USAGE
	sys.exit(2)

TEMPLATE = os.path.normpath(sys.argv[1])
INPUT = os.path.normpath(sys.argv[2])
OUTPUT = os.path.normpath(sys.argv[3])

class JackGenerator:
	def __init__(self, num_points):
		self.output = "let numPoints = %d;\n" % num_points
		self.output += "let data = Array.new(numPoints);\n"
		self.count = 0;

	def addRow(self, locations):
		self.output += "let temp = Array.new(%d);\n" % (len(locations) + 1)
		self.output += "let temp[0] = %d;\n" % (len(locations) + 1)
		for index, l in enumerate(locations):
			s = "let temp[%d] = %d;\n" % (index+1, l)
			self.output += s

		self.output += "let data[%d] = temp;\n" % self.count
		self.count += 1

class MapReader:
	def __init__(self, filename):
		self.inputfile = open(filename)
		self.lines = []

		self.readMap()

		self.inputfile.close()

	def readMap(self):

		for line in self.inputfile:
			locations = [m.start() for m in re.finditer('\|', line)]
			self.lines.append(locations)

def write_yield(data):
	infile = open(TEMPLATE)	
	outfile = open(OUTPUT, "w")
	
	for l in infile:
		if "%yield" in l:
			l = l.replace("%yield", data)
		outfile.write(l)

	infile.close()
	outfile.close()


##########
# Main

def main():
	try:
		reader = MapReader(INPUT)

		gen = JackGenerator(len(reader.lines))

		for l in reader.lines:
			gen.addRow(l)

		write_yield(gen.output)	

	except KeyboardInterrupt:
		sys.exit(0)


if __name__ == "__main__":
    main()






