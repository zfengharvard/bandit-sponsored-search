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
from runner_winexp_all_bidders import compute_reward,noise_mask,normalize
from regressions import *

def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold,noise,num_adaptive):
    algo_util  = []
    temp_regr  = []
    clean_alloc  = [[] for _ in range(0,T)]
    clean_pay    = [[] for _ in range(0,T)]
    clean_reward = [[] for _ in range(0,T)]
    for t in range(0,T):
        bid_chosen = [bidder[i].bidding() for i in range(0,num_adaptive)]
        for i in range(0,num_adaptive): 
            bids[t][i] = bid_chosen[i]
        bid_vec = deepcopy(bids[t])
        gsp_instance =GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders) 
        arm_chosen =[0]*num_adaptive
        for i in range(0,num_adaptive):
            allocated = gsp_instance.alloc_func(bidder[i].id, bids[t][bidder[i].id])
            temp      = [gsp_instance.alloc_func(bidder[i].id, bid*bidder[i].eps)  for bid in range(0, bidder[i].bid_space)]
            
            if (i == 0):
                clean_alloc[t] = deepcopy(temp)
            noise_cp = deepcopy(noise)
            #reward function: value - payment(coming from GSP module)
            arm_chosen[i] = int(math.ceil(bids[t][i]/bidder[i].eps))
            temp_pay = [gsp_instance.pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
            if (i == 0):
                bidder[i].alloc_func[t] = noise_mask(temp,noise_cp[t],ctr[t], num_slots)
                bidder[i].pay_func[t]   = temp_pay
                if allocated > threshold[t]:    
                    bidder[i].reward_func[t] = [(values[t][i] - bidder[i].pay_func[t][b]) for b in range(0,bidder[i].bid_space)] 
                else:
                    bidder[i].reward_func[t] = [0 for _ in range(0,bidder[i].bid_space)]


                bidder[i].utility[t] = bidder[i].reward_func[t]

                #weights update
                
                if bidder[i].pi[arm_chosen[i]] < 0.0000000001:
                    bidder[i].pi[arm_chosen[i]] = 0.0000000001
                estimated_loss = -bidder[i].utility[t][arm_chosen[i]]/bidder[i].pi[arm_chosen[i]]
                bidder[i].loss[arm_chosen[i]] += estimated_loss
                arr = np.array([(-bidder[i].eta_exp3)*bidder[i].loss[b] for b in range(0,bidder[i].bid_space)], dtype=np.float128)
                bidder[i].weights = np.exp(arr)
                bidder[i].pi = [bidder[i].weights[b]/sum(bidder[i].weights) for b in range(0,bidder[i].bid_space)]
            else:
                bidder[i].currbid[t]   = arm_chosen[i]*bidder[i].eps   
                bidder[i].allocated[t] = allocated
                bidder[i].payment[t]  = temp_pay[arm_chosen[i]]
                if allocated > threshold[t]:
                    bidder[i].allocated[t] = 1
                    bidder[i].alloc_func[t]                     = compute_allocation_function(bidder[i].currbid[:t+1], bidder[i].allocated[:t+1], bidder[i].bid_space, bidder[i].eps)
                    bidder[i].alloc_func[t][arm_chosen[i]]      = allocated
                    bidder[i].pay_func[t]                       = compute_payment_function(bidder[i].currbid[:t+1], bidder[i].payment[:t+1], bidder[i].bid_space, bidder[i].eps)       
                    bidder[i].pay_func[t][arm_chosen[i]]        = bidder[i].payment[t]
                    temp_reward                                 = [(values[t][0] - bidder[i].pay_func[t][b]) for b in range(0,bidder[i].bid_space)] 
                    bidder[i].reward_func[t]                    = normalize(temp_reward,bidder[i].bid_space,-1,1)
                    bidder[i].utility[t]                        = (bidder[i].compute_utility(1, bidder[i].reward_func[t], bidder[i].alloc_func[t]))
                else:
                    bidder[i].allocated[t] =0
                    bidder[i].alloc_func[t]                     = compute_allocation_function(bidder[i].currbid[:t+1], bidder[i].allocated[:t+1], bidder[i].bid_space, bidder[i].eps)
                    bidder[i].alloc_func[t][arm_chosen[i]]      = allocated
                    bidder[i].payment[t]                        = 0 
                    bidder[i].pay_func[t]                       = [0]*bidder[i].bid_space
                    bidder[i].reward_func[t]                    = [0 for _ in range(0,bidder[i].bid_space)]
                    bidder[i].utility[t]                        = (bidder[i].compute_utility(0, bidder[i].reward_func[t], bidder[i].alloc_func[t]))
        
                (bidder[i].weights, bidder[i].pi) = bidder[i].weights_update_winexp(bidder[i].eta_winexp, bidder[i].utility[t])        

        
        algo_util.append((bidder[0].reward_func[t][arm_chosen[0]]*clean_alloc[t][arm_chosen[0]]))
        temp_regr.append(regret(bidder[0].reward_func,clean_alloc,bidder[0].bid_space, algo_util,t))    

    return temp_regr   


