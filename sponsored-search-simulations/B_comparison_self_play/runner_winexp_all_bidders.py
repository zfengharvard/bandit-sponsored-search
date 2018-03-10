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
    algo_util  = []
    temp_regr  = []
    reward_lst = []
    for b in allocation_func:
        if b in ctr:
            # If bidder isn't allocated any slot: b == 0
            # However, b == 0 also if the CTR of the position is 0
            reward_lst.append(values[ctr.index(b)] - payment_func[allocation_func.index(b)])
        else :
            reward_lst.append(-1)
    return reward_lst


def main_winexp(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,num_auctions,bids,num_adaptive):
    algo_util = []
    temp_regr = []
    temp_bids = []
    adaptive_lst = [i for i in range(0, num_adaptive)]
    #bids      = [[] for _ in range(0,T)]
    for t in range(0,T):
        bid_chosen = [0]*num_bidders
        for i in range(0,num_bidders):
            if i in adaptive_lst:
                bid_chosen[i] = round(bidder[i].bidding(),2)
                bids[t][i] = bid_chosen[i]
            else: 
                bid_chosen[i] = bids[t][i]

        # same bid over all auctions that run at the same timestep
        for auction in range(0,num_auctions):
            #print ("all bids at timestep t=%d"%t)
            #bids[t] = bid_chosen
            #print bids
            
            #for i in range(0,num_bidders):
            for i in range(0,num_adaptive):
                # All the bidders are learning. Even the adaptive adversaries. 
                allocated = GSP(ctr[auction][t], reserve[auction][t], bids[t], rank_scores[auction][t], num_slots, num_bidders).alloc_func(bidder[i].id, bids[t][bidder[i].id])
                bidder[i].alloc_func[auction][t] = [GSP(ctr[auction][t], reserve[auction][t], bids[t], rank_scores[auction][t], num_slots, num_bidders).alloc_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]
                bid_vec = deepcopy(bids[t])
                bidder[i].pay_func[t] = [GSP(ctr[auction][t], reserve[auction][t], bid_vec, rank_scores[auction][t], num_slots, num_bidders).pay_func(bidder[i].id, bid*bidder[i].eps) for bid in range(0, bidder[i].bid_space)]  
                bidder[i].reward_func[auction][t] = compute_reward(bidder[i].alloc_func[auction][t], bidder[i].pay_func[t], ctr[auction][t], values[auction][t])
                if bidder[i].id == 0:
                    # Only the learner follows WINEXP
                    if bidder[i].alloc_func[auction][t][int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps))] != 0:
                        bidder[i].utility[auction][t] = (bidder[i].compute_utility(1, bidder[i].reward_func[auction][t], bidder[i].alloc_func[auction][t]))
                    else: 
                        bidder[i].utility[auction][t] = (bidder[i].compute_utility(0, bidder[i].reward_func[auction][t], bidder[i].alloc_func[auction][t]))
                else: 
                    bidder[i].utility[auction][t] = bidder[i].reward_func[auction][t]                        


        # for each auction (at the same t) you choose the same arm
        #arm_chosen = [int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps)) for i in range(0,num_bidders)]   
        arm_chosen = [int(math.ceil(bids[t][bidder[i].id]/bidder[i].eps)) for i in range(0,num_adaptive)]   
        #for i in range(0,num_bidders):
        for i in range(0,num_adaptive):
            u_s = [0 for _ in range(0,bidder[i].bid_space)]
            r_s = [0 for _ in range(0,bidder[i].bid_space)]
            for b in range(0, bidder[i].bid_space):
                for auction in range(0,num_auctions):
                    u_s[b] += bidder[i].utility[auction][t][b]
                    r_s[b] += bidder[i].reward_func[auction][t][b]*bidder[i].alloc_func[auction][t][b]
                #bidder.avg_utility[t].append(u_s[b]/num_auctions - 1) 
                if bidder[i].id == 0:
                    bidder[i].avg_utility[t].append(u_s[b]/num_auctions)
                    bidder[i].avg_reward[t].append(r_s[b]/num_auctions)
                else: 
                    bidder[i].avg_utility[t].append(r_s[b]/num_auctions -1)

            if bidder[i].id == 0: 
                # Only the learner plays WINEXP 
                (bidder[i].weights, bidder[i].pi) = bidder[i].weights_update_winexp(bidder[i].eta_winexp, bidder[i].avg_utility[t])   
            else: 
                # All the others are playing EXP3
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
                 

        #TODO turn this into averages

        #algo_util_auction = []
        #for auction in range(0, num_auctions):
        #    algo_util_auction.append((bidder.reward_func[auction][t][arm_chosen]*bidder.alloc_func[auction][t][arm_chosen]))
    

        #algo_util.append(np.mean(algo_util_auction)-1)
        # We compute the regret only for the learner 
        algo_util.append(bidder[0].avg_reward[t][arm_chosen[0]] - 1)
        temp_regr.append(regret(0, bidder[0].reward_func, bidder[0].alloc_func, bidder[0].bid_space, algo_util, t,num_auctions))
        #print bids[t]
        temp_bids.append(bids[t][:num_adaptive])

    return (temp_regr,temp_bids)   


