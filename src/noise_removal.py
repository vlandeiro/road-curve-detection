import sys
import argparse
import project_utils as ut
import numpy as np
from cluster import *
from viewer import viewer

def noise_removal(pcd_list, ratio=0.75):

	"""
	Remove noise by keeping the largest clusters after clustering with DBScan.
	First, we keep the largest cluster C1, then we check if the size of the
	second largest cluster C2 is bigger than C1.size*ratio. If it is, we also
	keep C2 and do the test with C3, and so on.
	"""

	# Cluster the points
	clusters = cluster(pcd_list, 'dbscan', {'eps':0.00005})
	# Get the clusters sizes
	sizes = clustersSize(clusters)
	# Get the largest clust
	largest_c = getCluster(clusters, sizes[0][0])

	# For each cluster size
	for s in sizes[1:]:
		# is the present cluster bigger than the largest cluster times the
		# ratio
		if s[1] >= sizes[0][1]*ratio:
			# keep it if it is the case
			largest_c += getCluster(clusters, s[0])
		else:
			break

	return largest_c


if "__main__" == __name__:
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help='input file that contains the point cloud', type=str)
	parser.add_argument("output", help='path to the output file', type=str)
	parser.add_argument("--slice", "-s", help='slice size (default: 15000)', type=int, default=15000)
	args = parser.parse_args()

	# Load input file
	pcd_list = ut.loadPoints(args.input, [2,3,4])

	# Compute the number of iterations to do given the slice size
	to_process = len(pcd_list)
	slice_size = args.slice
	iterations = to_process/slice_size
	if (iterations == 0 or to_process%slice_size == 0):
		iterations += 1
	largest_clusters = []
	i = 0

	for i in range(iterations):
		begin = i*slice_size
		if (i+1)*slice_size < to_process:
			end = (i+1)*slice_size
		else:
			end = to_process 
		# Get the largest clusters
		largest_clusters += noise_removal(pcd_list[begin:end], ratio=0.1)
	largest_clusters = np.array(largest_clusters)
	
	ut.savePoints(largest_clusters, args.output, [0,1,2])
	viewer(largest_clusters, c=largest_clusters[:,2], s=2)
