############ 
# Implements the regret both in the discretized case
############ 

import numpy as np

# TODO we need to run each instance of T rounds *multiple times* and take the average
# Arguments: 
# - cont: 0 when discrete, 1 when continuous
# - v_lst: 2D list with the realized valuations (size: num_rounds x bid_space)
# - p_lst: 2D list with the realized payments (size: num_rounds x bid_space)
# - alloc: 2D list with the realized allocation (size: num_rounds x bid_space)
# - bid_space: number of arms
# - algo_util: list with the utility that our algorithm has acquired (size: T) 
def regret(cont, v_lst, p_lst, alloc, bid_space, algo_util):
    if cont == 0: #discrete case
        util = []
        for i in range(0,bid_space-1):
            util_lst = [(v_lst[j][i] - p_lst[j][i])*(alloc[j][i]) for j in range(0,len(v_lst)-1)]
            util.append(sum(util_lst))
        max_util_hindsight = np.max(util)
    else: #continuous case
        # for now, we're not comparing with the continuous case
    return (max_util_hindsight - sum(algo_util))
