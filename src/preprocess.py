import argparse
import sys
import numpy as np
import project_utils as ut
import os.path

def filterPoints(pcd_list, options):
	"""
	Function that filters a given list of points with the given options.

	pcd_list is a list of points.

	options is a dict of filters, the possible keys are:
		- minlat \ filter on the
		- maxlat / latitude value
		- minlon \ filter on the
		- maxlon / longitude value
		- minele \ filter on the
		- maxele / elevation value
		- minval \ filter on the
		- maxval / elevation value
	"""
	filtered_list = []
	if "minlat" in options:
		filtered_list = filter(lambda pcd: pcd["lat"] >= options["minlat"], pcd_list)
		pcd_list = filtered_list
	if "maxlat" in options:
		filtered_list = filter(lambda pcd: pcd["lat"] <= options["maxlat"], pcd_list)
		pcd_list = filtered_list
	if "minlon" in options:
		filtered_list = filter(lambda pcd: pcd["lon"] >= options["minlon"], pcd_list)
		pcd_list = filtered_list
	if "maxlon" in options:
		filtered_list = filter(lambda pcd: pcd["lon"] <= options["maxlon"], pcd_list)
		pcd_list = filtered_list
	if "minele" in options:	
		filtered_list = filter(lambda pcd: pcd["ele"] >= options["minele"], pcd_list)
		pcd_list = filtered_list
	if "maxele" in options:
		filtered_list = filter(lambda pcd: pcd["ele"] <= options["maxele"], pcd_list)
		pcd_list = filtered_list
	if "minval" in options:
		filtered_list = filter(lambda pcd: pcd["val"] >= options["minval"], pcd_list)
		pcd_list = filtered_list
	if "maxval" in options:
		filtered_list = filter(lambda pcd: pcd["val"] <= options["maxval"], pcd_list)
		pcd_list = filtered_list
	return filtered_list

def getChunksList(pcd_dir):
	"""
	Returns all files that contain a chunk of point for the project.
	"""
	chunk_dirs = ut.allFilesInDir(pcd_dir)
	chunks = []
	for d in chunk_dirs:
		chunks += ut.allFilesInDir(d, "dump[0-9]*")
	return chunks

if "__main__" == __name__:
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help='path to the file or directory to process', type=str)
	parser.add_argument("output", help='path to the output file', type=str)
	parser.add_argument("--file", "-f", help='flag that indicates that the input is a file and not a directory', action="store_true")
	args = parser.parse_args()
	
	if args.file:
		chunks = [args.input]
	else:
		chunks = getChunksList(args.input)

	i = 0.
	l = float(len(chunks))

	# initialize options for the filter
	options = {}

	# filter on the intensity of the points
	# let's keep points that have an intensity value > 190

	options["minval"] = 190

	sys.stderr.write("Loading and filtering " + str(int(l)) + " chunks...\n")

	filtered_list = []
	fields_in = {'id':0, 'lidar_id':1, 'lat':2, 'lon':3, 'ele':4, 'val': 5}
	fields_out = {0:'id', 1:'lidar_id', 2:'lat', 3:'lon', 4:'ele', 5:'val'}

	for c in chunks:
		pcd_list = ut.loadPoints(c, fields_in)
		# filter on elevation by getting the points between the 35th
		# percentile and the 65th percentile for each chunk
		elevations = [pcd["ele"] for pcd in pcd_list]
		options["minele"] = np.percentile(elevations, 35)
		options["maxele"] = np.percentile(elevations, 65)

		filtered_list += filterPoints(pcd_list, options)
		i += 1.
		sys.stderr.write("%.2f\r" % float(100*i/l))

	sys.stderr.write("\nDone\n")

	ut.savePoints(filtered_list, args.output, fields_out)
