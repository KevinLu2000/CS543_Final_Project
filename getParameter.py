"""
Author: Jinqi Lu
Email: jinqilu@bu.edu
Collaboration: None
Date: February 10, 2023

This is the standalone script use to automatically calculate K and N based on Epsilon and Delta provided.
This script is purely used to decide which initial parameters should be used at the beginning of experiments.

Required Lib(s): None

run:
python3 genParameter.py
"""
import math

Epsilon = 0.1
Delta = 0.05

#get k, width
def getK(Epsilon):
    return math.ceil(2.0/Epsilon)

#get N, depth or height
def getN(Delta):
    return math.ceil(math.log(1.0/Delta))

def getNt(Delta):
    return -math.log(Delta)/math.log(2)

print("Provided Epsilon: " + str(Epsilon))
print("Provided Delta: " + str(Delta))
print("Calculated width K: " + str(getK(Epsilon)))
print("Calculated height N: " + str(getN(Delta)))
