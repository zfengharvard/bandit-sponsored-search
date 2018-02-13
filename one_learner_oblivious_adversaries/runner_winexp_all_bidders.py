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
            reward_lst.append(values - payment_func[allocation_func.index(b)])
        else :
            reward_lst.append(-1)
    return reward_lst


def main_winexp(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,num_auctions, threshold):
    algo_util = []
    temp_regr = []
    for t in range(0,T):
        bid_chosen = bidder.bidding()
        # same bid over all auctions that run at the same timestep
        auctions_won = 0
        for auction in range(0,num_auctions):
            bids[auction][t][0] = bid_chosen
            bid_vec = deepcopy(bids[auction][t])
            gsp_instance =GSP(ctr[auction][t], reserve[auction][t], bid_vec, rank_scores[auction][t], num_slots, num_bidders) 
            allocated = gsp_instance.alloc_func(bidder.id, bids[auction][t][bidder.id])
            bidder.alloc_func[auction][t] = [gsp_instance.alloc_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]
            #reward function: value - payment(coming from GSP module)
            bidder.pay_func[t] = [gsp_instance.pay_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]  
            bidder.reward_func[auction][t] = compute_reward(bidder.alloc_func[auction][t], bidder.pay_func[t], ctr[auction][t], values[auction][t][0])
            #print ("Bidder's Reward Function")
            #print bidder.reward_func[t]
            #### WIN-EXP computations ####
            #print ("allocated: %.5f"%allocated)
            if allocated > threshold[t]: #only if he passes threshold ctr he can get information     
                auctions_won += 1
                bidder.utility[auction][t] = (bidder.compute_utility(1, bidder.reward_func[auction][t], bidder.alloc_func[auction][t]))
            else:
                bidder.utility[auction][t] = (bidder.compute_utility(0, bidder.reward_func[auction][t], bidder.alloc_func[auction][t]))
            #bidder.utility[t] = [0 if bidder.utility[t][bb] == -0.0 else bidder.utility[t][bb] for bb in range(0,bidder.bid_space)]

        u_s = [0 for _ in range(0,bidder.bid_space)]
        r_s = [0 for _ in range(0,bidder.bid_space)]
        for b in range(0, bidder.bid_space):
            for auction in range(0,num_auctions):
                u_s[b] += bidder.utility[auction][t][b]
                r_s[b] += bidder.reward_func[auction][t][b]*bidder.alloc_func[auction][t][b]
            bidder.avg_utility[t].append(u_s[b]/num_auctions) 
            #bidder.avg_utility[t].append(u_s[b]/num_auctions - 1) 
            #bidder.avg_utility[t].append(u_s[b]/num_auctions + (num_auctions - auctions_won)/(num_auctions))
            bidder.avg_reward[t].append(r_s[b]/num_auctions)

        (bidder.weights, bidder.pi) = bidder.weights_update_winexp(bidder.eta_winexp, bidder.avg_utility[t])        
        # for each auction (at the same t) you choose the same arm
        arm_chosen = int(math.ceil(bids[0][t][bidder.id]/bidder.eps))   

        algo_util.append(bidder.avg_reward[t][arm_chosen] - 1)
        temp_regr.append(regret(0, bidder.reward_func, bidder.alloc_func, bidder.bid_space, algo_util, t,num_auctions))

    return temp_regr   


