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


def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids):
    
    for t in range(0,T):
        # bids[t] = []
        bids[t][0] = round(bidder.bidding(),2)
        print ("Bids inside exp3 at timestep %d"%t)
        print bids[t]
        #every bidder is a learner and they all should update the estimated utility that they get
        allocated = GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder.id, bids[t][bidder.id])
        bidder.alloc_func[t] = [GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]
        #reward function: value - payment(coming from GSP module)
        bid_vec = deepcopy(bids[t])
        bidder.pay_func[t] = [GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders).pay_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]  
    
        bidder.reward_func[t] = compute_reward(bidder.alloc_func[t], bidder.pay_func[t], ctr[t], values[t])
        #### EXP3 computations ####
        bidder.utility[t] = [bidder.reward_func[t][b]*bidder.alloc_func[t][b] - 1 for b in range(0, bidder.bid_space)]
        print ("Bidder %d utility"%bidder.id)
        print bidder.utility[t]

        #weights update
        print bids[t], bids[t][bidder.id]
        arm_chosen = int(math.ceil(bids[t][bidder.id]/bidder.eps))
        print ("Arm Chosen")
        print arm_chosen

        print ("Probability vector before computing estimated loss")
        print bidder.pi
       
        estimated_loss = bidder.utility[t][arm_chosen]/bidder.pi[arm_chosen]
        print ("Estimated Loss")
        print estimated_loss
        bidder.loss[arm_chosen] += estimated_loss
        print bidder.loss
        bidder.weights = [math.exp(bidder.eta_exp3*bidder.loss[b]) for b in range(0,bidder.bid_space)]
        bidder.pi = [bidder.weights[b]/sum(bidder.weights) for b in range(0,bidder.bid_space)]
        
        print ("Probability vector after computing estimated loss")
        print bidder.pi
        #for i in range(0,num_bidders):
        #    #every bidder is a learner and they all should update the estimated utility that they get
        #    allocated = GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder[i].id, bids[t][bidder[i].id])
        #    bidder[i].alloc_func[t] = [GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]
        #    #reward function: value - payment(coming from GSP module)
        #    bid_vec = deepcopy(bids[t])
        #    bidder[i].pay_func[t] = [GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders).pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
    
        #    bidder[i].reward_func[t] = compute_reward(bidder[i].alloc_func[t], bidder[i].pay_func[t], ctr[t], values[t])
        #    #### EXP3 computations ####
        #    bidder[i].utility[t] = [bidder[i].reward_func[t][b]*bidder[i].alloc_func[t][b] - 1 for b in range(0, bidder[i].bid_space)]
        #    print ("Bidder %d utility"%bidder[i].id)
        #    print bidder[i].utility[t]

        #    #weights update
        #    print bids[t], bids[t][bidder[i].id]
        #    arm_chosen = int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps))
        #    print ("Arm Chosen")
        #    print arm_chosen

        #    print ("Probability vector before computing estimated loss")
        #    print bidder[i].pi
        #   
        #    estimated_loss = bidder[i].utility[t][arm_chosen]/bidder[i].pi[arm_chosen]
        #    print ("Estimated Loss")
        #    print estimated_loss
        #    bidder[i].loss[arm_chosen] += estimated_loss
        #    print bidder[i].loss
        #    bidder[i].weights = [math.exp(bidder[i].eta_exp3*bidder[i].loss[b]) for b in range(0,bidder[i].bid_space)]
        #    bidder[i].pi = [bidder[i].weights[b]/sum(bidder[i].weights) for b in range(0,bidder[i].bid_space)]
            
        #    print ("Probability vector after computing estimated loss")
        #    print bidder[i].pi
        
    # after the end of T timesteps, compute regrets for both the EXP3 algo
    #for i in range(0, num_bidders):
    #    algo_util = [bidder[i].utility[t][int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps))] for t in range(0,T)]
    #    bidder[i].exp3_regret[curr_rep] = regret(0, bidder[i].reward_func, bidder[i].alloc_func, bidder[i].bid_space, algo_util, T)
    
    algo_util = [bidder.utility[t][int(math.ceil(bids[t][bidder.id]/bidder.eps))] for t in range(0,T)]
    bidder.exp3_regret[curr_rep] = regret(0, bidder.reward_func, bidder.alloc_func, bidder.bid_space, algo_util, T)
    #s = 0
    #for i in range(0, num_bidders):
    #    s += bidder[i].exp3_regret[curr_rep]
    
    #return s/num_bidders
    return bidder.exp3_regret[curr_rep]   


