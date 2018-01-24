########
# File that specifies the auction parameters to be used in each iteration. The same parameters are used subsequently by each repetition.
########


import numpy as np
import random

def set_auction_params(T,num_repetitions):
    num_bidders         = 5
    num_slots           = 3
    outcome_space       = 2
    #rank_scores = [0.700573810327246, 0.3110979655260716, 0.610430432163001, 0.03395812562678002, 0.8345253204018921]
    #ctr  = [0.97, 0.9, 0.57]
    #reserve = 0.1 
    #Create the rank scores (different at every t)
    #TODO: here I have assumed oblivious adversary
    #rank_scores = [[np.random.uniform(0,1) for i in range(0,num_bidders)] for j in range(0,T)]
    #ctr  = [[round(np.random.uniform(0.01,1), 2) for i in range(0,num_slots)] for j in range(0,T)]        
    
    rank_scores = [[0.12211550104237634, 0.8590194489130824, 0.2285404998534355, 0.11572885850955617, 0.25187157118899417], [0.7698389049349788, 0.6653921610038741, 0.9290202725696304, 0.15861628208461964, 0.7701639991708517], [0.8093644279074449, 0.08407252891930495, 0.750519856207743, 0.5833226859494088, 0.07680701089790909]]
    ctr = [[0.88, 0.66, 0.57], [0.99, 0.38, 0.01], [0.58, 0.32, 0.29]]
     
    #for t in range(0, T):
    #    ctr[t].sort(reverse=True)
    #reserve = [round(np.random.uniform(0,0.3),2) for i in range(0,T)]
    reserve = [0.18, 0.08, 0.07] 
    # value function for every slot
    # could be seen as the conversion rate for every slot
    #values = [[round(np.random.uniform(0,1),2) for j in range(0,num_slots)] for j in range(0,T)]
    values = [ [0.9, 0.56, 0.7], [0.59, 1.0, 0.59], [0.44, 0.37, 0.88]]

    return (num_bidders, num_slots, outcome_space,rank_scores, ctr, reserve, values)
