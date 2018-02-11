############ 
# Implements the regret both in the discretized case
# All functions in this module are from the perspective of a single bidder.
# The aggregate regret for all bidders is computed in the master file.
############ 

import numpy as np

# Arguments: 
# - cont: 0 when discrete, 1 when continuous
# - r_lst: 3D list with the realized rewards (size: num_auctions x num_rounds x bid_space)
# - alloc: 3D list with the realized allocation (size: num_auctions x num_rounds x bid_space)
# - bid_space: number of arms
# - algo_util: list with the utility that our algorithm has acquired for the submitted bid of the bidder (size: T) 
def regret(cont, r_lst, alloc, bid_space, algo_util, T, num_auctions):
    if cont == 0: #discrete case
        # size of tmp: T x bid_space
        tmp = [[] for _ in range(0,T+1)]

        #print ("Inside regret")
        #print ("r_lst")
        #print r_lst
        #print ("alloc")
        #print alloc

        for t in range(0,T+1):
            u_s = [0 for _ in range(0,bid_space)]
            for b in range(0,bid_space):
                for auction in range(0,num_auctions):
                    u_s[b] += r_lst[auction][t][b]*alloc[auction][t][b]

                u_s[b] = u_s[b]/num_auctions - 1
            tmp[t] = u_s
        #print ("Utility inside regret for timestep T=%d"%T)
        #print tmp

        util = []
        for b in range(0,bid_space):
            s = 0
            for t in range(0,T+1):
                s += tmp[t][b]
            util.append(s)
            

        max_util_hindsight = np.max(util)
    else: #continuous case
        return
    print ("Algorithm's Utility: %f"%(sum(algo_util)))
    print ("Best fixed: %f"%max_util_hindsight)
        # for now, we're not comparing with the continuous case
    return (max_util_hindsight - sum(algo_util))
