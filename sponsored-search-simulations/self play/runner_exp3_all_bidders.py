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


def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold,noise,num_adaptive):
    algo_util  = []
    temp_regr  = []
    #print ("Threshold inside exp3")
    #print threshold
    for t in range(0,T):
        bid_chosen = [bidder[i].bidding() for i in range(0,num_adaptive)]
        for i in range(0,num_adaptive): 
            bids[t][i] = bid_chosen[i]
        bid_vec = deepcopy(bids[t])
        gsp_instance =GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders) 
        #allocated = [0]*num_adaptive
        arm_chosen =[0]*num_adaptive
        for i in range(0,num_adaptive):
            allocated = gsp_instance.alloc_func(bidder[i].id, bids[t][bidder[i].id])
            temp      = [gsp_instance.alloc_func(bidder[i].id, bid*bidder[i].eps)  for bid in range(0, bidder[i].bid_space)]
        
            noise_cp = deepcopy(noise)
            bidder[i].alloc_func[t] = noise_mask(temp,noise_cp[t],ctr[t], num_slots)
            #bidder.alloc_func[t] = temp
            #reward function: value - payment(coming from GSP module)
            bidder[i].pay_func[t] = [gsp_instance.pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
            if allocated > threshold[t]:    
                bidder[i].reward_func[t] = [(values[t][i] - bidder[i].pay_func[t][b]) for b in range(0,bidder[i].bid_space)] 
                #TODO check here if this need to be multiplied by alloc
                #bidder.utility[t]     = [(bidder.reward_func[t][b] - 1) for b in range(0,bidder.bid_space)]
            else:
                bidder[i].reward_func[t] = [0 for _ in range(0,bidder[i].bid_space)]
                #bidder.utility[t]     = [(bidder.reward_func[t][b] - 1) for b in range(0,bidder.bid_space)]


            bidder[i].utility[t] = bidder[i].reward_func[t]

            #weights update
            arm_chosen[i] = int(math.ceil(bids[t][i]/bidder[i].eps))
            
            if bidder[i].pi[arm_chosen[i]] < 0.0000000001:
                bidder[i].pi[arm_chosen[i]] = 0.0000000001
            estimated_loss = bidder[i].utility[t][arm_chosen[i]]/bidder[i].pi[arm_chosen[i]]
            bidder[i].loss[arm_chosen[i]] += estimated_loss
            arr = [-bidder[i].eta_exp3*bidder[i].loss[b] for b in range(0,bidder[i].bid_space)]
            bidder[i].weights = np.exp(arr)
            bidder[i].pi = [bidder[i].weights[b]/sum(bidder[i].weights) for b in range(0,bidder[i].bid_space)]
        
        
        algo_util.append((bidder[0].reward_func[t][arm_chosen[0]]*bidder[0].alloc_func[t][arm_chosen[0]]))
        #print ("Algorithm's average utility")
        #print algo_util
        temp_regr.append(regret(bidder[0].reward_func,bidder[0].alloc_func,bidder[0].bid_space, algo_util,t))    
        #print ("Regret inside" )
        #print temp_regr

    return temp_regr   


