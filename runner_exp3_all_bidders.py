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
from runner_winexp_all_bidders import compute_reward


def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values):
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
        

        print ("Bids Vector")
        print bids[t]
        for i in range(0,num_bidders):
            #every bidder is a learner and they all should update the estimated utility that they get
            allocated = GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder[i].id, bids[t][bidder[i].id])
            bidder[i].alloc_func[t] = [GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]
            print ("Allocation Function for Bidder %d"%bidder[i].id)
            print bidder[i].alloc_func[t]
            print ("What he was allocated: %f"%allocated)
            #reward function: value - payment(coming from GSP module)
            bid_vec = deepcopy(bids[t])
            bidder[i].pay_func[t] = [GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders).pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
            print ("Payment Function for Bidder %d"%bidder[i].id)
            print bidder[i].pay_func[t]
            paid = bidder[i].pay_func[t][bidder[i].alloc_func[t].index(allocated)]
            print ("What he actually paid: %f"%paid)
    
            bidder[i].reward_func[t] = compute_reward(bidder[i].alloc_func[t], bidder[i].pay_func[t], ctr[t], values[t])
            print ("Reward Function for Bidder %d"%bidder[i].id)
            print bidder[i].reward_func[t]
            #### EXP3 computations ####
            bidder[i].utility[t] = [bidder[i].reward_func[t][b]*bidder[i].alloc_func[t][b] - 1 for b in range(0, bidder[i].bid_space)]
            print ("Bidder %d utility"%bidder[i].id)
            print bidder[i].utility[t]

            #weights update
            print bids[t], bids[t][bidder[i].id]
            arm_chosen = int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps))
            print ("Arm Chosen")
            print arm_chosen

            print ("Bidder %d Realized Utility: %f"%(bidder[i].id,bidder[i].utility[t][arm_chosen]))


            print ("Probability vector before computing estimated loss")
            print bidder[i].pi
           
            estimated_loss = bidder[i].utility[t][arm_chosen]/bidder[i].pi[arm_chosen]
            print ("Estimated Loss")
            print estimated_loss
            bidder[i].loss[arm_chosen] += estimated_loss
            print bidder[i].eta_exp3, bidder[i].loss
            bidder[i].weights = [math.exp(bidder[i].eta_exp3*bidder[i].loss[b]) for b in range(0,bidder[i].bid_space)]
            bidder[i].pi = [bidder[i].weights[b]/sum(bidder[i].weights) for b in range(0,bidder[i].bid_space)]
            
            print ("Weights vector")
            print bidder[i].weights


            print ("Probability vector after computing estimated loss")
            print bidder[i].pi
        
    # after the end of T timesteps, compute regrets for both the EXP3 algo
    for i in range(0, num_bidders):
        algo_util = [bidder[i].utility[t][int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps))] for t in range(0,T)]
        print ("Utility that bidder %d"%i + " got:")
        print algo_util
        print ("Reward Function for bidder %d"%i)
        print bidder[i].reward_func
        print ("Allocation Function for bidder %d"%i)
        print bidder[i].alloc_func
        bidder[i].exp3_regret[curr_rep] = regret(0, bidder[i].reward_func, bidder[i].alloc_func, bidder[i].bid_space, algo_util, T)
    s = 0
    for i in range(0, num_bidders):
        s += bidder[i].exp3_regret[curr_rep]
    return s/num_bidders
        


