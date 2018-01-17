###################
# Implements GSP class
# Includes Functions:
# - compute: return allocated slot and per-click-payment
# - alloc_func: return allocation function for the learner
# - payment_func: return payment function
###################


import numpy as np
import random
import math


class GSP(object):
    """
    Implements the generalized second price auction mechanism.
    """
    ##########
    # ctr: a vector of click-through-rate
    # r: rankscore reserve
    # b: a vector of the bids from bidders
    # s: a vector of the scores associated with each bidder
    # m: number of slots
    # n: number of bidders
    
    def __init__(self, ctr, r, b, s, m, n):
        self.ctr = ctr
        self.r = r
        self.b = b
        self.s = s
        self.m = m
        self.n = n
        
        
    def compute(self):
        rankscores = zip(range(0,self.n), [x*y for x,y in zip(self.b, self.s)])
        valid = lambda (a, bid): bid >= self.r
        valid_bids = filter(valid, rankscores)
        rev_cmp_bids = lambda (a1, b1), (a2, b2): cmp(b2, b1)
        # sort the valid (weighted) rankscores decreasingly
        valid_bids.sort(rev_cmp_bids)
        allocated_bids = valid_bids[:self.m]
        if len(allocated_bids) == 0:
            return ([], [])
        
        (allocation, just_bids) = zip(*allocated_bids)
        allocated_s = [self.s[i] for i in allocation[:(self.m-1)]]
        # compute the per-click-payment of the bidders except for the last bidder
        pc_payment = [x/y for x,y in zip(list(just_bids[1:]), allocated_s)]
        if len(valid_bids) > self.m:
            last_payment = valid_bids[self.m][1]/self.s[allocation[-1]]
        else:
            last_payment = self.r/self.s[allocation[-1]]
            
        pc_payment.append(last_payment)
        return(list(allocation), pc_payment)
        
    '''
    The following function returns the allocation probability(ctr) of the 
    corresponding bidder with bid=Bid given the others' bids
    '''
    def alloc_func(self, bidder_id, Bid):
        if Bid * self.s[bidder_id] < self.r:
            return 0
        else:
            # Count how many bidders have higher rankscores than this bidder
            k = 0
            for i in range(self.n):
                if i == bidder_id:
                    k += 0
                else:
                    if self.b[i] * self.s[i] >= Bid * self.s[bidder_id]:
                        k += 1
                    else:
                        k += 0
            # return the allocation probability (CTR)
            if k > self.m - 1:
                return 0
            else:
                return self.ctr[int(k)]
         
    '''
    The following function returns the per-click-payment of the 
    corresponding bidder with bid given the others' bids
    '''  
    def pay_func(self, bidder_id, Bid):
        self.b[bidder_id] = Bid
        rankscores = zip(range(0,self.n), [x*y for x,y in zip(self.b, self.s)])
        valid = lambda (a, bid): bid >= self.r
        valid_bids = filter(valid, rankscores)
        rev_cmp_bids = lambda (a1, b1), (a2, b2): cmp(b2, b1)
        # sort the valid (weighted) rankscores decreasingly
        valid_bids.sort(rev_cmp_bids)
        allocated_bids = valid_bids[:self.m]
        
        if len(allocated_bids) == 0:
            return 0
        (allocation, just_bids) = zip(*allocated_bids)
        if len(valid_bids) > self.m:
            last_payment = valid_bids[self.m][1]/self.s[allocation[-1]]
        else:
            last_payment = self.r/self.s[allocation[-1]]
        
        if bidder_id in list(allocation):
            rank = list(allocation).index(bidder_id)
            if rank < self.m-1:
                return list(just_bids)[rank+1]/self.s[bidder_id]
            else:
                return last_payment        
                
        else:
            return 0
           
