############ 
# Implements the regret both in the discretized case and
# in the continuous
############ 

import numpy as np

def indicator(bid,price):
    if bid >= price:
        return 1
    else:
        return 0

# Reward List is the list of the utilities that were realized
# Reward List is a Txbid_space matrix
# The allocation function is also a Txbid_space matrix
# Because the regret that we compute is expected regret
# TODO we need to run each instance of T rounds *multiple times* and take the average
def regret(cont, v_lst, p_lst, alloc, eps, bid_space):
    if cont == 0: #discrete case
        util = []
        for i in range(0,bid_space-1):
            util_lst = [(v_lst[j][i] - p_lst[j][i])*(alloc[j][i]) for j in range(0,len(v_lst)-1)]
            util[i] = sum(util_lst)
        max_util_hindsight = np.max(util)
    else: #continuous case
        # for now, we're not comparing with the continuous case
    return max_util_hindsight
