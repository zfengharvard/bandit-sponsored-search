############ 
# Implements the regret both in the discretized case
# All functions in this module are from the perspective of a single bidder.
# The aggregate regret for all bidders is computed in the master file.
############ 

import numpy as np

def regret(r_lst, alloc, bid_space, algo_util, T):
    # size of tmp: T x bid_space
    tmp = [[0 for _ in range(0,bid_space)] for _ in range(0,T+1)]

    for t in range(0,T+1):
        for b in range(0,bid_space):
            tmp[t][b] += r_lst[t][b]*alloc[t][b]


    util = []
    for b in range(0,bid_space):
        s = 0
        for t in range(0,T+1):
            s += tmp[t][b]
        util.append(s)
        

    max_util_hindsight = np.max(util)
    print ("Algorithm's Utility: %f"%(sum(algo_util)))
    print ("Best fixed: %f"%max_util_hindsight)
        # for now, we're not comparing with the continuous case
    print ("Regret:%f"%(max_util_hindsight-sum(algo_util)))
    return (max_util_hindsight - sum(algo_util))




def regret2(reward,alloc,bid_space,algo_util,T,num_auctions):
    util = []
    for b in range(0,bid_space):
        s = 0
        for t in range(0,T+1):
            s += reward[t][b]*(alloc[t][b])
        util.append(s)

    max_util_hindsight = np.max(util)
    print ("Algorithm's Utility: %f"%(sum(algo_util)))
    print ("Best fixed: %f"%max_util_hindsight)
        # for now, we're not comparing with the continuous case
    print ("Regret:%f"%(max_util_hindsight-sum(algo_util)))
    return (max_util_hindsight - sum(algo_util))




