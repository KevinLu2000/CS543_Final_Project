"""
Author: Jinqi Lu
Email: jinqilu@bu.edu
Collaboration: None
Date: May 02, 2023

This is the main script file that contains the implementation of Count-Min Sketch
and a simulation function. The simulation function is used to test the difference
of CMS and the actual probability of a given dataset.
Some other helper functions was defined in helper.py
Only the global variables were supposed to be edited for experimental purposes.

Required Lib(s): hashlib, zlib, numpy, progressbar, matplotlib and helper files

run:
python3 CountMinSketch.py
"""

import hashlib, zlib, progressbar
import numpy as np
from helper import *
import matplotlib.pyplot as plt

####################### Global Variables #######################
encoding = "utf-8"
artificial_data = "Data/aData.txt"
real_data = "Data/Fnums.txt"
graph_dir = "Graphs/"
#set to true to use real data, false to use artificial data, and None to use both(run both datasets in series with same parameters.).
use_real_data = True
#bucket width
K = 1100
#Top X heavy hitters
top_x = 25
#number of hash functions (up to 4)
N = 4
#round digits for percentage
round_digits = 4
#number of overestimates details to be print. if total number of error goes over this, all the error details will be omitted
#to avoid spamming the console.
num_print_over_counts = 20
#DPI of output graphs
graph_dpi = 300
#graph height inches
graph_height = 5
#graph width inches
graph_width = 15
#draw graph switch
draw_graph_switch = False
#################################################################
file_path = ""

#update and return table with hash
def update_table(cms_table, str, k, n):
    #get keys
    keys = get_hash(str, k, n)
    for i in range(n):
        cms_table[i, keys[i]] += 1
    return cms_table

#update table for all elements
def update_wrapper(str_list, cms_table, k, n):
    lenf1 = len(str_list)
    print("Total number of elements: " + str(lenf1))
    bar = progressbar.ProgressBar(maxval=lenf1, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    cnt = 0
    for i in str_list:
        cms_table = update_table(cms_table, i, k, n)
        cnt += 1
        bar.update(cnt)
    bar.finish()
    return cms_table

def CMS(k, flist, n):
    cms_table = np.zeros([n,k])
    #run exp
    cms_table = update_wrapper(flist,cms_table,k, n)
    return cms_table



#show the graph
def draw_graph(X,Y_exp,Y_cms):
    print("Generating Graphs.... This may take a while depending on your system performance and dataset size.")
    tres = ""
    graph_name = ""
    if(use_real_data):
        tres = "N = " + str(N) + " K = " + str(K) + " using real-world data"
        graph_name = "realN" + str(N) + "K" + str(K)
    else:
        tres = "N = " + str(N) + " K = " + str(K) + " using artificial data"
        graph_name = "artN" + str(N) + "K" + str(K)
    plt.title(tres)
    plt.plot(X,Y_exp, label = "Actual counts")
    plt.plot(X,Y_cms, label = "CMS counts")
    plt.xlabel("Elements")
    plt.ylabel("Counts")
    plt.legend()
    final_dir = graph_dir + graph_name + ".png"
    plt.gcf().set_size_inches(graph_width, graph_height)
    plt.savefig(final_dir, dpi = graph_dpi)
    print("Graph saved to " + final_dir)
    plt.close()
    return

#Run simulation to compare the CMS and exact data
def RunSimulation(k, file_path, n, print_details = False):
    print("Running experiments...")
    dmsg = ""
    if(use_real_data):
        dmsg ="Using real world data..."
    else:
        dmsg = "Using artificial data..."
    #result
    res_str = []
    res_exact = []
    res_cms = []
    #read file
    flist = get_list_from_file(file_path)
    #get dict of exact elements & occurrences.
    exact_count = get_exact_count(flist)
    #get the CMS table
    cms_table = CMS(k, flist, n)
    #update the counts of different methods (cms & exact)
    for key, value in exact_count.items():
        res_str.append(key)
        res_exact.append(value)
        res_cms.append(int(get_count_cms(key,cms_table,k, n)))
    total_len = len(res_str)
    #get the actual top hitters
    actual_topx = get_top_hitters(top_x, [], flist)
    actual_topx.sort()
    #get the CMS top hitters
    cms_topx = get_top_hitters_cms(cms_table,flist,top_x,k,n)
    cms_topx.sort()
    print("\n################## Count-Min Sketch SIMULATION REPORT ##################\n")
    print(dmsg)
    print("\n### PARAMETERS ###")
    print("Number of hash functions used (N): " + str(n))
    print("Width of bucket (K): " + str(k))
    print("Comparing Top " + str(top_x) + " heavy hitters.")
    print("Space Used: " + str(k*n))
    print("\n### RESULT ###")
    if (print_details):
        print("Actual top hitters: ")
        print(actual_topx)
        print("CMS top hitters: ")
        print(cms_topx)
    print("Number of actual top hitters: " + str(len(actual_topx)))
    print("Number of CMS top hitters: " + str(len(cms_topx)))
    print("Percentage of corrected identified heavy hitters: " + str(
        get_correct_rate(actual_topx, cms_topx, round_digits)))
    #generate a graph showing overestimating of each item
    if(draw_graph_switch):
        draw_graph(res_str,res_exact,res_cms)

#Run a test simulation
def main():
    global file_path,real_data,artificial_data,use_real_data
    klist = [100,200,400,600,700,800,900,1000,1200,1300,1500,1800,1900,2000,2500,3000,4000]
    klist = [1000]
    if(use_real_data != None):
        #update data path
        if(use_real_data):
            file_path = real_data
        else:
            file_path = artificial_data
        #key level details will not be print when using real world data as it will be too large
        for i in klist:
            RunSimulation(i//N,file_path,N)
            input()
    else:
        #run for real data
        use_real_data = True
        file_path = real_data
        RunSimulation(K, file_path, N)
        #run for artificial data
        use_real_data = False
        file_path = artificial_data
        RunSimulation(K, file_path, N)

if __name__ == '__main__':
    main()

