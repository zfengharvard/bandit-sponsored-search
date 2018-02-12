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
from regressions import *


def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids):
    algo_util  = []
    temp_regr  = []
    for t in range(0,T):
        bid_chosen = round(bidder.bidding(),2)
        bidder.bid_chosen.append(bid_chosen)
        #bid_chosen = round(np.random.uniform(0,1),1)
        #bid_chosen = round(np.random.uniform(0,1),2)
        #print ("Bid chosen for timestep t=%d is:%f"%(t,bid_chosen))
        #bid_chosen = round(np.random.uniform(0,1),2)
        bids[t][0] = bid_chosen
        bidder.allocated.append(GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder.id, bids[t][bidder.id]))

        alloc_cpy = deepcopy(bidder.alloc_func[:t])
        bid_cpy   = deepcopy(bidder.bid_chosen)

        # this will return the function of the estimated labels according to the regression that we will run
        bidder.alloc_func[t] = compute_allocation_function(bid_cpy[:t], alloc_cpy, bidder.bid_space)  
    
        bid_vec = deepcopy(bids[t])
        bidder.paid.append(GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders).pay_func(bidder.id, bid*bidder.eps))
        pay_cpy = deepcopy(bidder.paid[:t])
        bidder.pay_func[t] = compute_payment_function(bid_cpy, pay_cpy, bidder.bid_space)
        #print ("pay func")
        #print bidder.pay_func
    
        bidder.reward_func[t] = compute_reward(bidder.alloc_func[t], bidder.pay_func[t], ctr[t], values[t])
        #print ("Bidder's Reward function")
        #print bidder.reward_func
        #### EXP3 computations ####
        #bidder.utility[auction][t] = [bidder.reward_func[auction][t][b]*bidder.alloc_func[auction][t][b] - 1 for b in range(0, bidder.bid_space)]
        bidder.utility[t] = [bidder.reward_func[t][b]*bidder.alloc_func[t][b] - 1 for b in range(0, bidder.bid_space)]
        #print ("Bidder %d utility"%bidder.id)
        #print bidder.utility

        #weights update
        arm_chosen = int(math.ceil(bids[t][0]/bidder.eps))
        #print ("Arm Chosen")
        #print arm_chosen
        #print ("Average reward at timestep t=%d is:"%t)
        #print (bidder.avg_reward[t])
        #print ("Average utility at timestep t=%d is:"%t)
        #print (bidder.avg_utility[t])

        #print ("Probability vector before computing estimated loss")
        #print bidder.pi
        
        if bidder.pi[arm_chosen] < 0.0000000001:
            bidder.pi[arm_chosen] = 0.0000000001
        estimated_loss = bidder.utility[t][arm_chosen]/bidder.pi[arm_chosen]
        #print ("Estimated Loss")
        #print estimated_loss
        bidder.loss[arm_chosen] += estimated_loss
        #print bidder.loss
        bidder.weights = [math.exp(bidder.eta_exp3*bidder.loss[b]) for b in range(0,bidder.bid_space)]
        bidder.pi = [bidder.weights[b]/sum(bidder.weights) for b in range(0,bidder.bid_space)]
        
        #print ("Probability vector after computing estimated loss")
        #print bidder.pi
        # compute the algorithm's utility at every step
        #algo_util.append(bidder.avg_utility[t][int(math.ceil(bids[0][t][bidder.id]/bidder.eps))])
        
        algo_util.append(bidder.utility[t][int(math.ceil(bids[t][0]/bidder.eps))])
        temp_regr.append(regret(0,bidder.reward_func,bidder.alloc_func,bidder.bid_space, algo_util,t))    
        #print ("Regret inside" )
        #print temp_regr

    return temp_regr   


