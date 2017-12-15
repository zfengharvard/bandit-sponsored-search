# Code for drawing an arm given the probabilities of the arms
# Gets as input the list of the probabilities for each arm
# Return the arm to be drawn
import random

def draw(probs_lst):
    t           = random.random()
    cumulative  = 0.0
    for i in range(0,len(probs_lst)):
        cumulative += probs_lst[i]
        if cumulative > t:
            return i
    return (len(probs_lst)-1)


