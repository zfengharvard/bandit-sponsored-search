import numpy as np
import random
import math
from copy import deepcopy
from runner_winexp_all_bidders import *
from runner_exp3_all_bidders import *
from runner_gexp3_all_bidders import *
from multiprocessing import Pool

winexp_regr = []
exp3_regr   = []


def log_winexp_results(res):
    winexp_regr.append(res)

def log_exp3_results(res):
    exp3_regr.append(res)

def regret_winexp(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, bids,threshold,noise,num_adaptive):
    f1 = "winexp_regrets.txt"
    winexp_regrets = open(f1, "w")
    #winexp_regr is now a num_repetitionsxT matrix

    pool = Pool(processes = num_repetitions)
    results = [pool.apply_async(main_winexp, args = (bidder[rep],rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, threshold,noise,num_adaptive), callback = log_winexp_results) for rep in range(0,num_repetitions)]

    pool.close()
    pool.join()

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


def regret_exp3(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold, noise,num_adaptive):
    f2 = "exp3_regrets.txt"
    exp3_regrets = open(f2,"w")
    #exp3_regr is now a num_repetitionsxT matrix
    pool = Pool(processes=num_repetitions)
    results = [pool.apply_async(main_exp3, args = (bidder[rep],rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, threshold,noise, num_adaptive), callback = log_exp3_results) for rep in range(0,num_repetitions)]
    

    pool.close()
    pool.join()   

    for r in range(0,num_repetitions):
        s = ""
        for t in range(0,T):
            s += ("%.5f "%exp3_regr[r][t])
        s += "\n"
        exp3_regrets.write(s) 
        
    # below, we compute the cumulative regret for the number of repetitions we ran rounds 0->T
    exp3_expected_regr = []
    for t in range(0,T):
        exp3_expected_regr.append(sum(d[t] for d in exp3_regr)/num_repetitions)

    final_exp3_regr = exp3_expected_regr
    #print final_exp3_regr
    exp3_regrets.close()
    return (final_exp3_regr, exp3_regr)


def regret_gexp3(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,num_auctions):
    f2 = "gexp3_regrets.txt"
    gexp3_regrets = open(f2,"w")
    #exp3_regr is now a num_repetitionsxT matrix
    gexp3_regr = []
    for rep in range(0, num_repetitions):
        #print ("Repetition rep %d for exp3"%rep)
        # at each repetition, a whole array of size T is returned: This corresponds to the regrets at each one of the T rounds
        gexp3_regr.append(main_gexp3(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,num_auctions))
        #print ("Current Regrets")
        #print exp3_regr
        bidder.loss           = [0 for j in range(0,bidder.bid_space)]
        bidder.pi             = [1.0/bidder.bid_space for j in range(0,bidder.bid_space)]
        bidder.weights        = [1 for j in range(0,bidder.bid_space)]
        bidder.avg_utility    = [[] for i in range(0, T)]
        bidder.avg_reward     = [[] for i in range(0, T)]
        bidder.alloc_func     = [[[] for t in range(0,T)] for _ in range(0,num_auctions)] 
        bidder.pay_func       = [[] for t in range(0,T)]
        bidder.reward_func    = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
        bidder.utility        = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
 
    #print ("Big regret list")
    #print exp3_regr

    #for r in range(0,num_repetitions):
    #    s = ""
    #    for t in range(0,T):
    #        s += ("%.5f "%exp3_regr[r][t])
    #    s += "\n"
        #exp3_regrets.write(s) 
    #exp3_expected_regr = []
    #for t in range(0,T):
    #    tmp = 0
    #    for r in range(0,num_repetitions):
    #        tmp += exp3_regr[r][t]
    #    exp3_expected_regr.append(tmp/num_repetitions)

        
    # below, we compute the cumulative regret for the number of repetitions we ran rounds 0->T
    gexp3_expected_regr = []
    for t in range(0,T):
        gexp3_expected_regr.append(sum(d[t] for d in gexp3_regr)/num_repetitions)

    #print ("Inside master_file.py")
    #print ("Expected regret (div by num_repetitions)")
    final_gexp3_regr = gexp3_expected_regr
    #print final_exp3_regr
    gexp3_regrets.close()
    return (final_gexp3_regr)
