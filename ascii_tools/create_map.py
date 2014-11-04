#! /usr/bin/python2

import os
import sys

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
		self.output = "let numPoints = " + `num_points` + ";\n"
		self.output += "let data = Array.new(numPoints);\n"
		self.point_count = 0;


	def addPoint(self, x, y):
		self.output += "let temp = Array.new(2);\n"
		self.output += "let temp[0] = " + `x` + ";\n"
		self.output += "let temp[1] = " + `y` + ";\n"
		self.output += "let data["+`self.point_count`+"] = temp;\n"
#		self.output += "do temp.dispose();\n"

		self.point_count += 1

class MapReader:
	def __init__(self, filename):
		self.inputfile = open(filename)
		self.x = 0;
		self.y = 0;
		self.y_count = 0;
		self.points = []

		self.readMap()

		self.inputfile.close()

	def readMap(self):
		while True:
			c = self.inputfile.read(1)
			if not c:
				break
			if c.isspace():
				self.x += 8
			if "\n" in c:
				self.y_count += 1
				if (self.y_count >= 16):
					self.y = 0
					self.y_count = 0
				else:
					self.y += 15
				self.x = 0
			if c == "|":
				self.points.append([self.x, self.y])
				self.x += 8



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

		gen = JackGenerator(len(reader.points))
		for point in reader.points:
			gen.addPoint(point[0], point[1])

		write_yield(gen.output)	

	except KeyboardInterrupt:
		sys.exit(0)


if __name__ == "__main__":
    main()






