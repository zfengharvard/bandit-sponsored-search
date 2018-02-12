from bidder import *
from copy import deepcopy
from master_file import  regret_winexp, regret_exp3
from auction_parameters import set_auction_params
import matplotlib
import matplotlib.pyplot as plt


num_repetitions = 5
winexp = [] 
exp3 = []
min_num_rounds = 0
max_num_rounds = 1000
step = 10
num_auctions = 5
num_adaptive = 3
rounds = [T for T in range(min_num_rounds,max_num_rounds, step)]

#initialize the bidders once for the maximum number of rounds 
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions,num_auctions)
# bids of the "adversaries" are considered fixed
# bids size now: T x num_bidders
bids = [] 
for t in range(0,T):
    bids.append([np.random.uniform(0,1) for i in range(0,num_bidders)])

# Preferred Discretizations for the learner
epsilon = 0.01


final_winexp = [[] for _ in range(0,3)]
final_exp3   = [[] for _ in range(0,3)]
eps_list = [0.0001, 0.001, 0.01]
for epsilon in eps_list:
    # bidder with id == 0 is our learner, everybody else is an adversary
    bidder = [Bidder(i, epsilon, T, outcome_space, num_repetitions, num_auctions) for i in range(0,num_adaptive)]

    #winexp regret has to be returned as a list of all the regrets for all the rounds
    winexp = regret_winexp(bidder, T, num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, num_auctions, bids,num_adaptive)

    # for each bidder, re-initialize everything
    for i in range(0,num_adaptive):
        bidder[i].pi               = [1.0/bidder[i].bid_space for j in range(0, bidder[i].bid_space)]
        bidder[i].weights          = [1 for j in range(0, bidder[i].bid_space)]
        bidder[i].exp3_regret      = [0]*num_repetitions
        bidder[i].utility          = [[[] for _ in range(0, T)] for _ in range(0,num_auctions)]
        bidder[i].avg_reward       = [[] for _ in range(0,T)]
        bidder[i].avg_utility      = [[] for _ in range(0,T)]
        bidder[i].loss             = [0 for _ in range(0,bidder[i].bid_space)]
        bidder[i].alloc_func       = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
        bidder[i].pay_func         = [[] for t in range(0,T)]
        bidder[i].reward_func      = [[[] for t in range(0,T)]  for _ in range(0,num_auctions)]

    #this has to be returned as a list of all the regrets for all the rounds 
    exp3 = regret_exp3(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, num_auctions,bids,num_adaptive)

    final_winexp[eps_list.index(epsilon)]= [winexp[i] for i in range(min_num_rounds, max_num_rounds, step)]
    final_exp3[eps_list.index(epsilon)] = [exp3[i] for i in range(min_num_rounds,max_num_rounds,step)]

#print ("final_ex3")
#print final_exp3

matplotlib.rcParams.update({'font.size': 17})
fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(10)
plt.figure(1,figsize=(10,10))
for epsilon in eps_list:
    if (epsilon == 0.01):
        plt.plot(rounds, final_winexp[eps_list.index(epsilon)], 'ro')
        plt.plot(rounds, final_winexp[eps_list.index(epsilon)], '-r', label='WINEXP epsilon = %.5f'%epsilon)
   
        plt.plot(rounds, final_exp3[eps_list.index(epsilon)], 'bo')
        plt.plot(rounds, final_exp3[eps_list.index(epsilon)], '-b', label='EXP3 epsilon = %.5f'%epsilon)
    elif (epsilon == 0.055):
        plt.plot(rounds, final_winexp[eps_list.index(epsilon)], 'go')
        plt.plot(rounds, final_winexp[eps_list.index(epsilon)], '-g', label='WINEXP epsilon = %.5f'%epsilon)
   
        plt.plot(rounds, final_exp3[eps_list.index(epsilon)], 'co')
        plt.plot(rounds, final_exp3[eps_list.index(epsilon)], '-c', label='EXP3 epsilon = %.5f'%epsilon)
    else:
        plt.plot(rounds, final_winexp[eps_list.index(epsilon)], 'mo')
        plt.plot(rounds, final_winexp[eps_list.index(epsilon)], '-m', label='WINEXP epsilon = %.5f'%epsilon)
   
        plt.plot(rounds, final_exp3[eps_list.index(epsilon)], 'yo')
        plt.plot(rounds, final_exp3[eps_list.index(epsilon)], '-y', label='EXP3 epsilon = %.5f'%epsilon)
plt.legend(loc='best')
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.title('Regret Performance of WIN-EXP vs EXP3 wrt bid_space')
plt.savefig('self_play.png')
#plt.savefig('exp3.png')
plt.show()
