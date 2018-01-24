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


# if he gets allocated a slot, then reward = value - payment
# else reward = 0
def compute_reward(allocation_func, payment_func, ctr, values):
    reward_lst = []
    for b in allocation_func:
        if b in ctr:
            # If bidder isn't allocated any slot: b == 0
            # However, b == 0 also if the CTR of the position is 0
            reward_lst.append(values[ctr.index(b)] - payment_func[allocation_func.index(b)])
        else :
            reward_lst.append(-1)
    return reward_lst


def main_winexp(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values):
    bids = []
    for t in range(0,T):
        bids.append([round(bidder[i].bidding(),2) for i in range(0,num_bidders)])
        print ("Rank Scores at timestep %d"%t)
        print rank_scores[t]
        print ("Bids at timestep %d"%t)
        #bids.append([0.6, 0.0, 0.2, 0.1, 0.4])
        print bids[t] 
        print ("CTR at timestep %d"%t)
        print ctr[t]
        print ("Reserve Price at timestep %d"%t)
        print reserve[t]  
        print ("Values List at timestep %d"%t)
        print values[t]
        
        for i in range(0,num_bidders):
            #every bidder is a learner and they all should update the estimated utility that they get
            allocated = GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder[i].id, bids[t][bidder[i].id])
            bidder[i].alloc_func[t] = [GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]
            print ("Allocation Function for Bidder %d"%bidder[i].id)
            print bidder[i].alloc_func[t]
            #reward function: value - payment(coming from GSP module)
            bid_vec = deepcopy(bids[t])
            bidder[i].pay_func[t] = [GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders).pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
            print ("Payment Function for Bidder %d"%bidder[i].id)
            print bidder[i].pay_func[t]
            bidder[i].reward_func[t] = compute_reward(bidder[i].alloc_func[t], bidder[i].pay_func[t], ctr[t], values[t])
            print ("Reward Function for Bidder")
            print bidder[i].reward_func[t]
            #### WIN-EXP computations ####
            if allocated != 0: #only if he gets allocated originally he can get information     
                #updates the bidder's estimate of the utility
                bidder[i].utility[t] = (bidder[i].compute_utility(1, bidder[i].reward_func[t], bidder[i].alloc_func[t]))
            else:
                bidder[i].utility[t] = (bidder[i].compute_utility(0, bidder[i].reward_func[t], bidder[i].alloc_func[t]))
            bidder[i].utility[t] = [0 if bidder[i].utility[t][bb] == -0.0 else bidder[i].utility[t][bb] for bb in range(0,bidder[i].bid_space)]
            #weights update
            print ("Bidder %d utility"%i)
            print bidder[i].utility[t]
            print ("Bidder %d weights and probabilities before the update at timestep %d"%(i,t))
            print bidder[i].weights
            print bidder[i].pi 
            bidder[i].weights_update_winexp(bidder[i].eta_winexp, bidder[i].utility[t])        
            print ("Bidder %d weights and probabilities after the update at timestep %d"%(i,t))
            print bidder[i].weights
            print bidder[i].pi 
        
        
    # after the end of T timesteps, compute regrets for both the WIN-EXP algo
    for i in range(0, num_bidders):
        arm_chosen = [int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps)) for t in range(0,T)]  
        algo_util = [(bidder[i].reward_func[t][arm_chosen[t]]*bidder[i].alloc_func[t][arm_chosen[t]] - 1) for t in range(0,T)]
        bidder[i].winexp_regret[curr_rep] = regret(0, bidder[i].reward_func, bidder[i].alloc_func, bidder[i].bid_space, algo_util, T)
    s = 0
    for i in range(0, num_bidders):
        s += bidder[i].winexp_regret[curr_rep]
    return s/num_bidders
        


