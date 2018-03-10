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


def main_exp3(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,num_auctions,bids,num_adaptive):
    algo_util  = []
    temp_regr  = []
    temp_bids  = []
    adaptive_lst = [i for i in range(0,num_adaptive)]
    #bids       = [[] for _ in range(0,T)]
    for t in range(0,T):
        #   The bids chosen for both the learner and the adversaries are the same
        #    for all auctions in a batch.
        
        bid_chosen = [0]*num_bidders
        for i in range(0,num_bidders):
            if i in adaptive_lst:
                bid_chosen[i] = round(bidder[i].bidding(),2)
                bids[t][i]    = bid_chosen[i]
            else:
                bid_chosen[i] = bids[t][i]
        for auction in range(0,num_auctions):
            #bid_chosen = round(np.random.uniform(0,1),1)
            #bid_chosen = round(np.random.uniform(0,1),2)
            #print ("Bid chosen for timestep t=%d is:%f"%(t,bid_chosen))
            #bid_chosen = round(np.random.uniform(0,1),2)
            #bids[t] = bid_chosen
            
            #print ("Repetition=%d, timestep t=%d"%(curr_rep, t))
            #print ("Rank scores")
            #print rank_scores[t]
            #print ("CTR")
            #print ctr[t]
            #print ("reserve")
            #print reserve[t]
            #print ("bids")
            #print bids[t]
            #for i in range(0,num_bidders):
            for i in range(0,num_adaptive):
                allocated = GSP(ctr[auction][t], reserve[auction][t], bids[t], rank_scores[auction][t], num_slots, num_bidders).alloc_func(bidder[i].id, bids[t][bidder[i].id])
                bidder[i].alloc_func[auction][t] = [GSP(ctr[auction][t], reserve[auction][t], bids[t], rank_scores[auction][t], num_slots, num_bidders).alloc_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]
                bid_vec = deepcopy(bids[t])
                bidder[i].pay_func[t] = [GSP(ctr[auction][t], reserve[auction][t], bid_vec, rank_scores[auction][t], num_slots, num_bidders).pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
                bidder[i].reward_func[auction][t] = compute_reward(bidder[i].alloc_func[auction][t], bidder[i].pay_func[t], ctr[auction][t], values[auction][t])


            #bidder.alloc_func[auction][t] = [GSP(ctr[auction][t], reserve[auction][t], bids[t], rank_scores[auction][t], num_slots, num_bidders).alloc_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]
            #print ("alloc func")
            #print bidder.alloc_func
            #reward function: value - payment(coming from GSP module)
            #bid_vec = deepcopy(bids[auction][t])
            #bidder.pay_func[t] = [GSP(ctr[auction][t], reserve[auction][t], bid_vec, rank_scores[auction][t], num_slots, num_bidders).pay_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]  
            #print ("pay func")
            #print bidder.pay_func
    
            #bidder.reward_func[auction][t] = compute_reward(bidder.alloc_func[auction][t], bidder.pay_func[t], ctr[auction][t], values[auction][t])
            #print ("Bidder's Reward function")
            #print bidder.reward_func
            #### EXP3 computations ####
            #bidder.utility[auction][t] = [bidder.reward_func[auction][t][b]*bidder.alloc_func[auction][t][b] - 1 for b in range(0, bidder.bid_space)]
            #bidder.utility[t] = [bidder.reward_func[t][b]*bidder.alloc_func[t][b] - 1 for b in range(0, bidder.bid_space)]
            #print ("Bidder %d utility"%bidder.id)
            #print bidder.utility

        #for i in range(0,num_bidders):
        for i in range(0,num_adaptive):
            u_s = [0 for _ in range(0,bidder[i].bid_space)]
            for b in range(0, bidder[i].bid_space):
                for auction in range(0,num_auctions):
                    u_s[b] += bidder[i].reward_func[auction][t][b]*bidder[i].alloc_func[auction][t][b]
                bidder[i].avg_utility[t].append(u_s[b]/num_auctions - 1) 

        #weights update
        #arm_chosen = [int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps)) for i in range(0,num_bidders)]
        arm_chosen = [int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps)) for i in range(0,num_adaptive)]
        #print ("Arm Chosen")
        #print arm_chosen
        #print ("Average reward at timestep t=%d is:"%t)
        #print (bidder.avg_reward[t])
        #print ("Average utility at timestep t=%d is:"%t)
        #print (bidder.avg_utility[t])

        #print ("Probability vector before computing estimated loss")
        #print bidder.pi
        
        #for i in range(0,num_bidders):
        for i in range(0,num_adaptive):
            if bidder[i].pi[arm_chosen[i]] < 0.0000000001:
                bidder[i].pi[arm_chosen[i]] = 0.0000000001
            estimated_loss = bidder[i].avg_utility[t][arm_chosen[i]]/bidder[i].pi[arm_chosen[i]]
            #print ("Estimated Loss")
            #print estimated_loss
            bidder[i].loss[arm_chosen[i]] += estimated_loss
            #print bidder.loss
            arr = [bidder[i].eta_exp3*bidder[i].loss[b] for b in range(0,bidder[i].bid_space)]
            #bidder[i].weights = [math.exp(bidder[i].eta_exp3*bidder[i].loss[b]) for b in range(0,bidder[i].bid_space)]
            bidder[i].weights = np.exp(arr)
            bidder[i].pi = [bidder[i].weights[b]/sum(bidder[i].weights) for b in range(0,bidder[i].bid_space)]
            
            #print ("Probability vector after computing estimated loss")
            #print bidder.pi
            # compute the algorithm's utility at every step
            #algo_util.append(bidder.avg_utility[t][int(math.ceil(bids[0][t][bidder.id]/bidder.eps))])
        
        #   Only bidder 0 is our learner. The rest are adaptive adversaries 
        
        algo_util.append(bidder[0].avg_utility[t][int(math.ceil(bids[t][0]/bidder[0].eps))])
        temp_regr.append(regret(0,bidder[0].reward_func,bidder[0].alloc_func,bidder[0].bid_space, algo_util,t,num_auctions))    
        temp_bids.append(bids[t][:num_adaptive])
        #print ("Regret inside" )
        #print temp_regr

    return (temp_regr,temp_bids)   

