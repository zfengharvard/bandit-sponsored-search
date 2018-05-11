import numpy as np
import matplotlib
import matplotlib.pyplot as plt


from collections import OrderedDict
from matplotlib.transforms import blended_transform_factory


min_num_rounds = 0
max_num_rounds = 0
num_repetitions = 0

#winexp_file1 = open("winexp_regrets.txt","r")
#exp3_file1   = open("exp3_regrets.txt","r")

#winexp_file1 = open("winexp_regrets.txt","r")
#exp3_file1   = open("exp3_regrets.txt","r")

#winexp_file1 = open("winexp_regrets.txt","r")
#exp3_file1   = open("exp3_regrets.txt","r")


with open('winexp_regrets0.00100.txt') as f:
    #w, h = [float(x) for x in next(f).split()] # read first line
    winexp_regrets_1 = []
    for line in f: # read rest of lines
        num_repetitions += 1
        winexp_regrets_1.append([float(x) for x in line.split()])
with open('winexp_regrets0.01000.txt') as f:
    #w, h = [float(x) for x in next(f).split()] # read first line
    winexp_regrets_2 = []
    for line in f: # read rest of lines
        #num_repetitions += 1
        winexp_regrets_2.append([float(x) for x in line.split()])
with open('winexp_regrets0.10000.txt') as f:
    #w, h = [float(x) for x in next(f).split()] # read first line
    winexp_regrets_3 = []
    for line in f: # read rest of lines
        #num_repetitions += 1
        winexp_regrets_3.append([float(x) for x in line.split()])

with open('exp3_regrets0.00100.txt') as f:
    #w, h = [float(x) for x in next(f).split()] # read first line
    exp3_regrets_1 = []
    for line in f: # read rest of lines
        exp3_regrets_1.append([float(x) for x in line.split()])

with open('exp3_regrets0.01000.txt') as f:
    #w, h = [float(x) for x in next(f).split()] # read first line
    exp3_regrets_2 = []
    for line in f: # read rest of lines
        exp3_regrets_2.append([float(x) for x in line.split()])

with open('exp3_regrets0.10000.txt') as f:
    #w, h = [float(x) for x in next(f).split()] # read first line
    exp3_regrets_3 = []
    for line in f: # read rest of lines
        exp3_regrets_3.append([float(x) for x in line.split()])

max_num_rounds = len(winexp_regrets_1[0])
T = max_num_rounds
rounds = [i for i in range(0,T)]

winexp_1 = []
winexp_2 = []
winexp_3 = []
for t in range(0,T): 
    winexp_1.append(sum(d[t] for d in winexp_regrets_1)/num_repetitions)
    winexp_2.append(sum(d[t] for d in winexp_regrets_2)/num_repetitions)
    winexp_3.append(sum(d[t] for d in winexp_regrets_3)/num_repetitions)
        

exp3_1 = []
exp3_2 = []
exp3_3 = []
for t in range(0,T): 
    exp3_1.append(sum(d[t] for d in exp3_regrets_1)/num_repetitions)
    exp3_2.append(sum(d[t] for d in exp3_regrets_2)/num_repetitions)
    exp3_3.append(sum(d[t] for d in exp3_regrets_3)/num_repetitions)



final_winexp_1           =  np.array([winexp_1[i] for i in range(min_num_rounds, max_num_rounds)])
winexp_arr_1              =  np.array(winexp_regrets_1) #size repetitions x T
winexp_10_percentile_1    =  [np.percentile(winexp_arr_1[:,t],10) for t in range(0,T)]
winexp_90_percentile_1    =  [np.percentile(winexp_arr_1[:,t],90) for t in range(0,T)]
final_exp3_1              =  np.array([exp3_1[i] for i in range(min_num_rounds,max_num_rounds)])
exp3_arr_1                =  np.array(exp3_regrets_1) #size repetitions x T
exp3_10_percentile_1      =  [np.percentile(exp3_arr_1[:,t],10) for t in range(0,T)]
exp3_90_percentile_1      =  [np.percentile(exp3_arr_1[:,t],90) for t in range(0,T)]


