########
# File that specifies the auction parameters to be used in each iteration. The same parameters are used subsequently by each repetition.
########


import numpy as np
import random
import math

def set_auction_params(T,num_repetitions):
    num_bidders         = 20
    num_slots           = 3
    outcome_space       = 2
    #Create the rank scores. Size of rank_scores: T x num_bidders
    rank_scores = [[np.random.uniform(0,1) for i in range(0,num_bidders)] for _ in range(0,T)]  
    # at every t, the rank scores are the same, irrespective of the auction that we're currently participating in
    #size of CTR: T x num_slots
    ctr  = [[np.random.uniform(0.5,1) for _ in range(0,num_slots)] for _ in range(0,T)] 
    for t in range(0, T):
        ctr[t].sort(reverse=True)
    
    #size of reserve: num_auctions x T
    reserve = [np.random.uniform(0,0.3) for i in range(0,T)]   
    # value function for every slot
    # could be seen as the conversion rate for every slot
    # size of values:  T x num_bidders 
    values = [[np.random.uniform(0,1) for j in range(0,num_bidders)] for _ in range(0,T)]
    # threshold ctr to decide whether or you get clicked or not
    threshold = [np.random.uniform(0,1) for _ in range(0,T)]
    #threshold = np.random.binomial(1,0.5,T)

    # gaussian noise on all timesteps on all slots
    # we assume that the last slot + 1 corresponds to the "no-allocation" case
    #noise = [np.random.normal(0,math.sqrt(1.0/100),num_slots+1) for _ in range(0,T)]
    noise = [[0 for _ in range(0,num_slots+1)] for _ in range(0,T)]
    
    return (num_bidders, num_slots, outcome_space,rank_scores, ctr, reserve, values, threshold,noise)
