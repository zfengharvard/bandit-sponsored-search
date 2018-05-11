from bidder import *
from copy import deepcopy
from master_file import  regret_winexp, regret_exp3
from auction_parameters import set_auction_params
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.switch_backend('agg')

num_repetitions = 30
winexp = [] 
exp3 = []
min_num_rounds = 0
max_num_rounds = 5000
step = 1
rounds = [T for T in range(min_num_rounds,max_num_rounds, step)]
matplotlib.rcParams.update({'font.size': 17})
fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(10)
plt.figure(1,figsize=(10,10))

#initialize the bidders once for the maximum number of rounds 
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,threshold,noise) = set_auction_params(T,num_repetitions)
# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders
bids = [] 
for t in range(0,T):
    bids.append([np.random.uniform(0,1) for i in range(0,num_bidders)])


eps_list = [0.001, 0.01, 0.1]
for epsilon in eps_list:
    bidder_winexp = [Bidder(0, epsilon, T, outcome_space, num_repetitions) for _ in range(0,num_repetitions)]
    bidder_exp3   = [Bidder(0, epsilon, T, outcome_space, num_repetitions) for _ in range(0,num_repetitions)]


    # Preferred Discretizations for the learner
    cpy1 = deepcopy(bids)
    cpy2 = deepcopy(bids)
    
    (winexp, winexp_regrets) = regret_winexp(bidder_winexp, T, num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy1, threshold,noise)



    (exp3, exp3_regrets) = regret_exp3(bidder_exp3,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy2,threshold, noise)


