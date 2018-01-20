########
# File that specifies the auction parameters to be used in each iteration. The same parameters are used subsequently by each repetition.
########


import numpy as np
import random


num_bidders         = 5
num_repetitions     = 10 #how many times each T will be repeated  
max_num_rounds      = 10
min_num_rounds      = 1
T                   = 10
num_slots           = 3
outcome_space       = 2

#rank_scores = [0.700573810327246, 0.3110979655260716, 0.610430432163001, 0.03395812562678002, 0.8345253204018921]
#ctr  = [0.97, 0.9, 0.57]
#reserve = 0.1 
#Create the rank scores (different at every t)
#TODO: here I have assumed oblivious adversary
rank_scores = [[np.random.uniform(0,1) for i in range(0,num_bidders)] for j in range(0,T)]
ctr  = [[round(np.random.uniform(0,1), 2) for i in range(0,num_slots)] for j in range(0,T)]        
for t in range(0, T):
    ctr[t].sort(reverse=True)
reserve = [round(np.random.uniform(0,0.3),2) for i in range(0,T)]
# value function for every slot
# could be seen as the conversion rate for every slot
values = [[round(np.random.uniform(0,1),2) for j in range(0,num_slots)] for j in range(0,T)]



