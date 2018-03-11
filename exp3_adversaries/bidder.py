############ 
# Implements Bidder Class 
# Includes Functions: 
# - prob_outcome
# - compute_utility
# - weights_update_winexp
# - bidding
############ 

import random
import numpy as np
from probability import draw
import math


class Bidder(object):

    # Each bidder has a unique id and we 
    # differentiate bidders based on that number.
    # Also, each bidder can choose a different discretization
    def __init__(self, bidder_id, eps, T, outcome_space, num_repetitions):
        self.id             = bidder_id
        self.eps            = eps
        self.bid_space      = int(1.0/self.eps) + 1
        # initialization of the probabilities for each arm
        self.pi             = [1.0/self.bid_space for i in range(0,self.bid_space)]
        self.weights        = [1 for i in range(0,self.bid_space)]
        self.eta_winexp     = math.sqrt(2*math.log(self.bid_space,2)/(5*T))
        self.eta_exp3       = math.sqrt(1.0*(2*math.log(self.bid_space,2))/(T*self.bid_space))
        self.eta_gexp3      = 0.95*math.sqrt(math.log(self.bid_space,2)/(T*self.bid_space))
        self.beta           = math.sqrt(math.log(self.bid_space,2)*(1/0.01)/(T*self.bid_space))
        self.loss           = [0 for i in range(0,self.bid_space)]
        self.utility        = [[] for i in range(0, T)]
        self.winexp_regret  = [0]*num_repetitions 
        self.exp3_regret    = [0]*num_repetitions
        self.alloc_func     = [[] for t in range(0,T)] 
        self.pay_func       = [[] for t in range(0,T)]
        self.reward_func    = [[] for t in range(0,T)]    
    # P[o_t]: probability of seeing outcome o_t
    # pi[b] is the probability of bid b being chosen
    # alloc[2] = x_t(1*eps), pi[2] = pi_t(1*eps)
    def prob_outcome(self,alloc):
        p   = [self.pi[b]*alloc[b] for b in range(0,self.bid_space)]
        return sum(p)
        
    # Compute estimate of utility from observed allocation
    # outcome and reward function (which is given to us
    # as a list)
    def compute_utility(self, reward_won, reward_func, alloc):
        if reward_won == 1:
            return [1.0*(reward_func[b] - 1)*(alloc[b])/(self.prob_outcome(alloc)) for b in range(0,self.bid_space)] 
        else:
            return [-1.0*(1 - alloc[b])/(1 - self.prob_outcome(alloc)) for b in range(0,self.bid_space)] 

    # Multiplicative Weights Update according to winexp
    # Updates weights list and returns the list of probabilities for each arm    
    def weights_update_winexp(self, eta, estimated_utility):
        self.weights = [self.weights[b]*math.exp(eta*estimated_utility[b]) for b in range(0,self.bid_space)]
        self.pi      = [self.weights[b]/sum(self.weights) for b in range(0,self.bid_space)]
        return (self.weights, self.pi)

    # Choosing a bid according to exp3/win_exp
    # Returns the bid (==arm*eps) (to be submitted to the auctioneer)
    def bidding(self):
        bid              = draw(self.pi)
        return (bid*self.eps)
    
    def gbidding(self, weights,gamma):
        probs            = distr(weights,gamma)
        bid              = draw_gexp3(probs)
        return (bid*self.eps)


