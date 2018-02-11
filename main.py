
import numpy as np
import random
from gsp import GSP


### Test the GSP module

reserve = 0.1
num_bidder = 5
num_slots = 3
#ctr = [0.6, 0.5, 0.3]

#score = [0.2, 0.3, 0.25, 0.3, 0.4]

#bids = [2.0, 3.0, 4.0, 2.0, 3.0]

score = [0.700573810327246, 0.3110979655260716, 0.610430432163001, 0.03395812562678002, 0.8345253204018921]
bids = [0.6, 0.0, 0.2, 0.1, 0.4]
ctr  = [0.97, 0.9, 0.57]


l = [GSP(ctr, reserve, bids, score, num_slots, num_bidder).alloc_func(0, i*0.1) for i in range(0,10)]
l2 = [GSP(ctr, reserve, bids, score, num_slots, num_bidder).pay_func(0, i*0.1) for i in range(0,10)]
#print(GSP(ctr, reserve, bids, score, num_slots, num_bidder).alloc_func(2, 4))
print l,l2
print(GSP(ctr, reserve, bids, score, num_slots, num_bidder).pay_func(2, 4))


