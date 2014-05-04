import cv2
import project_utils as ut
import argparse
import numpy as np
import sys
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from sklearn.cluster import Ward
from sklearn.cluster import MeanShift, estimate_bandwidth
from viewer import viewer
from collections import Counter

def cluster(pcd_list, method_str="dbscan", options={}):
	"""
	Take a 3-d list of points (x,y,z) and a clustering method and returns the
	clusters obtained when this method is applied.

	pcd_list is a list of points

	method_str is a string describing the method to use to cluster

	options is the options dictionary used by some scikit clustering
	functions
	"""
	if method_str == "kmeans":
		method = KMeans
	elif method_str == "affinity":
		method = AffinityPropagation
	elif method_str == "dbscan":
		method = DBSCAN
	elif method_str == "ward":
		method = Ward
	elif method_str == "meanshift":
		method = MeanShift
	else:
		sys.stderr.write("Error: Unsupported clustering method_str.\n")
		exit(0)

	# Keep two dimensions only to compute cluster (remove elevation)
	pcd_list = np.array(pcd_list)[:,:2]

	# Build the estimator with the given options
	estimator = method(**options)

	# Fit the estimator
	estimator.fit(pcd_list)

	# Get the labels and return the labeled points
	labels = estimator.labels_
	clusters = np.append(pcd_list, np.array([labels]).T, 1)

	return clusters

def getCluster(clusters, i, label_field=2):
	"""
	Return the points belonging to a given cluster.

	clusters: list of labeled points where labels are the cluster ids

	i: id of the cluster to get

	label_field: field where the cluster id is stored in the list of labeled
	points

	"""
	return [c.tolist() for c in clusters if c[label_field] == i]

def clustersSize(clusters):
	"""
	Return the size of the clusters given a list of labeled points.
	"""
	labels = clusters[:,2]
	counter = Counter(labels)
	return counter.most_common()

if "__main__" == __name__:
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help='path to the point cloud file to cluster', type=str)
	parser.add_argument("-n", help='number of clusters to create (not used in DBSCAN)', type=int, default=3)
	parser.add_argument("--meth", "-m", dest="meth", help='method used to cluster (default: dbscan)', type=str, default="dbscan")
	parser.add_argument("--eps", help='epsilon value for DBSCAN (default: 0.00005)', type=float, default=0.00005)
	args = parser.parse_args()

	method = args.meth
	if method == "kmeans":
		sys.stderr.write("Clustering with K-Means method...\n")
		options = {'init':'random', 'n_clusters':args.n, 'n_jobs':-1, 'n_init':10}
	elif method == "affinity":
		sys.stderr.write("Clustering with Affinity Propagation method...\n")
		options = {'preference':-50}
	elif method == "dbscan":
		sys.stderr.write("Clustering with DBScan method...\n")
		options = {'eps':args.eps}
	elif method == "ward":
		sys.stderr.write("Clustering with Ward method...\n")
		options = {'n_clusters':args.n}
	elif method == "meanshift":
		sys.stderr.write("Clustering with Mean Shift method...\n")
		options = {'bandwidth':bandwidth, 'bin_seeding':True}
	else:
		sys.stderr.write("Error: Unsupported clustering method.\n")
		exit(0)

	# Load file
	pcd_list = ut.loadPoints(args.file, [2,3,4])

	# Cluster the points
	clusters = cluster(pcd_list, method, options)
	# Show the clusters
	viewer(clusters, draw_elevation=False, c=clusters[:,2])
