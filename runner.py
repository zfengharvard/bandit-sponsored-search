from bidder import *
from copy import deepcopy
from master_file import regret_winexp, regret_exp3
from auction_parameters import set_auction_params
import matplotlib
import matplotlib.pyplot as plt


num_repetitions = 500
winexp = [] 
exp3 = []
min_num_rounds = 10
max_num_rounds = 30
step = 2
rounds = [T for T in range(min_num_rounds,max_num_rounds, step)]
for T in range(min_num_rounds, max_num_rounds,step):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions)
    # bids of the "adversaries" are considered fixed
    bids = []
    for t in range(0,T):
        bids.append([round(np.random.uniform(0,1),2) for i in range(0,num_bidders)])
        print ("Bids for timestep %d"%t)
        print bids[t]
    # Preferred Discretizations for the learner
    #epsilon = []
    #for i in range(0,num_bidders):
    #    epsilon.append(0.1)
    epsilon = 0.1

    # Create the bidders and store them in a list
    #bidder = [] #list of bidder objects
    #for i in range(0,num_bidders):
    #    bidder.append(Bidder(i, epsilon[i], T, outcome_space, num_repetitions))
    bidder = Bidder(0, epsilon, T, outcome_space, num_repetitions)
    # Compute regret for winexp for T rounds (*num of repetitions)
    cpy1 = deepcopy(bids)
    cpy2 = deepcopy(bids)
    regr = regret_winexp(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy1)
    winexp.append(regr)
    print ("WIN-EXP regr %f"%regr)
    
    # Compute regret for exp3 for T rounds (*num of repetitions) after you reinitialize everything
    #for i in range(0, num_bidders):
    #    bidder[i].pi = [bidder[i].eps for j in range(0, bidder[i].bid_space)]
    #    bidder[i].weights = [1 for j in range(0, bidder[i].bid_space)]
    #    bidder[i].utility = [[] for j in range(0,T)]
    #    bidder[i].exp3_regret = [0]*num_repetitions

    #bidder.pi = [1.0/bidder.bid_space for j in range(0, bidder.bid_space)]
    #bidder.weights = [1 for j in range(0, bidder.bid_space)]
    #bidder.utility = [[] for j in range(0,T)]
    #bidder.exp3_regret = [0]*num_repetitions
        
    #regr = regret_exp3(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy2)
    #exp3.append(regr)
    #print ("EXP3 regr %f"%regr)

    print ("List of WIN-EXP regrets")
    print (winexp)
    print ("List of EXP3 regrets")
    print (exp3)

matplotlib.rcParams.update({'font.size': 17})
fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(10)
plt.figure(1,figsize=(10,10))
plt.plot(rounds, winexp, 'ro', label = 'WIN-EXP')
#plt.plot(rounds, exp3, 'bs', label = 'EXP3')
plt.legend(loc='best')
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.title('Regret Performance of WIN-EXP vs EXP3')
#plt.savefig('winexp_vs_exp3_one_learner.png')
plt.savefig('winexp.png')
plt.show()
