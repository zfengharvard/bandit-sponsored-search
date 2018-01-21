import numpy as np
import random
import math
from copy import deepcopy
from runner_winexp_all_bidders import *
from runner_exp3_all_bidders import *


def regret_winexp(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values):
    winexp_regr = []
    for rep in range(0, num_repetitions):
        winexp_regr.append(main_winexp(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values))

        # After each repetition, re-initialize the weights and the probabilities of the arm

        for i in range(0, num_bidders):
            bidder[i].pi         = [bidder[i].eps for j in range(0,bidder[i].bid_space)]
            bidder[i].weights    = [1 for j in range(0,bidder[i].bid_space)]
            bidder[i].utility    = [[] for j in range(0, T)]
            bidder[i].alloc_func = [[] for t in range(0,T)]
            bidder[i].pay_func   = [[] for t in range(0,T)]
            bidder[i].reward_func = [[] for t in range(0,T)]

    winexp_expected_regr = sum(winexp_regr)/num_repetitions

    print ("WIN-EXP expected regret for T=%d"%T)
    print winexp_expected_regr


def regret_exp3(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values):
    exp3_regr = [] 
    for rep in range(0, num_repetitions):
        exp3_regr.append(main_exp3(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values)
        # After each repetition, re-initialize the weights and the probabilities of the arm

        for i in range(0, num_bidders):
            bidder[i].pi         = [bidder[i].eps for j in range(0,bidder[i].bid_space)]
            bidder[i].weights    = [1 for j in range(0,bidder[i].bid_space)]
            bidder[i].utility    = [[] for j in range(0, T)]
            bidder[i].alloc_func = [[] for t in range(0,T)]
            bidder[i].pay_func   = [[] for t in range(0,T)]
            bidder[i].reward_func = [[] for t in range(0,T)]

    exp3_expected_regr = sum(exp3_regr)/num_repetitions

    print ("EXP3 expected regret for T=%d"%T)
    print exp3_expected_regr
