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
from regressions import *


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
    
# returns the normalization of table A in [c,d]
def normalize(A, bid_space,c,d):
    minn = np.min(A)
    maxx = np.max(A)

    if (minn == maxx):
        B = [(1/bid_space) for _ in range(0,bid_space)]
    else: 
        B = [(d-c)*(A[i] - minn)/(maxx - minn) + c for i in range(0,bid_space)]

    return B

def main_winexp(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold, noise):
    algo_util = []
    temp_regr = []
    clean_alloc = [[] for _ in range(0,T)]
    clean_pay   = [[] for _ in range(0,T)]
    clean_reward = [[] for _ in range(0,T)]
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
        clean_pay[t]        = [gsp_instance.pay_func(bidder.id, b*bidder.eps) for b in range(0,bidder.bid_space)]

        arm_chosen = int(math.ceil(bids[t][bidder.id]/bidder.eps))   
        # computation of reward will only be used for the regret
        if allocated > threshold[t]:    
            bidder.allocated[t]                 = 1
            bidder.alloc_func[t]                = compute_allocation_function(bidder.currbid[:t+1], bidder.allocated[:t+1], bidder.bid_space, bidder.eps)
            bidder.alloc_func[t][arm_chosen]    = allocated
            bidder.pay_func[t]                  = compute_payment_function(bidder.currbid[:t+1], bidder.payment[:t+1], bidder.bid_space, bidder.eps)       
            bidder.pay_func[t][arm_chosen]      = bidder.payment[t]
            temp_reward                         = [(values[t][0] - bidder.pay_func[t][b]) for b in range(0,bidder.bid_space)] 
            clean_reward[t]                     = [(values[t][0] - clean_pay[t][b]) for b in range(0,bidder.bid_space)]
            # since pay_func is estimated from the regression
            # we are not sure it is going to be in [-1,1]
            bidder.reward_func[t]   = normalize(temp_reward,bidder.bid_space,-1,1)
            bidder.utility[t]       = bidder.compute_utility(1, bidder.reward_func[t], bidder.alloc_func[t])
        else:
            bidder.allocated[t]                 = 0
            bidder.alloc_func[t]                = compute_allocation_function(bidder.currbid[:t+1], bidder.allocated[:t+1], bidder.bid_space, bidder.eps)
            bidder.alloc_func[t][arm_chosen]    = allocated
            bidder.payment[t]                   = 0 
            bidder.pay_func[t]                  = [0]*bidder.bid_space
            bidder.reward_func[t]               = [0 for _ in range(0,bidder.bid_space)]
            clean_reward[t]                     = bidder.reward_func[t]
            bidder.utility[t]                   = (bidder.compute_utility(0, bidder.reward_func[t], bidder.alloc_func[t]))


        (bidder.weights, bidder.pi) = bidder.weights_update_winexp(bidder.eta_winexp, bidder.utility[t])        

        # utility of algorithm computed as if we knew everything
        algo_util.append(clean_reward[t][arm_chosen]*clean_alloc[t][arm_chosen])

        temp_regr.append(regret(clean_reward,clean_alloc,bidder.bid_space, algo_util,t))    

    return temp_regr   


