############ 
# Implements the regret both in the discretized case
# All functions in this module are from the perspective of a single bidder.
# The aggregate regret for all bidders is computed in the master file.
############ 

import numpy as np

# Arguments: 
# - cont: 0 when discrete, 1 when continuous
# - r_lst: 2D list with the realized rewards (size: num_rounds x bid_space)
# - alloc: 1D list with the realized allocation (size: bid_space)
# - bid_space: number of arms
# - algo_util: list with the utility that our algorithm has acquired for the submitted bid of the bidder (size: T) 
def regret(cont, r_lst, alloc, bid_space, algo_util, T):
    if cont == 0: #discrete case
        tmp  = []
        for t in range(0, T):
            tmp.append([r_lst[t][b]*alloc[t][b] - 1 for b in range(0,bid_space)])
        util = []
        for b in range(0,bid_space):
            util.append(sum(tt[b] for tt in tmp))
            
        max_util_hindsight = np.max(util)
    else: #continuous case
        return
    print ("Algorithm's Utility: %f"%sum(algo_util))
    print ("Best fixed: %f"%max_util_hindsight)
        # for now, we're not comparing with the continuous case
    return (max_util_hindsight - sum(algo_util))
