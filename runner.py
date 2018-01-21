from bidder import *
from master_file import regret_winexp, regret_exp3
from auction_parameters import set_auction_params


num_repetitions = 2
for T in range(3,4):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions)
    # Preferred Discretizations for the bidders
    epsilon = []
    for i in range(0,num_bidders):
        epsilon.append(0.1)

    # Create the bidders and store them in a list
    bidder = [] #list of bidder objects
    for i in range(0,num_bidders):
        bidder.append(Bidder(i, epsilon[i], T, outcome_space, num_repetitions))
    # Compute regret for winexp for T rounds (*num of repetitions)
    regret_winexp(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values)
    # Compute regret for exp3 for T rounds (*num of repetitions) after you reinitialize everything
    for i in range(0, num_bidders):
        bidder[i].pi = [bidder[i].eps for j in range(0, bidder[i].bid_space)]
        bidder[i].weights = [1 for j in range(0, bidder[i].bid_space)]
        bidder[i].utility = [[] for j in range(0,T)]
        bidder[i].exp3_regret = [0]*num_repetitions
        
    regret_exp3(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values)
