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


def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold,noise):
    algo_util  = []
    temp_regr  = []
    #print ("Threshold inside exp3")
    #print threshold
    for t in range(0,T):
        bid_chosen = bidder.bidding()
        bids[t][0] = bid_chosen
        bid_vec = deepcopy(bids[t])
        gsp_instance =GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders) 
        allocated = gsp_instance.alloc_func(bidder.id, bids[t][bidder.id])
        temp      = [gsp_instance.alloc_func(bidder.id, bid*bidder.eps)  for bid in range(0, bidder.bid_space)]
        
        noise_cp = deepcopy(noise)
        #bidder.alloc_func[t] = noise_mask(temp,noise_cp[t],ctr[t], num_slots)
        bidder.alloc_func[t] = temp
        #reward function: value - payment(coming from GSP module)
        bidder.pay_func[t] = [gsp_instance.pay_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]  
        if allocated > threshold[t]:    
            bidder.reward_func[t] = [(values[t][0] - bidder.pay_func[t][b]) for b in range(0,bidder.bid_space)] 
            #TODO check here if this need to be multiplied by alloc
            bidder.utility[t]     = [(bidder.reward_func[t][b] - 1) for b in range(0,bidder.bid_space)]
        else:
            bidder.reward_func[t] = [0 for _ in range(0,bidder.bid_space)]
            bidder.utility[t]     = [(bidder.reward_func[t][b] - 1) for b in range(0,bidder.bid_space)]


        #weights update
        arm_chosen = int(math.ceil(bids[t][0]/bidder.eps))
        
        if bidder.pi[arm_chosen] < 0.0000000001:
            bidder.pi[arm_chosen] = 0.0000000001
        estimated_loss = bidder.utility[t][arm_chosen]/bidder.pi[arm_chosen]
        bidder.loss[arm_chosen] += estimated_loss
        arr = [bidder.eta_exp3*bidder.loss[b] for b in range(0,bidder.bid_space)]
        bidder.weights = np.exp(arr)
        bidder.pi = [bidder.weights[b]/sum(bidder.weights) for b in range(0,bidder.bid_space)]
        
        
        algo_util.append((bidder.reward_func[t][arm_chosen]*bidder.alloc_func[t][arm_chosen]))
        #print ("Algorithm's average utility")
        #print algo_util
        temp_regr.append(regret(bidder.reward_func,bidder.alloc_func,bidder.bid_space, algo_util,t))    
        #print ("Regret inside" )
        #print temp_regr

    return temp_regr   


