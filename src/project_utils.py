import os.path
import glob
import csv
import sys 

def loadPoints(input_file, fields):
	"""
	Function that loads a point cloud from a csv file and returns a python object.
	Each point can be loaded in a dict or in a list and this depends of the fields value.

	If 'fields' is the dict {'a': 0, 'c': 3, 'p': 1} then column 0, 3, and 1
	will be loaded from the csv input file for each row and will be associated
	with the keys (respectively) a, c and p to describe each point.

	If 'fields' is the list [1,3,4] then each row of the csv file will be
	loaded as a list of the column 1,3, and 4.
	"""
	pcd_list = []
	with open(input_file, "r") as points:
		reader = csv.reader(points)
		for line in reader:
			if type(fields) == dict:
				p = {f:float(line[fields[f]]) for f in fields}
			elif type(fields) == list:
				p = [float(line[f]) for f in fields]
			else:
				sys.stderr.write("Error: fields type not supported. Must be dict or list.\n")
			pcd_list.append(p)
	return pcd_list

def savePoints(points, output_file, fields):    
 	"""     
    Function that outputs a point cloud as a csv file. The parameter 'fields'
    allows us to save a point cloud that has been loaded as a dict or as a
    list.

    See loadPoints documentation for the 'fields' parameter possibilities.
	"""

	with open(output_file, "w") as o:
		for p in points:
			if type(fields) == dict:
				s = ','.join(map(str, [p[fields[i]] for i in fields]))
			elif type(fields) == list:
				s = ','.join(map(str, [p[i] for i in fields]))
			else:
				sys.stderr.write("Error: fields type not supported. Must be dict or list.\n")
			o.write(s + '\n')

def allFilesInDir(dir, expr="*"):
	"""
	Returns a list of all the files in a directory that match a regular
	expression.
	"""
	joinpath = os.path.abspath(os.path.abspath(dir) + "/" + expr)
	return glob.glob(joinpath)
