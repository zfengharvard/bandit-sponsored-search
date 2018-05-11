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
step = 5
#num_auctions = 1
rounds = [T for T in range(min_num_rounds,max_num_rounds)]

#initialize the bidders once for the maximum number of rounds 
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, threshold,noise) = set_auction_params(T,num_repetitions)
# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders
bids = [] 
for t in range(0,T):
    bids.append([np.random.uniform(0,1) for i in range(0,num_bidders)])


# Preferred Discretizations for the learner
epsilon = 0.01
bidder_winexp = [Bidder(0, epsilon, T, outcome_space, num_repetitions) for _ in range(0,num_repetitions)]
bidder_exp3 = [Bidder(0, epsilon, T, outcome_space, num_repetitions) for _ in range(0,num_repetitions)]
cpy1 = deepcopy(bids)
cpy2 = deepcopy(bids)
cp3  = deepcopy(bids)
noise_cpy1 = deepcopy(noise)
noise_cpy2 = deepcopy(noise)
#winexp regret has to be returned as a list of all the regrets for all the rounds
#threshold passed as an argument is the ctr above which I get clicked
(winexp, winexp_regrets) = regret_winexp(bidder_winexp, T, num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy1, threshold,noise_cpy1)

#this has to be returned as a list of all the regrets for all the rounds 
#no need to observe threshold
(exp3, exp3_regrets) = regret_exp3(bidder_exp3,T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, cpy2,threshold,noise_cpy2)

final_winexp            =  np.array([winexp[i] for i in range(min_num_rounds, max_num_rounds)])
winexp_arr              =  np.array(winexp_regrets) #size repetitions x T
winexp_10_percentile    =  [np.percentile(winexp_arr[:,t],10) for t in range(0,T)]
winexp_90_percentile    =  [np.percentile(winexp_arr[:,t],90) for t in range(0,T)]
final_exp3              =  np.array([exp3[i] for i in range(min_num_rounds,max_num_rounds)])
exp3_arr                =  np.array(exp3_regrets) #size repetitions x T
exp3_10_percentile      =  [np.percentile(exp3_arr[:,t],10) for t in range(0,T)]
exp3_90_percentile      =  [np.percentile(exp3_arr[:,t],90) for t in range(0,T)]

matplotlib.rcParams.update({'font.size': 17})
plt.style.use('ggplot')
fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(10)
plt.figure(1,figsize=(10,10))
plt.plot(rounds, final_winexp, 'r', linewidth=2,label = 'WIN-EXP')
plt.fill_between(rounds, winexp_10_percentile, winexp_90_percentile,facecolor='#db3236', alpha=0.4)
plt.plot(rounds, final_exp3, 'b', linewidth=2,label = 'EXP3')
plt.fill_between(rounds, exp3_10_percentile, exp3_90_percentile,facecolor='#4885ed', alpha=0.4)
plt.legend(loc='best')
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.title('Regret Performance of WIN-EXP vs EXP3')
plt.savefig('oblivious_03.png')
