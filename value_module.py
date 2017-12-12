############ 
# Random Value Generator for the bidders.
# Value is sent to the bidders that can observe reward. 
############ 
 
import random
import numpy as np
import matplotlib.pyplot as plt
import patsy
import pandas as pd
import statsmodels.api as sm

def reward_gen():
    value   = np.random.uniform(0,1)
    payment = np.random.uniform(0,1)
    return (value-payment)


