########
# File that specifies the auction parameters to be used in each iteration. The same parameters are used subsequently by each repetition.
########


import numpy as np
import random

def set_auction_params(T,num_repetitions,num_auctions):
    num_bidders         = 20
    num_slots           = 2
    outcome_space       = 2
    #Create the rank scores. Size of rank_scores: num_auctions x T x num_bidders
    # rank scores size: num_auctions x T x num_slots
    rank_scores = [[[np.random.uniform(0,1) for i in range(0,num_bidders)] for j in range(0,T)] for _ in range(0,num_auctions)]
    # at every t, the rank scores are the same, irrespective of the auction that we're currently participating in
    
    #size of CTR: num_auctions x T x num_slots
    ctr  = [[[np.random.uniform(0.01,1) for i in range(0,num_slots)] for j in range(0,T)] for _ in range(0,num_auctions)]

    for auction in range(0, num_auctions):
        for t in range(0, T):
            ctr[auction][t].sort(reverse=True)
    
    #size of reserve: num_auctions x T
    reserve = [[np.random.uniform(0,0.3) for i in range(0,T)] for _ in range(0, num_auctions)]   
    # value function for every slot
    # could be seen as the conversion rate for every slot
    # size of values: num_auctions x T x num_slots
    values = [[[np.random.uniform(0,1) for j in range(0,num_slots)] for _ in range(0,T)] for _ in range(0,num_auctions)]
    #print ("Rank Scores")
    #print rank_scores
    #print ("CTR")
    #print ctr
    #print ("reserve")
    #print reserve
    #print ("values")
    #print values


    return (num_bidders, num_slots, outcome_space,rank_scores, ctr, reserve, values)
