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
    for t in range(0,T):
        bid_chosen = [bidder[i].bidding() for i in range(0,num_adaptive)]
        for i in range(0,num_adaptive): 
            bids[t][i] = bid_chosen[i]
        bid_vec = deepcopy(bids[t])
        gsp_instance =GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders) 
        # this is not reported to the bidder, and thus is cleaned of noise
        for i in range(0,num_adaptive):
            allocated = gsp_instance.alloc_func(bidder[i].id, bids[t][bidder[i].id])
            temp      = [gsp_instance.alloc_func(bidder[i].id, bid*bidder[i].eps)  for bid in range(0, bidder[i].bid_space)]
            
            if (i == 0):
                clean_alloc[t] = deepcopy(temp)
            # bidder sees noisy data as his allocation
            noise_cp = deepcopy(noise)
            bidder[i].alloc_func[t] = noise_mask(temp, noise_cp[t], ctr[t], num_slots)
        #bidder.alloc_func[t] = temp
        
        #reward function: value - payment(coming from GSP module)
            bidder[i].pay_func[t] = [gsp_instance.pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
        #### WIN-EXP computations ####
        # computation of reward will only be used for the regret
            if (i == 0):
                if allocated > threshold[t]:    
                    bidder[i].reward_func[t] = [(values[t][0] - bidder[i].pay_func[t][b]) for b in range(0,bidder[i].bid_space)] 
                    bidder[i].utility[t] = bidder[i].compute_utility(1, bidder[i].reward_func[t], bidder[i].alloc_func[t])
                else:
                    bidder[i].reward_func[t] = [0 for _ in range(0,bidder[i].bid_space)]
                    bidder[i].utility[t] = (bidder[i].compute_utility(0, bidder[i].reward_func[t], bidder[i].alloc_func[t]))


                (bidder[i].weights, bidder[i].pi) = bidder[i].weights_update_winexp(bidder[i].eta_winexp, bidder[i].utility[t])        

            else: 
                if allocated > threshold[t]:    
                    bidder[i].reward_func[t] = [(values[t][i] - bidder[i].pay_func[t][b]) for b in range(0,bidder[i].bid_space)] 
                else:
                    bidder[i].reward_func[t] = [0 for _ in range(0,bidder[i].bid_space)]

            
                bidder[i].utility[t] = bidder[i].reward_func[t]

                #weights update
                arm_chosen = int(math.ceil(bids[t][i]/bidder[i].eps))
                
                if bidder[i].pi[arm_chosen] < 0.0000000001:
                    bidder[i].pi[arm_chosen] = 0.0000000001
                estimated_loss = -bidder[i].utility[t][arm_chosen]/bidder[i].pi[arm_chosen]
                bidder[i].loss[arm_chosen] += estimated_loss
                arr = np.array([(-bidder[i].eta_exp3)*bidder[i].loss[b] for b in range(0,bidder[i].bid_space)], dtype=np.float128)
                bidder[i].weights = np.exp(arr)
                bidder[i].pi = [bidder[i].weights[b]/sum(bidder[i].weights) for b in range(0,bidder[i].bid_space)]


        # for each auction (at the same t) you choose the same arm
        arm = int(math.ceil(bids[t][0]/bidder[0].eps))   

        algo_util.append((bidder[0].reward_func[t][arm]*clean_alloc[t][arm]))
        temp_regr.append(regret(bidder[0].reward_func,clean_alloc,bidder[0].bid_space, algo_util,t))    


    return temp_regr   


