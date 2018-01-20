############ 
# Coordinates the gsp and the bidder modules
############ 

import numpy as np
import random
import math
from copy import deepcopy
from bidder import *
from value_module import *
from gsp import GSP
from auction_parameters import *
from regret import *


# if he gets allocated a slot, then reward = value - payment
# else reward = 0
curr_rep = 0
def compute_reward(allocation_func, payment_func, ctr, values):
    reward_lst = []
    for b in allocation_func:
        if b in ctr:
            reward_lst.append(values[ctr.index(b)] - payment_func[allocation_func.index(b)])
        else :
            reward_lst.append(-1)
    return reward_lst

# Preferred Discretizations for the bidders
epsilon = []
for i in range(0,num_bidders):
    epsilon.append(0.1)

# Create the bidders and store them in a list
bidder = [] #list of bidder objects
for i in range(0,num_bidders):
    bidder.append(Bidder(i, epsilon[i]))


bids = []
for t in range(0,T):
    #bids = [round(bidder[i].bidding(),2) for i in range(0,num_bidders)]
    print ("Rank Scores at timestep %d"%t)
    print rank_scores[t]
    print ("Bids at timestep %d"%t)
    bids.append([0.6, 0.0, 0.2, 0.1, 0.4])
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
        bidder[i].pay_func[t] = [GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
        print ("Payment Function for Bidder %d"%bidder[i].id)
        print bidder[i].pay_func
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
        print ("Bidder's utility")
        print bidder[i].utility[t]
        #TODO: I have checked up until this point and all is computed correctly. Next Steps:
        """
            1) Need to check that utilities are included correctly for all timesteps (list of lists)
            2) Solve/Clarify the TODOs in the gsp.py module
            3) Compute the regret first for the win-exp algo to make sure everything is computed correctly
            4) Compute the regret for the EXP3 algorithm (CAREFUL! (3) and (4) have to be computed for the same 
               inputs.
            5) Run steps 3 and 4 repeatedly for num_repetitions in order to get estimated expected regret.
        """
        bidder[i].weights_update_winexp(bidder[i].eta_winexp, bidder[i].utility[t])        
    
    
# after the end of T timesteps, compute regret
for i in range(0, num_bidders):
    algo_util = [bidder[i].utility[t][int(bids[t][bidder[i].id]/bidder[i].eps)] for t in range(0,T)]
    bidder[i].regret[curr_rep] = regret(0, bidder[i].reward_func, bidder[i].alloc_func, bidder[i].bid_space, algo_util)


        ### EXP3 computations

        


