import numpy as np
import random
import math
from copy import deepcopy
from runner_winexp_all_bidders import *
from runner_exp3_all_bidders import *
from multiprocessing import Pool

winexp_regr = []
exp3_regr   = []


def log_winexp_results(res):
    winexp_regr.append(res)

def log_exp3_results(res):
    exp3_regr.append(res)

def regret_winexp(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, bids,threshold,noise):
    f1 = "winexp_regrets.txt"
    winexp_regrets = open(f1, "w")
    #winexp_regr is now a num_repetitionsxT matrix
    
    pool = Pool(processes = num_repetitions)
    results = [pool.apply_async(main_winexp, args = (bidder[rep],rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, threshold,noise), callback = log_winexp_results) for rep in range(0,num_repetitions)]
    

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
    

    #final_winexp_regr = [winexp_expected_regr[t]/t for t in range(1,T-1)]
    final_winexp_regr = winexp_expected_regr
    winexp_regrets.close()
    return (final_winexp_regr, winexp_regr)


def regret_exp3(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids,threshold, noise):
    f2 = "exp3_regrets.txt"
    exp3_regrets = open(f2,"w")
    #exp3_regr is now a num_repetitionsxT matrix
    pool = Pool(processes=num_repetitions)
    results = [pool.apply_async(main_exp3, args = (bidder[rep],rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,bids, threshold,noise), callback = log_exp3_results) for rep in range(0,num_repetitions)]
    

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
    exp3_regrets.close()
    return (final_exp3_regr, exp3_regr)


