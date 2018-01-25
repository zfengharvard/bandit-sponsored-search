from bidder import *
from master_file import regret_winexp, regret_exp3
from auction_parameters import set_auction_params
import matplotlib
import matplotlib.pyplot as plt


num_repetitions = 10
winexp = [] 
exp3 = []
min_num_rounds = 1000
max_num_rounds = 2000
rounds = [T for T in range(min_num_rounds,max_num_rounds)]
for T in range(min_num_rounds, max_num_rounds):
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
    winexp.append(regret_winexp(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values))
    # Compute regret for exp3 for T rounds (*num of repetitions) after you reinitialize everything
    for i in range(0, num_bidders):
        bidder[i].pi = [bidder[i].eps for j in range(0, bidder[i].bid_space)]
        bidder[i].weights = [1 for j in range(0, bidder[i].bid_space)]
        bidder[i].utility = [[] for j in range(0,T)]
        bidder[i].exp3_regret = [0]*num_repetitions
        
    exp3.append(regret_exp3(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values))


matplotlib.rcParams.update({'font.size': 17})
fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(10)
plt.figure(1,figsize=(10,10))
plt.plot(rounds, winexp, 'ro', label = 'WIN-EXP')
plt.plot(rounds, exp3, 'bs', label = 'EXP3')
plt.legend(loc='best')
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.title('Regret Performance of WIN-EXP vs EXP3')
plt.savefig('winexp_vs_exp3.png')
plt.show()
