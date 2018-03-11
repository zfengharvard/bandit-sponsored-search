###################
# Gets requests from the runner-dp file.
# Computes the regret of the winexp and exp3 algoritmhs using the parameters
# that it gets from runner-dp.py.
##################

import numpy as np
import random
import math
from copy import deepcopy
from runner_winexp_all_bidders import *
from runner_exp3_all_bidders import *


def regret_winexp(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, bids,threshold,noise):
    f1 = "winexp_regrets.txt"
    winexp_regrets = open(f1, "w")
    #winexp_regr is now a num_repetitionsxT matrix
    winexp_regr = []
    for rep in range(0, num_repetitions):
        # at each repetition, a whole array of size T is returned: This corresponds to the regrets at each one of the T rounds
        winexp_regr.append(main_winexp(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, threshold,noise))
        bidder.pi             = [1.0/bidder.bid_space for j in range(0,bidder.bid_space)]
        bidder.weights        = [1 for j in range(0,bidder.bid_space)]
        bidder.utility        = [[] for i in range(0,T)] 
        bidder.alloc_func     = [[] for t in range(0,T)] 
        bidder.pay_func       = [[] for t in range(0,T)]
        bidder.reward_func    = [[] for t in range(0,T)] 
        

    winexp_expected_regr = []
    for t in range(0,T):
        winexp_expected_regr.append(sum(d[t] for d in winexp_regr)/num_repetitions)

    for r in range(0,num_repetitions):
        s = ""
        for t in range(0,T):
            s += ("%.5f "%winexp_regr[r][t])
        s += "\n"
        winexp_regrets.write(s) 
    

    final_winexp_regr = winexp_expected_regr
    winexp_regrets.close()
    return (final_winexp_regr, winexp_regr)


def regret_exp3(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold, noise):
    f2 = "exp3_regrets.txt"
    exp3_regrets = open(f2,"w")
    #exp3_regr is now a num_repetitionsxT matrix
    exp3_regr = []
    for rep in range(0, num_repetitions):
        # at each repetition, a whole array of size T is returned: This corresponds to the regrets at each one of the T rounds
        exp3_regr.append(main_exp3(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold,noise))
        bidder.loss           = [0 for j in range(0,bidder.bid_space)]
        bidder.pi             = [1.0/bidder.bid_space for j in range(0,bidder.bid_space)]
        bidder.weights        = [1 for j in range(0,bidder.bid_space)]
        bidder.alloc_func     = [[] for t in range(0,T)]  
        bidder.pay_func       = [[] for t in range(0,T)]
        bidder.reward_func    = [[] for t in range(0,T)] 
        bidder.utility        = [[] for t in range(0,T)] 
 

    for r in range(0,num_repetitions):
        s = ""
        for t in range(0,T):
            s += ("%.5f "%exp3_regr[r][t])
        s += "\n"
        exp3_regrets.write(s) 

        
    # compute the cumulative regret for the number of repetitions we ran rounds 0->T
    exp3_expected_regr = []
    for t in range(0,T):
        exp3_expected_regr.append(sum(d[t] for d in exp3_regr)/num_repetitions)

    final_exp3_regr = exp3_expected_regr
    exp3_regrets.close()
    return (final_exp3_regr, exp3_regr)


