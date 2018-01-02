
import numpy as np
import random
from gsp import GSP


### Test the GSP module

reserve = 0.6
num_bidder = 5
num_slots = 3
ctr = [0.6, 0.5, 0.3]
score = [0.2, 0.3, 0.25, 0.3, 0.4]
bids = [2.0, 3.0, 4.0, 2.0, 3.0]


print(GSP(ctr, reserve, bids, score, num_slots, num_bidder).alloc_func(2, 3))
print(GSP(ctr, reserve, bids, score, num_slots, num_bidder).pay_func(2, 3))


