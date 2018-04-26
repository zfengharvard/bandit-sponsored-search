############ 
# Coordinates the gsp and the bidder modules
# For the EXP3 implementation
############ 
import sys
import numpy as np
import random
import math
from copy import deepcopy
from bidder import *
from gsp import GSP
from regret import *
from runner_winexp_all_bidders import compute_reward,noise_mask
from regressions import *

# returns the normalization of table A in [c,d]
def normalize(A, bid_space,c,d):
    minn = np.min(A)
    maxx = np.max(A)

    if (maxx == minn):
        B = [1/(bid_space) for _ in range(0,bid_space)]
    else:
        B = [(d-c)*(A[i] - minn)/(maxx - minn) + c for i in range(0,bid_space)]

    return B

def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold,noise):
    algo_util  = []
    temp_regr  = []
    clean_alloc = [[] for _ in range(0,T)]
    for t in range(0,T):
        bid_chosen          = bidder.bidding()
        bids[t][0]          = bid_chosen
        bid_vec             = deepcopy(bids[t])
        bidder.currbid[t]   = bid_chosen
        currbid_cpy         = deepcopy(bidder.currbid)
 
        gsp_instance        = GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders) 
        allocated           = gsp_instance.alloc_func(bidder.id, bidder.currbid[t])
        bidder.payment[t]   = gsp_instance.pay_func(bidder.id, currbid_cpy[t])
        clean_alloc[t]      = [gsp_instance.alloc_func(bidder.id, b*bidder.eps) for b in range(0,bidder.bid_space)]        
        bidder.pay_func[t]  = [gsp_instance.pay_func(bidder.id, b*bidder.eps) for b in range(0,bidder.bid_space)]     
        bidder.alloc_func[t] = clean_alloc[t]

        arm_chosen = int(math.ceil(bids[t][0]/bidder.eps))
        #reward function: value - payment(coming from GSP module)
        if allocated > threshold[t]:    
            bidder.reward_func[t]           = [(values[t][0] - bidder.pay_func[t][b]) for b in range(0,bidder.bid_space)] 
        else:
            bidder.reward_func[t] = [0 for _ in range(0,bidder.bid_space)]

        #bidder.utility[t] = [bidder.reward_func[t][b] - 1 for b in range(0,bidder.bid_space)] 
        bidder.utility[t] = normalize(bidder.reward_func[t],bidder.bid_space,0,1)

        #weights update
        
        if bidder.pi[arm_chosen] < 0.0000000001:
            bidder.pi[arm_chosen] = 0.0000000001
        estimated_loss = bidder.utility[t][arm_chosen]/bidder.pi[arm_chosen]
        bidder.loss[arm_chosen] += estimated_loss
        arr = np.array([(-bidder.eta_exp3)*bidder.loss[b] for b in range(0,bidder.bid_space)], dtype=np.float128)
        bidder.weights = np.exp(arr)
        bidder.pi = [bidder.weights[b]/sum(bidder.weights) for b in range(0,bidder.bid_space)]
        
        
        algo_util.append((bidder.reward_func[t][arm_chosen]*clean_alloc[t][arm_chosen]))
        temp_regr.append(regret(bidder.reward_func,clean_alloc,bidder.bid_space, algo_util,t))    

    return temp_regr   


