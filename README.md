# Learning to Bid without Knowing your Value

Code for reproducing experimental results from our paper: \<place link to paper here once all results are ready\>

### Prerequisites

* Python 2.7.13
* conda 4.4.10 

## Implementation

Folders for different simulations with oblivious adveraries, adaptive adversaries using EXP3 and adaptive adversaries using WINEXP. In order to run each simulation: 
'''
python runner-dp.py
'''
This will create 2 .txt files: winexp_regrets.txt and exp3_regrets.txt. These files hold the regrets for each repetition and each timestep and they are of size num_repetitions x T. Further, it will create a .png file, with the plot of regrets.


