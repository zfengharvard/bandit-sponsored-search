from bidder import *
from copy import deepcopy
from master_file import regret_winexp, regret_exp3
from auction_parameters import set_auction_params
import matplotlib
import matplotlib.pyplot as plt


num_repetitions = 50
winexp = [] 
exp3 = []
min_num_rounds = 0
max_num_rounds = 1000
step = 5
num_auctions = 10
rounds = [T for T in range(min_num_rounds,max_num_rounds, step)]


#initialize the bidders once for the maximum number of rounds 
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions,num_auctions)
# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders
bids = [] 
for auction in range(0,num_auctions):
    tmp = []
    for t in range(0,T):
        tmp.append([np.random.uniform(0,1) for i in range(0,num_bidders)])
    bids.append(tmp)

#print ("Bids initially")
#print bids


# Preferred Discretizations for the learner
epsilon = 0.01
bidder = Bidder(0, epsilon, T, outcome_space, num_repetitions,num_auctions)
cpy1 = deepcopy(bids)
cpy2 = deepcopy(bids)
#winexp regret has to be returned as a list of all the regrets for all the rounds
winexp = regret_winexp(bidder, T, num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy1, num_auctions)

bidder.pi               = [1.0/bidder.bid_space for j in range(0, bidder.bid_space)]
bidder.weights          = [1 for j in range(0, bidder.bid_space)]
bidder.exp3_regret      = [0]*num_repetitions
bidder.utility          = [[[] for i in range(0, T)] for _ in range(0,num_auctions)]
bidder.avg_utility      = [[] for i in range(0,T)]
bidder.avg_reward       = [[] for i in range(0,T)]
bidder.loss             = [0 for i in range(0,bidder.bid_space)]
bidder.alloc_func       = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
bidder.pay_func         = [[] for t in range(0,T)]
bidder.reward_func      = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]

#this has to be returned as a list of all the regrets for all the rounds 
exp3 = regret_exp3(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy2, num_auctions)

final_winexp = [winexp[i] for i in range(min_num_rounds, max_num_rounds, step)]
final_exp3 = [exp3[i] for i in range(min_num_rounds,max_num_rounds,step)]

matplotlib.rcParams.update({'font.size': 17})
fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(10)
plt.figure(1,figsize=(10,10))
plt.plot(rounds, final_winexp, 'ro', label = 'WIN-EXP')
plt.plot(rounds,final_winexp, 'r-')
plt.plot(rounds, final_exp3, 'bs', label = 'EXP3')
plt.plot(rounds,final_exp3, 'b-')
plt.legend(loc='best')
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.title('Regret Performance of WIN-EXP vs EXP3')
plt.savefig('winexp_vs_exp3_one_learner.png')
#plt.savefig('exp3.png')
#plt.show()
