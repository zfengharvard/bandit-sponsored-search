############ 
# Coordinates the gsp and the bidder modules
############ 

import numpy as np
import random
import math
from bidder import *
from value_module import *
from gsp import GSP

num_bidders         = 5
num_repetititions   = 10 #how many times each T will be repeated  
max_num_rounds      = 10
min_num_rounds      = 1
T                   = 10

# Preferred Discretizations for the bidders
epsilon = []
for i in range(0,num_bidders-1):
    epsilon.append(0.1)

# Create the bidders and store them in a list
bidder = [] #list of bidder objects
for i in range(0,num_bidders-1):
    bidder.append(Bidder(i, epsilon[i]))

    