final_winexp_2           =  np.array([winexp_2[i] for i in range(min_num_rounds, max_num_rounds)])
winexp_arr_2              =  np.array(winexp_regrets_2) #size repetitions x T
winexp_10_percentile_2    =  [np.percentile(winexp_arr_2[:,t],10) for t in range(0,T)]
winexp_90_percentile_2    =  [np.percentile(winexp_arr_2[:,t],90) for t in range(0,T)]
final_exp3_2              =  np.array([exp3_2[i] for i in range(min_num_rounds,max_num_rounds)])
exp3_arr_2                =  np.array(exp3_regrets_2) #size repetitions x T
exp3_10_percentile_2      =  [np.percentile(exp3_arr_2[:,t],10) for t in range(0,T)]
exp3_90_percentile_2      =  [np.percentile(exp3_arr_2[:,t],90) for t in range(0,T)]


final_winexp_3           =  np.array([winexp_3[i] for i in range(min_num_rounds, max_num_rounds)])
winexp_arr_3              =  np.array(winexp_regrets_3) #size repetitions x T
winexp_10_percentile_3    =  [np.percentile(winexp_arr_3[:,t],10) for t in range(0,T)]
winexp_90_percentile_3    =  [np.percentile(winexp_arr_3[:,t],90) for t in range(0,T)]
final_exp3_3              =  np.array([exp3_3[i] for i in range(min_num_rounds,max_num_rounds)])
exp3_arr_3                =  np.array(exp3_regrets_3) #size repetitions x T
exp3_10_percentile_3      =  [np.percentile(exp3_arr_3[:,t],10) for t in range(0,T)]
exp3_90_percentile_3      =  [np.percentile(exp3_arr_3[:,t],90) for t in range(0,T)]



plt.style.use('ggplot')
#matplotlib.rcParams.update({'font.size': 12})
fig = plt.figure()
#fig.set_figheight(6)
#fig.set_figwidth(6)
matplotlib.rcParams.update({'font.size': 11})
fig.set_figheight(4)
fig.set_figwidth(4)


#plt.figure(1,figsize=(10,10))

#b_0.00100
epsilon = 0.001
plt.plot(rounds, final_winexp_1, '#d61111', linewidth=2, label=r'WINEXP $\epsilon =$ %.3f'%epsilon)
#plt.fill_between(rounds, winexp_10_percentile_1, winexp_90_percentile_1,facecolor='red', alpha=0.5)
plt.plot(rounds, final_exp3_1, '#52aafb', linestyle=':',linewidth=2,label=r'EXP3 $\epsilon =$ %.3f'%epsilon)
#plt.fill_between(rounds, exp3_10_percentile_1, exp3_90_percentile_1,facecolor='blue', alpha=0.5)

#epsilon = 0.01:
epsilon =0.01
plt.plot(rounds, final_winexp_2, '#f44b4b', linewidth=2,label=r'WINEXP $\epsilon =$ %.2f'%epsilon)
#plt.fill_between(rounds, winexp_10_percentile_2, winexp_90_percentile_2,facecolor='green', alpha=0.5)

plt.plot(rounds, final_exp3_2, 'b', linestyle=':',linewidth=2,label=r'EXP3 $\epsilon =$ %.2f'%epsilon)
#plt.fill_between(rounds, exp3_10_percentile_2, exp3_90_percentile_2,facecolor='cyan', alpha=0.5)

#epsilon = 0.1
epsilon = 0.1
plt.plot(rounds, final_winexp_3, 'm', linewidth=2,label='WINEXP $\epsilon =$ %.1f'%epsilon)
#plt.fill_between(rounds, winexp_10_percentile_3, winexp_90_percentile_3,facecolor='magenta', alpha=0.5)

plt.plot(rounds, final_exp3_3, 'k', linestyle=':',linewidth=2,label='EXP3 $\epsilon =$ %.1f'%epsilon)
#plt.fill_between(rounds, exp3_10_percentile_3, exp3_90_percentile_3,facecolor='magenta', alpha=0.5)


plt.legend(loc='best')
plt.axis([0,5000,0,85])
plt.xlabel('number of rounds')
plt.ylabel('regret')
plt.savefig('b_comparison_oblivious2.png')
#plt.show()
