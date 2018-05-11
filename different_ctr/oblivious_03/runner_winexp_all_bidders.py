############ 
# Coordinates the gsp and the bidder modules
# For the WIN-EXP implementation
############ 

import numpy as np
import random
import math
from copy import deepcopy
from bidder import *
from gsp import GSP
from regret import *

# returns the normalization of table A in [0,1]
def normalize(A, bid_space,c,d):
    minn = np.min(A)
    maxx = np.max(A)

    if (minn == maxx):
        B = [(1.0/bid_space) for _ in range(0,bid_space)]
    else:
        B = [1.0*(d-c)*(A[i] - minn)/(maxx - minn) + c for i in range(0,bid_space)]

    return B

# if he gets allocated a slot, then reward = value - payment
# else reward = 0
def compute_reward(payment_func, values, bid_space):
    reward_lst = [(values - payment_func[b]) for b in range(0, bid_space)] 
    return reward_lst


def noise_mask(alloc_func, noise,ctr,num_slots):
    lst = []
    for b in alloc_func: 
        if (b == 0):
            lst.append(np.max([0,np.min([noise[num_slots],1])]))
        else:
            lst.append(np.max([0,np.min([b+noise[ctr.index(b)],1])]))

    return lst
    

def main_winexp(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold, noise):
    algo_util = []
    temp_regr = []
    clean_alloc = [[] for _ in range(0,T)]
    for t in range(0,T):
        bid_chosen = bidder.bidding()
        bids[t][0] = bid_chosen
        bid_vec = deepcopy(bids[t])
        gsp_instance =GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders) 
        # this is not reported to the bidder, and thus is cleaned of noise
        allocated = gsp_instance.alloc_func(bidder.id, bids[t][bidder.id])
        temp      = [gsp_instance.alloc_func(bidder.id, bid*bidder.eps)  for bid in range(0, bidder.bid_space)]
        
        clean_alloc[t] = deepcopy(temp)

        # bidder sees noisy data as his allocation
        noise_cp = deepcopy(noise)
        bidder.alloc_func[t] = noise_mask(temp, noise_cp[t], ctr[t], num_slots)
        
        #reward function: value - payment(coming from GSP module)
        bidder.pay_func[t] = [gsp_instance.pay_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]  
        #### WIN-EXP computations ####
        # computation of reward will only be used for the regret
        if allocated > threshold[t]:    
            bidder.reward_func[t] = [(values[t][0] - bidder.pay_func[t][b]) for b in range(0,bidder.bid_space)] 
            bidder.utility[t] = bidder.compute_utility(1, bidder.reward_func[t], bidder.alloc_func[t])
        else:
            bidder.reward_func[t] = [0 for _ in range(0,bidder.bid_space)]
            bidder.utility[t] = (bidder.compute_utility(0, bidder.reward_func[t], bidder.alloc_func[t]))


        (bidder.weights, bidder.pi) = bidder.weights_update_winexp(bidder.eta_winexp, bidder.utility[t])        
        # for each auction (at the same t) you choose the same arm
        arm_chosen = int(math.ceil(bids[t][0]/bidder.eps))   


        algo_util.append((bidder.reward_func[t][arm_chosen]*clean_alloc[t][arm_chosen]))
        temp_regr.append(regret(bidder.reward_func,clean_alloc,bidder.bid_space, algo_util,t))    

    return temp_regr   


