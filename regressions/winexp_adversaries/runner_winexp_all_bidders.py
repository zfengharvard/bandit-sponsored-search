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

# returns the normalization of table A in [c,d]
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
    

def main_winexp(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold, noise,num_adaptive):
    algo_util = []
    temp_regr = []
    clean_alloc = [[] for _ in range(0,T)]
    clean_pay   = [[] for _ in range(0,T)]
    clean_reward = [[] for _ in range(0,T)]
    for t in range(0,T):
        bid_chosen = [bidder[i].bidding() for i in range(0,num_adaptive)]
        for i in range(0,num_adaptive): 
            bids[t][i] = bid_chosen[i]
        bid_vec = deepcopy(bids[t])
        gsp_instance =GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders) 

        arm_chosen = [int(math.ceil(bids[t][i]/bidder[i].eps)) for i in range(0,num_adaptive)] 
        for i in range(0,num_adaptive):
            allocated = gsp_instance.alloc_func(bidder[i].id, bids[t][bidder[i].id])
            temp      = [gsp_instance.alloc_func(bidder[i].id, bid*bidder[i].eps)  for bid in range(0, bidder[i].bid_space)]
            if (i == 0):
                clean_alloc[t]          = deepcopy(temp)
                clean_pay[t]            = [gsp_instance.pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0,bidder[i].bid_space)]
                
            temp_pay                = gsp_instance.pay_func(bidder[i].id, bid_vec[i])
            bidder[i].payment[t]    = temp_pay
            
            # bidder sees noisy data as his allocation
            noise_cp = deepcopy(noise)
            bidder[i].currbid[t]   = arm_chosen[i]*bidder[i].eps   
            if allocated > threshold[t]:
                bidder[i].allocated[t]                  = 1
                bidder[i].alloc_func[t]                 = compute_allocation_function(bidder[i].currbid[:t+1], bidder[i].allocated[:t+1], bidder[i].bid_space, bidder[i].eps)
                bidder[i].alloc_func[t][arm_chosen[i]]  = allocated
                bidder[i].pay_func[t]                   = compute_payment_function(bidder[i].currbid[:t+1], bidder[i].payment[:t+1], bidder[i].bid_space, bidder[i].eps)       
                bidder[i].pay_func[t][arm_chosen[i]]    = bidder[i].payment[t]
                temp_reward                             = [(values[t][0] - bidder[i].pay_func[t][b]) for b in range(0,bidder[i].bid_space)] 
                if (i == 0):
                    clean_reward[t]                     = [(values[t][0] - clean_pay[t][b]) for b in range(0,bidder[i].bid_space)]
                bidder[i].reward_func[t]   = normalize(temp_reward,bidder[i].bid_space,-1,1)
                bidder[i].utility[t]                    = (bidder[i].compute_utility(1, bidder[i].reward_func[t], bidder[i].alloc_func[t]))
            else:
                bidder[i].allocated[t] =0
                bidder[i].alloc_func[t]                 = compute_allocation_function(bidder[i].currbid[:t+1], bidder[i].allocated[:t+1], bidder[i].bid_space, bidder[i].eps)
                bidder[i].alloc_func[t][arm_chosen[i]]  = allocated
                bidder[i].payment[t]                    = 0 
                bidder[i].pay_func[t]                   = [0]*bidder[i].bid_space
                temp_reward                             = [0 for _ in range(0,bidder[i].bid_space)]
                bidder[i].reward_func[t]                = normalize(temp_reward,bidder[i].bid_space,-1,1)
                if (i == 0):
                    clean_reward[t]                     = [0 for _ in range(0,bidder[i].bid_space)]
                bidder[i].utility[t]                    = (bidder[i].compute_utility(0, bidder[i].reward_func[t], bidder[i].alloc_func[t]))
        
            (bidder[i].weights, bidder[i].pi) = bidder[i].weights_update_winexp(bidder[i].eta_winexp, bidder[i].utility[t])        
                

        algo_util.append((clean_reward[t][arm_chosen[0]]*clean_alloc[t][arm_chosen[0]]))
        temp_regr.append(regret(clean_reward,clean_alloc,bidder[0].bid_space, algo_util,t))    
        

    return temp_regr   


