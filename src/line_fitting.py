import numpy as np
import argparse
import project_utils as ut
import matplotlib.pyplot as plt
from viewer import viewer

if "__main__" == __name__:
    """
    Compute fitting polynoms for a given point cloud and print them over the point cloud.

    input: input file containing the point cloud
    degree: degree of the fitting polynoms
    slice: size of the chunks to slice the data in order to process it faster
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='path to the input file', type=str)
    parser.add_argument("--degree", "-d", help='degree of the fitting polynoms (default: 3)', type=int, default=3)
    parser.add_argument("--slice", "-s", help='size of the chunks (default: 20000)', type=int, default=20000)
    args = parser.parse_args()

    # Load input file
    pcd_list = np.array(ut.loadPoints(args.input, [0,1,2]))

    # Compute the number of iterations to do given the slice size
    to_process = len(pcd_list)
    slice_size = args.slice
    iterations = to_process/slice_size
    if (iterations == 0 or to_process%slice_size == 0):
        iterations += 1

    # Initialize the iteration variable
    i = 0
    
    # Get the matplotlib object that shows the point cloud
    plt = viewer(pcd_list, get=True)
    # Compute the fitting polynoms and plot them
    for i in range(iterations):
        begin = i*slice_size
        if (i+1)*slice_size < to_process:
            end = (i+1)*slice_size
        else:
            end = to_process 
        points_slice = pcd_list[begin:end]
        xp = np.linspace(points_slice[0,0], points_slice[end-begin-1,0], 100)
        pl = np.poly1d(np.polyfit(points_slice[:,0], points_slice[:,1], args.degree))
        plt.plot(xp, pl(xp), 'r-', linewidth=3.0)

    plt.show()
