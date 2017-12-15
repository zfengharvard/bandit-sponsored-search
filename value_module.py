############ 
# Random Value Generator for the bidders.
# Value is sent to the bidders that can observe reward. 
############ 
 
import random
import numpy as np

def reward_gen():
    value   = np.random.uniform(0,1)
    payment = np.random.uniform(0,1)
    return (value-payment)


