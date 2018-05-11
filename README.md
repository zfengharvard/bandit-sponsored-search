# Learning to Bid without Knowing your Value

Code for reproducing experimental results from our paper: \<place link to paper here once all results are ready\>

### Prerequisites

* Python 2.7.13
* conda 4.4.10 
* RStudio (if you want to run the plotters)

## Implementation

Folders for different simulations with oblivious adveraries, adaptive adversaries using EXP3 and adaptive adversaries using WINEXP. In order to run each simulation: 
```
python runner-dp.py
```
This will create 2 .txt files: winexp_regrets.txt and exp3_regrets.txt. These files hold the regrets for each repetition and each timestep and they are of size num_repetitions x T. Further, it will create a .png file, with the plot of regrets.

For the folders that create the graphs for different discretizations there is a separate .txt file for each algorithm (winexp and exp3) and each discretization (0.001, 0.01, 0.1). 

We also include .R files that extract the graphs along with the final .png that appear in our paper.
