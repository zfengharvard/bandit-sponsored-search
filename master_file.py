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

num_bidders         = 5
num_repetititions   = 10 #how many times each T will be repeated  
max_num_rounds      = 10
min_num_rounds      = 1
T                   = 10
num_slots           = 3


# if he gets allocated a slot, then reward = value - payment
# else reward = 0
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


rank_scores = [0.700573810327246, 0.3110979655260716, 0.610430432163001, 0.03395812562678002, 0.8345253204018921]
bids = [0.6, 0.0, 0.2, 0.1, 0.4]
ctr  = [0.97, 0.9, 0.57]
reserve = 0.1 
for t in range(0,1):
    #Create the rank scores (different at every t)
    #rank_scores = [np.random.uniform(0,1) for i in range(0,num_bidders)]
    #bids = [round(bidder[i].bidding(),2) for i in range(0,num_bidders)]
    #ctr  = [round(np.random.uniform(0,1), 2) for i in range(0,num_slots)]        
    #ctr.sort(reverse=True)
    #reserve = round(np.random.uniform(0,0.3),2)
    print ("Rank Scores: ")
    print rank_scores
    print ("Bids")
    print bids 
    print ("CTRs")
    print ctr
    print ("Reserve Price")
    print reserve  
    # value function for every slot
    # could be seen as the conversion rate for every slot
    values = [round(np.random.uniform(0,1),2) for j in range(0,num_slots)]
    print ("Values List")
    print values
    
    for i in range(0,num_bidders):
        #every bidder is a learner and they all should update the estimated utility that they get
        allocated = GSP(ctr, reserve, bids, rank_scores, num_slots, num_bidders).alloc_func(bidder[i].id, bids[bidder[i].id])
        allocation_func = [GSP(ctr, reserve, bids, rank_scores, num_slots, num_bidders).alloc_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]
        print ("Allocation Function for Bidder %d"%bidder[i].id)
        print allocation_func
        #reward function: value - payment(coming from GSP module)
        payment_func = [GSP(ctr, reserve, bids, rank_scores, num_slots, num_bidders).pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
        print ("Payment Function for Bidder %d"%bidder[i].id)
        print payment_func
        reward_func = compute_reward(allocation_func, payment_func, ctr, values)
        print ("Reward Function for Bidder")
        print reward_func
        #### WIN-EXP computations ####
        if allocated != 0: #only if he gets allocated originally he can get information     
            #updates the bidder's estimate of the utility
            bidder[i].utility[t] = (bidder[i].compute_utility(1, reward_func, allocation_func))
        else:
            bidder[i].utility[t] = (bidder[i].compute_utility(0, reward_func, allocation_func))
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


        ### EXP3 computations

        


