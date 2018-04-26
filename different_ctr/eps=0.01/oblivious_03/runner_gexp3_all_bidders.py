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


def main_gexp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,num_auctions):
    algo_util  = []
    temp_regr  = []
    gamma = 1.05*math.sqrt(bidder.bid_space*math.log(bidder.bid_space,2)/T)
    for t in range(0,T):
        #bid_chosen = round(bidder.gbidding(bidder.weights,gamma),2)
        bid_chosen = round(bidder.bidding(),2)
        # the bid chosen by the learner is the same for all auctions in the batch
        for auction in range(0,num_auctions):
            #bid_chosen = round(np.random.uniform(0,1),1)
            #bid_chosen = round(np.random.uniform(0,1),2)
            #print ("Bid chosen for timestep t=%d is:%f"%(t,bid_chosen))
            #bid_chosen = round(np.random.uniform(0,1),2)
            bids[auction][t][0] = bid_chosen
            #print ("Repetition=%d, timestep t=%d, auction=%d"%(curr_rep, t, auction))
            #print ("Rank scores")
            #print rank_scores[auction][t]
            #print ("CTR")
            #print ctr[auction][t]
            #print ("reserve")
            #print reserve[auction][t]
            #print ("bids")
            #print bids[auction][t]
            allocated = GSP(ctr[auction][t], reserve[auction][t], bids[auction][t], rank_scores[auction][t], num_slots, num_bidders).alloc_func(bidder.id, bids[auction][t][bidder.id])
            bidder.alloc_func[auction][t] = [GSP(ctr[auction][t], reserve[auction][t], bids[auction][t], rank_scores[auction][t], num_slots, num_bidders).alloc_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]
            #print ("alloc func")
            #print bidder.alloc_func
            #reward function: value - payment(coming from GSP module)
            bid_vec = deepcopy(bids[auction][t])
            bidder.pay_func[t] = [GSP(ctr[auction][t], reserve[auction][t], bid_vec, rank_scores[auction][t], num_slots, num_bidders).pay_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]  
            #print ("pay func")
            #print bidder.pay_func
    
            bidder.reward_func[auction][t] = compute_reward(bidder.alloc_func[auction][t], bidder.pay_func[t], ctr[auction][t], values[auction][t])
            #print ("Bidder's Reward function")
            #print bidder.reward_func
            #### EXP3 computations ####
            #bidder.utility[auction][t] = [bidder.reward_func[auction][t][b]*bidder.alloc_func[auction][t][b] - 1 for b in range(0, bidder.bid_space)]
            #bidder.utility[t] = [bidder.reward_func[t][b]*bidder.alloc_func[t][b] - 1 for b in range(0, bidder.bid_space)]
            #print ("Bidder %d utility"%bidder.id)
            #print bidder.utility

        u_s = [0 for _ in range(0,bidder.bid_space)]
        for b in range(0, bidder.bid_space):
            for auction in range(0,num_auctions):
                u_s[b] += bidder.reward_func[auction][t][b]*bidder.alloc_func[auction][t][b]
            bidder.avg_utility[t].append(u_s[b]/num_auctions - 1) 

        #weights update
        arm_chosen = int(math.ceil(bids[0][t][0]/bidder.eps))
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
        #estimated_loss = bidder.avg_utility[t][arm_chosen]/bidder.pi[arm_chosen]
        estimated_loss  = (bidder.avg_utility[t][arm_chosen] - bidder.beta)/bidder.pi[arm_chosen]
        #print ("Estimated Loss")
        #print estimated_loss
        bidder.loss[arm_chosen] += estimated_loss
        #print bidder.loss
        bidder.weights = [math.exp(-bidder.eta_gexp3*bidder.loss[b])  for b in range(0,bidder.bid_space)]
        bidder.pi = [(1-gamma)*bidder.weights[b]/sum(bidder.weights) + gamma/bidder.bid_space for b in range(0,bidder.bid_space)]
        
        #print ("Probability vector after computing estimated loss")
        #print bidder.pi
        # compute the algorithm's utility at every step
        #algo_util.append(bidder.avg_utility[t][int(math.ceil(bids[0][t][bidder.id]/bidder.eps))])
        
        algo_util.append(bidder.avg_utility[t][int(math.ceil(bids[0][t][0]/bidder.eps))])
        #print ("Algorithm's average utility")
        #print algo_util
        temp_regr.append(regret(0,bidder.reward_func,bidder.alloc_func,bidder.bid_space, algo_util,t,num_auctions))    
        #print ("Regret inside" )
        #print temp_regr

    return temp_regr   


