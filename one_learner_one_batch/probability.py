# Code for drawing an arm given the probabilities of the arms
# Gets as input the list of the probabilities for each arm
# Return the arm to be drawn
import random
import numpy as np

def draw(probs_lst):
    t           = np.random.uniform(0,1)
    cumulative  = 0.0
    for i in range(0,len(probs_lst)):
        cumulative += probs_lst[i]
        if cumulative > t:
            return i
    return (len(probs_lst)-1)



# Implementation of gamma-EXP3 altered from: https://github.com/j2kun/exp3/blob/master/probability.py
# Makes a distribution out of a list of floats
def draw_gexp3(weights):
    choice = random.uniform(0, sum(weights))
    choiceIndex = 0

    for weight in weights:
        choice -= weight
        if choice <= 0:
            return choiceIndex

        choiceIndex += 1
    return (len(weights)-1)

def distr(weights, gamma=0.0):
    theSum = float(sum(weights))
    return tuple((1.0 - gamma) * (w / theSum) + (gamma / len(weights)) for w in weights)

def mean(aList):
   theSum = 0
   count = 0

   for x in aList:
      theSum += x
      count += 1

   return 0 if count == 0 else theSum / count

