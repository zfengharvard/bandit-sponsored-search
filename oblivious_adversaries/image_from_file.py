# Create custom plots from the .txt files of the simulated data

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


min_num_rounds = 0
max_num_rounds = 0
num_repetitions = 0

winexp_file = open("winexp_regrets.txt","r")
exp3_file   = open("exp3_regrets.txt","r")

with open('winexp_regrets.txt') as f:
    winexp_regrets = []
    for line in f: 
        num_repetitions += 1
        winexp_regrets.append([float(x) for x in line.split()])

with open('exp3_regrets.txt') as f:
    exp3_regrets = []
    for line in f: 
        exp3_regrets.append([float(x) for x in line.split()])

max_num_rounds = len(winexp_regrets[0])
T = max_num_rounds
rounds = [i for i in range(0,T)]

winexp = []
for t in range(0,T): 
    winexp.append(sum(d[t] for d in winexp_regrets)/num_repetitions)
        

exp3 = []
for t in range(0,T): 
    exp3.append(sum(d[t] for d in exp3_regrets)/num_repetitions)





final_winexp            =  np.array([winexp[i] for i in range(min_num_rounds, max_num_rounds)])
winexp_arr              =  np.array(winexp_regrets) #size repetitions x T
winexp_10_percentile    =  [np.percentile(winexp_arr[:,t],10) for t in range(0,T)]
winexp_90_percentile    =  [np.percentile(winexp_arr[:,t],90) for t in range(0,T)]
final_exp3              =  np.array([exp3[i] for i in range(min_num_rounds,max_num_rounds)])
exp3_arr                =  np.array(exp3_regrets) #size repetitions x T
exp3_10_percentile      =  [np.percentile(exp3_arr[:,t],10) for t in range(0,T)]
exp3_90_percentile      =  [np.percentile(exp3_arr[:,t],90) for t in range(0,T)]

plt.style.use('ggplot')
matplotlib.rcParams.update({'font.size': 12})
fig = plt.figure()
fig.set_figheight(4.5)
fig.set_figwidth(4.5)
plt.plot(rounds, final_winexp, 'r', linewidth=2,label = 'WIN-EXP')
plt.fill_between(rounds, winexp_10_percentile, winexp_90_percentile,facecolor='#db3236', alpha=0.4)
plt.plot(rounds, final_exp3, 'b', linewidth=2,label = 'EXP3')
plt.fill_between(rounds, exp3_10_percentile, exp3_90_percentile,facecolor='#4885ed', alpha=0.4)
plt.legend(loc='best')
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.axis([0,5000,0,65])
plt.savefig('oblivious.png')
