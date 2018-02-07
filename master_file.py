import numpy as np
import random
import math
from copy import deepcopy
from runner_winexp_all_bidders import *
from runner_exp3_all_bidders import *


def regret_winexp(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, bids, num_auctions):
    f1 = "winexp_regrets.txt"
    winexp_regrets = open(f1, "w")
    #winexp_regr is now a num_repetitionsxT matrix
    winexp_regr = []
    for rep in range(0, num_repetitions):
        # at each repetition, a whole array of size T is returned: This corresponds to the regrets at each one of the T rounds
        winexp_regr.append(main_winexp(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, num_auctions))
        #print ("Current Regrets")
        #print winexp_regr[rep]
        bidder.pi             = [1.0/bidder.bid_space for j in range(0,bidder.bid_space)]
        bidder.weights        = [1 for j in range(0,bidder.bid_space)]
        bidder.utility        = [[[] for i in range(0, T)] for _ in range(0,num_auctions)]
        bidder.avg_utility    = [[] for i in range(0,T)]
        bidder.avg_reward     = [[] for i in range(0,T)]
        bidder.alloc_func     = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
        bidder.pay_func       = [[] for t in range(0,T)]
        bidder.reward_func    = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]

 
    winexp_expected_regr = []
    for t in range(0,T):
        tmp = 0
        for r in range(0,num_repetitions):
            tmp += winexp_regr[r][t]
        winexp_expected_regr.append(tmp/num_repetitions)

    for r in range(0,num_repetitions):
        s = ""
        for t in range(0,T):
            s += ("%.5f "%winexp_regr[r][t])
        s += "\n"
        winexp_regrets.write(s) 
    

    #final_winexp_regr = [winexp_expected_regr[t]/t for t in range(1,T-1)]
    final_winexp_regr = winexp_expected_regr
    return final_winexp_regr 


def regret_exp3(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, num_auctions):
    f2 = "exp3_regrets.txt"
    exp3_regrets = open(f2,"w")
    #exp3_regr is now a num_repetitionsxT matrix
    exp3_regr = []
    for rep in range(0, num_repetitions):
        #print ("Repetition rep %d for exp3"%rep)
        # at each repetition, a whole array of size T is returned: This corresponds to the regrets at each one of the T rounds
        exp3_regr.append(main_exp3(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, num_auctions))
        bidder.loss           = [0 for j in range(0,bidder.bid_space)]
        bidder.pi             = [1.0/bidder.bid_space for j in range(0,bidder.bid_space)]
        bidder.weights        = [1 for j in range(0,bidder.bid_space)]
        bidder.utility        = [[[] for i in range(0, T)] for _ in range(0,num_auctions)]
        bidder.avg_utility    = [[] for i in range(0,T)]
        bidder.avg_reward     = [[] for i in range(0,T)]
        bidder.alloc_func     = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
        bidder.pay_func       = [[] for t in range(0,T)]
        bidder.reward_func    = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
 
    #print ("Big regret list")
    #print exp3_regr

    exp3_expected_regr = []
    for t in range(0,T):
        tmp = 0
        for r in range(0,num_repetitions):
            tmp += exp3_regr[r][t]
        exp3_expected_regr.append(tmp/num_repetitions)

    for r in range(0,num_repetitions):
        s = ""
        for t in range(0,T):
            s += ("%.5f "%exp3_regr[r][t])
        s += "\n"
        exp3_regrets.write(s) 

    #final_exp3_regr = [exp3_expected_regr[t]/t for t in range(1,T-1)]
    print ("Inside master_file.py")
    print ("Expected regret (div by num_repetitions")
    final_exp3_regr = exp3_expected_regr
    print final_exp3_regr
    return (final_exp3_regr)
