from bidder import *
from copy import deepcopy
from master_file import  regret_winexp, regret_exp3, regret_gexp3
from auction_parameters import set_auction_params
import matplotlib
import matplotlib.pyplot as plt


num_repetitions = 5
winexp = [] 
exp3 = []
min_num_rounds = 0
max_num_rounds = 400
step = 1
num_auctions = 3
rounds = [T for T in range(min_num_rounds,max_num_rounds, step)]
matplotlib.rcParams.update({'font.size': 17})
fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(10)
plt.figure(1,figsize=(10,10))

#initialize the bidders once for the maximum number of rounds 
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions,num_auctions)
# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders
bids = [] 
bids_per_timestep = []
for t in range(0,T):
    bids_per_timestep.append([np.random.uniform(0,1) for i in range(0,num_bidders)])

for auction in range(0,num_auctions):
    auction_bids = [bids_per_timestep[t] for t in range(0,T)]
    bids.append(auction_bids)


eps_list = [0.0001, 0.001, 0.01]
for epsilon in eps_list:
    # Preferred Discretizations for the learner
    bidder = Bidder(0, epsilon, T, outcome_space, num_repetitions, num_auctions)
    cpy1 = deepcopy(bids)
    cpy2 = deepcopy(bids)
    #cp3  = deepcopy(bids)
    
    (winexp, winexp_regrets) = regret_winexp(bidder, T, num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy1, num_auctions)

    bidder.pi               = [1.0/bidder.bid_space for j in range(0, bidder.bid_space)]
    bidder.weights          = [1 for j in range(0, bidder.bid_space)]
    bidder.exp3_regret      = [0]*num_repetitions
    bidder.utility          = [[[] for i in range(0, T)] for _ in range(0,num_auctions)]
    bidder.avg_reward       = [[] for _ in range(0,T)]
    bidder.avg_utility      = [[] for _ in range(0,T)]
    bidder.loss             = [0 for i in range(0,bidder.bid_space)]
    bidder.alloc_func       = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
    bidder.pay_func         = [[] for t in range(0,T)]
    bidder.reward_func      = [[[] for t in range(0,T)]  for _ in range(0,num_auctions)]


    (exp3, exp3_regrets) = regret_exp3(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy2,num_auctions)

    #bidder.pi               = [1.0/bidder.bid_space for j in range(0, bidder.bid_space)]
    #bidder.weights          = [1 for j in range(0, bidder.bid_space)]
    #bidder.gexp3_regret     = [0]*num_repetitions
    #bidder.utility          = [[[] for i in range(0, T)] for _ in range(0,num_auctions)]
    #bidder.avg_reward       = [[] for _ in range(0,T)]
    #bidder.avg_utility      = [[] for _ in range(0,T)]
    #bidder.loss             = [0 for i in range(0,bidder.bid_space)]
    #bidder.alloc_func       = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
    #bidder.pay_func         = [[] for t in range(0,T)]
    #bidder.reward_func      = [[[] for t in range(0,T)]  for _ in range(0,num_auctions)]

    #gexp3 = regret_gexp3(bidder,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy2,num_auctions)

    final_winexp            =  np.array([winexp[i] for i in range(min_num_rounds, max_num_rounds)])
    winexp_arr              =  np.array(winexp_regrets) #size repetitions x T
    winexp_10_percentile    =  [np.percentile(winexp_arr[:,t],10) for t in range(0,T)]
    winexp_90_percentile    =  [np.percentile(winexp_arr[:,t],90) for t in range(0,T)]
    final_exp3              =  np.array([exp3[i] for i in range(min_num_rounds,max_num_rounds)])
    exp3_arr                =  np.array(exp3_regrets) #size repetitions x T
    exp3_10_percentile      =  [np.percentile(exp3_arr[:,t],10) for t in range(0,T)]
    exp3_90_percentile      =  [np.percentile(exp3_arr[:,t],90) for t in range(0,T)]
    if (epsilon == 0.01):
        plt.plot(rounds, final_winexp, '-r', label='WINEXP epsilon = %.5f'%epsilon)
        plt.fill_between(rounds, winexp_10_percentile, winexp_90_percentile,facecolor='red', alpha=0.5)
        plt.plot(rounds, final_exp3, '-b', label='EXP3 epsilon = %.5f'%epsilon)
        plt.fill_between(rounds, exp3_10_percentile, exp3_90_percentile,facecolor='blue', alpha=0.5)
    elif (epsilon == 0.055):
        plt.plot(rounds, final_winexp, '-g', label='WINEXP epsilon = %.5f'%epsilon)
        plt.fill_between(rounds, winexp_10_percentile, winexp_90_percentile,facecolor='green', alpha=0.5)
   
        plt.plot(rounds, final_exp3, '-c', label='EXP3 epsilon = %.5f'%epsilon)
        plt.fill_between(rounds, exp3_10_percentile, exp3_90_percentile,facecolor='cyan', alpha=0.5)
    else:
        plt.plot(rounds, final_winexp, '-m', label='WINEXP epsilon = %.5f'%epsilon)
        plt.fill_between(rounds, winexp_10_percentile, winexp_90_percentile,facecolor='magenta', alpha=0.5)
   
        plt.plot(rounds, final_exp3, '-y', label='EXP3 epsilon = %.5f'%epsilon)
        plt.fill_between(rounds, exp3_10_percentile, exp3_90_percentile,facecolor='magenta', alpha=0.5)


plt.legend(loc='best')
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.title('Regret Performance of WIN-EXP vs EXP3 wrt bid space')
plt.savefig('b_comparison.png')
plt.show()
