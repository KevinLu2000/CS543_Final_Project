"""
Author: Jinqi Lu
Email: jinqilu@bu.edu
Collaboration: None
Date: May 02, 2023

This is the main script file that contains the implementation of Misra-Gries
and a simulation function. The simulation function is used to test the difference
of MG and the actual probability of a given dataset.
Some other helper functions was defined in helper.py
Only the global variables were supposed to be edited for experimental purposes.

Required Lib(s): hashlib, zlib, numpy, progressbar, matplotlib and helper files

run:
python3 Misra-Gries.py
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
K = 4400
#Top X heavy hitters
top_x = 25
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
draw_graph_switch = True
#################################################################
file_path = ""

#hash one, input the str and bucket length K, output a integer of length K.
#This function uses MD5 to get the first hash.
def hash_one(str, k):
    #get md5
    md5_hex = hashlib.md5(str.encode(encoding)).hexdigest()
    #convert hex md5 to 10 base.
    md5_10 = int(md5_hex, 16)
    #take mod, get the required length.
    key = md5_10 % k
    #return the result
    return key

#hash two, input the str and bucket length K, output a integer of length K.
#This function uses SHA256 to get the second hash.
def hash_two(str, k):
    #get SHA256
    sha_hex = hashlib.sha256(str.encode(encoding)).hexdigest()
    #convert hex SHA256 to 10 base.
    sha_10 = int(sha_hex, 16)
    #take mod, get the required length.
    key = sha_10 % k
    #return the result
    return key

#hash three, input the str and bucket length K, output a integer of length K.
#This function uses SHA256 to get the third hash.
def hash_three(str, k):
    #get SHA256
    sha_hex = hashlib.sha1(str.encode(encoding)).hexdigest()
    #convert hex SHA256 to 10 base.
    sha_10 = int(sha_hex, 16)
    #take mod, get the required length.
    key = sha_10 % k
    #return the result
    return key

#hash four, input the str and bucket length K, output a integer of length K.
#This function uses CRC32 to get the third hash.
def hash_four(str, k):
    #get CRC32
    crc = zlib.crc32(str.encode(encoding))
    #take mod, get the required length.
    key = crc % k
    #return the result
    return key

#function to get keys for a str
def get_hash(str, k, n):
    res = []
    if (n == 0):
        res.append(hash_one(str ,k))
    elif(n == 1):
        res.append(hash_two(str, k))
    elif( n == 2):
        res.append(hash_three(str, k))
    elif(n == 3):
        res.append(hash_four(str, k))
    return res[0]

#decrease all counters by one and remove empty
def decrease_counters(mg_table):
    keysList = list(mg_table.keys())
    for key in keysList:
        #decrease first
        mg_table[key] -= 1
        if(mg_table[key] == 0):
            mg_table.pop(key, None)
    return mg_table
#update and return table with hash
def update_table(mg_table, str, k):
    #get key
    #key = get_hash(str, k, n)
    #mg core
    #increase counter by one if existed
    if str in mg_table:
        mg_table[str] += 1
    #key not present and empty space available
    elif( str not in mg_table and len(mg_table)<=k):
        mg_table[str] = 1
    #key not present and empty space not available
    else:
        mg_table = decrease_counters(mg_table)
    return mg_table

#update table for all elements
#inputlist, table/dict, width, index of used hash
def update_wrapper(str_list, mg_table, k):
    lenf1 = len(str_list)
    print("Total number of elements: " + str(lenf1))
    bar = progressbar.ProgressBar(maxval=lenf1, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    cnt = 0
    for i in str_list:
        mg_table = update_table(mg_table, i, k)
        cnt += 1
        bar.update(cnt)
    bar.finish()
    return mg_table

def MG(k, flist):
    mg_table = {}
    #run exp
    mg_table = update_wrapper(flist,mg_table,k)
    return mg_table

#get to x hitters
def get_count_mg(mg_table, x):
    topx = get_top_hitters(x, mg_table)
    return topx

#show the graph
def draw_graph(X,Y_exp,Y_cms):
    print("Generating Graphs.... This may take a while depending on your system performance and dataset size.")
    tres = ""
    graph_name = ""
    if(use_real_data):
        tres = " using real-world data"
        graph_name = "realK" + str(K)
    else:
        tres = " K = " + str(K) + " using artificial data"
        graph_name = "artK" + str(K)
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

#Run simulation to compare the MG and exact data
def RunSimulation(k, file_path, print_details = False):
    print("Running experiments...")
    dmsg = ""
    if(use_real_data):
        dmsg ="Using real world data..."
    else:
        dmsg = "Using artificial data..."
    #result
    #read file
    flist = get_list_from_file(file_path)
    #get the actual top x heavy hitters
    actual_topx = get_top_hitters(top_x,[],flist)
    actual_topx.sort()
    #get the MG table
    mg_table = MG(k, flist)
    #get the heavy hitters by MG
    mg_topx = get_top_hitters(top_x,mg_table)
    mg_topx.sort()
    #print(mg_topx)
    ##print(len(mg_topx))
    #print(actual_topx)
    #print(len(actual_topx))
    print("########################### Misra-Gries SIMULATION REPORT ###########################")
    print(dmsg)
    print("\n### PARAMETERS ###")
    print("Max Length of Dictionary: " + str(k))
    print("Comparing Top " + str(top_x) + " heavy hitters.")
    print("Space Used: " + str(k))
    print("\n### RESULT ###")
    if(print_details):
        print("Actual top hitters: ")
        print(actual_topx)
        print("MG top hitters: ")
        print(mg_topx)
    print("Number of actual top hitters: " + str(len(actual_topx)))
    print("Number of MG top hitters: " + str(len(mg_topx)))
    print("Percentage of corrected identified heavy hitters: " + str(get_correct_rate(actual_topx,mg_topx,round_digits)))
    return

#Run a test simulation
def main():
    global file_path,real_data,artificial_data,use_real_data
    #klist = [50,75,100,150,200,400,600,700,750,800,850,900,950,1000,1050,1200,1300,1400,1500,1700,1750,1800,1850,1900,2000,2500,3000,4000,4350,4400]
    klist = [1000]
    if(use_real_data != None):
        #update data path
        if(use_real_data):
            file_path = real_data
        else:
            file_path = artificial_data
        #key level details will not be print when using real world data as it will be too large
        for i in klist:
            RunSimulation(i,file_path)
            input()
    else:
        #run for real data
        use_real_data = True
        file_path = real_data
        RunSimulation(K, file_path)
        #run for artificial data
        use_real_data = False
        file_path = artificial_data
        RunSimulation(K, file_path)

if __name__ == '__main__':
    main()

