import project_utils as ut
import argparse
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys

def viewer(chunk, draw_elevation=False, c=None, s=1, get=False):
	"""
	Simple function to view the point cloud using matplotlib. Takes a list of
	points as parameters.

	chunk: list of points (x,y,z)

	draw_elevation: boolean that indicates if the points should be shown in a
	3D graph (True) or in a 2D graph (False). If the points are shown in 2D,
	the third dimension will be used to color the points. 3D display takes
	more time and is often useless.

	c: list of colors. The length of c must be the same as the length of the
	chunk parameter.

	s: size of the displayed points.

	get: True if the user wants to the matplotlib object instead of showing it
	by default."""
	np_chunk = np.array(chunk)
	fig = plt.figure()
	if draw_elevation:
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(np_chunk[:,0], np_chunk[:,1], np_chunk[:,2], s=s)
	else:
		ax = fig.add_subplot(111)
		ax.grid(True,linestyle='-',color='0.75')
		if c == None:
			c = np_chunk[:,2]
		elif type(c) == int:
			c = [1]*len(np_chunk[:,0])
		ax.scatter(np_chunk[:,0], np_chunk[:,1], c=c, s=s, edgecolors='none')
	plt.xlabel('Latitude')
	plt.ylabel('Longitude')

	if get:
		return plt
	else:
		plt.show()

if "__main__" == __name__:
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help='file to display', type=str)
	parser.add_argument("--w3d", help='flag to show the points in a 3D graph', action='store_true')
	parser.add_argument("x", help='field of the file that contains the x value', type=int)
	parser.add_argument("y", help='field of the file that contains the y value', type=int)
	parser.add_argument("z", help='field of the file that contains the z value', type=int)
	args = parser.parse_args()

	field = [args.x, args.y, args.z]
	chunk = ut.loadPoints(args.file, field)
	viewer(chunk, draw_elevation=args.w3d)
