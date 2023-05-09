"""
Author: Jinqi Lu
Email: jinqilu@bu.edu
Collaboration: None
Date: May 02, 2023

This is the helper script contains various helper methods.
This file is required for the major components of the CMS program to run.
This file is not intended to be run directly via CMD.

Required Lib(s): progressbar (remove this will not affect the functionality)

run:
This script does not run
"""

import random,progressbar, operator
from collections import defaultdict
import hashlib, zlib, progressbar
encoding = "utf-8"
#write a specific file to a system location with content
def writefile(filename, content, print_progress = True):
    res = open(filename, "w")
    if(print_progress):
        lenf1 = len(content)
        bar = progressbar.ProgressBar(maxval=lenf1, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        cnt = 0
        for i in content:
            res.write(str(i))
            res.write("\n")
            cnt += 1
            bar.update(cnt)
        bar.finish()
    else:
        for i in content:
            res.write(str(i))
            res.write("\n")
    res.close()

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
    for i in range(n):
        if (i == 0):
            res.append(hash_one(str ,k))
        elif(i == 1):
            res.append(hash_two(str, k))
        elif( i == 2):
            res.append(hash_three(str, k))
        elif(i == 3):
            res.append(hash_four(str, k))
    return res

#return content of a single file as list
def get_list_from_file(fdir):
    file1 = open(fdir, 'r', encoding='utf8')
    Lines = file1.read().splitlines()
    return Lines

#get random digit
def get_random():
    return random.random()

def get_zero():
    return 0
#get a dictionary of list of element where key is the element string and value is the exact count:
def get_exact_count(inputlist):
    res = defaultdict(get_zero)
    for i in inputlist:
        res[i] += 1
    return res

#get actual x top hitters
def get_top_hitters(x, table = [], inputlist = []):
    exact_count = get_exact_count(inputlist) if table == [] else table
    sorted_table = dict(sorted(exact_count.items(), key=operator.itemgetter(1), reverse=True))
    res = []
    cnt = 0
    for key in sorted_table:
        res.append(key)
        cnt += 1
        if(cnt == x):
            break
    return res

#get rate of correctness for heavy hitters
def get_correct_rate(actual, mg, round_digits):
    correct = 0
    for i in mg:
        if(i in actual):
            correct += 1
    return round(correct/len(mg),round_digits)

#function to get the occurence count of a string
def get_count_cms(str, cms_table, k, n):
    keys = get_hash(str, k, n)
    reslist = []
    for i in range(n):
        reslist.append(cms_table[i, keys[i]])
    #get the min count
    res = min(reslist)
    return res

#get the top x heavy hitters for CMS
def get_top_hitters_cms(cms_table, inputlist, x, k, n):
    #get each element's occurrence in CMS first
    keys = list(get_exact_count(inputlist).keys())
    #dict of str and count
    cms_dict = {}
    for i in keys:
        cms_dict[i] = get_count_cms(i,cms_table, k, n)
    return get_top_hitters(x,cms_dict)