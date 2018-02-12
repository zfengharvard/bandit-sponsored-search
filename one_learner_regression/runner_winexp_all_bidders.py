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


def main_winexp(bidder,curr_rep, T,num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids):
    algo_util = []
    temp_regr = []
    for t in range(0,T):
        bid_chosen = round(bidder.bidding(),2)
        # same bid over all auctions that run at the same timestep
        bids[t][0] = bid_chosen
        #every bidder is a learner and they all should update the estimated utility that they get
        allocated = GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder.id, bids[t][bidder.id])
        bidder.alloc_func[t] = [GSP(ctr[t], reserve[t], bids[t], rank_scores[t], num_slots, num_bidders).alloc_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]
        #reward function: value - payment(coming from GSP module)
        bid_vec = deepcopy(bids[t])
        bidder.pay_func[t] = [GSP(ctr[t], reserve[t], bid_vec, rank_scores[t], num_slots, num_bidders).pay_func(bidder.id, bid*bidder.eps) for bid in range(0, bidder.bid_space)]  
        bidder.reward_func[t] = compute_reward(bidder.alloc_func[t], bidder.pay_func[t], ctr[t], values[t])
        #print ("Bidder's Reward Function")
        #print bidder.reward_func[t]
        #### WIN-EXP computations ####
        if allocated != 0: #only if he gets allocated originally he can get information     
            #updates the bidder's estimate of the utility
            bidder.utility[t] = (bidder.compute_utility(1, bidder.reward_func[t], bidder.alloc_func[t]))
        else:
            bidder.utility[t] = (bidder.compute_utility(0, bidder.reward_func[t], bidder.alloc_func[t]))
        #TODO check what the probability of the outcome should be in this case
        #bidder.utility[t] = [0 if bidder.utility[t][bb] == -0.0 else bidder.utility[t][bb] for bb in range(0,bidder.bid_space)]


        #TODO check again
        #for b in range(0, bidder.bid_space):
        #    u_s = 0
        #    for auction in range(0,num_auctions):
        #        u_s += bidder.reward_func[auction][t][b]*bidder.alloc_func[auction][t][b] 
        #    #bidder.avg_utility[t].append(bidder.avg_reward[t][b]-1)
        #    bidder.avg_reward[t].append(u_s/num_auctions)
        #    bidder.avg_utility[t].append(bidder.avg_reward[t][b]-1)

        (bidder.weights, bidder.pi) = bidder.weights_update_winexp(bidder.eta_winexp, bidder.utility[t])        
        # for each auction (at the same t) you choose the same arm
        arm_chosen = int(math.ceil(bids[t][bidder.id]/bidder.eps))   

        #TODO turn this into averages

        #algo_util_auction = []
        #for auction in range(0, num_auctions):
        #    algo_util_auction.append((bidder.reward_func[auction][t][arm_chosen]*bidder.alloc_func[auction][t][arm_chosen]))
    

        #algo_util.append(np.mean(algo_util_auction)-1)
        algo_util.append(bidder.reward_func[t][arm_chosen]*bidder.alloc_func[t][arm_chosen] - 1)
        temp_regr.append(regret(0, bidder.reward_func, bidder.alloc_func, bidder.bid_space, algo_util, t))

    return temp_regr   


