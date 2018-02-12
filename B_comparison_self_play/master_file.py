import numpy as np
import random
import math
import matplotlib.pyplot as plt
import matplotlib
from copy import deepcopy
from runner_winexp_all_bidders import *
from runner_exp3_all_bidders import *


def regret_winexp(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values, num_auctions,bids,num_adaptive):
    f1 = "winexp_regrets.txt"
    winexp_regrets = open(f1, "w")
    winexp_regrets.write("eps=%.5f\n"%bidder[0].eps)
    #winexp_regr is now a num_repetitionsxT matrix
    winexp_regr  = []
    bids_inside  = [[] for _ in range(0,num_repetitions)]
    print ("WINEXP")
    for rep in range(0, num_repetitions):
        print ("Repetition = %d"%rep)
        #   at each repetition, a whole array of size T is returned: 
        #    This corresponds to the regrets for bidder 0 at each one of the T rounds
        
        (returned_regret, returned_bids) = main_winexp(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,num_auctions,bids,num_adaptive)
        winexp_regr.append(returned_regret)
        bids_inside[rep] = returned_bids
        #print ("Current Regrets")
        #print winexp_regr[rep]
        for i in range(0,num_adaptive):
            bidder[i].pi             = [1.0/bidder[i].bid_space for j in range(0,bidder[i].bid_space)]
            bidder[i].weights        = [1 for j in range(0,bidder[i].bid_space)]
            bidder[i].utility        = [[[] for _ in range(0, T)] for _ in range(0,num_auctions)]
            bidder[i].avg_utility    = [[] for _ in range(0,T)]
            bidder[i].avg_reward     = [[] for _ in range(0,T)]
            bidder[i].alloc_func     = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
            bidder[i].pay_func       = [[] for t in range(0,T)]
            bidder[i].reward_func    = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
        
    #print ("size of winexp list")
    #print len(winexp_regr)

 
    winexp_expected_regr = []
    for t in range(0,T):
        winexp_expected_regr.append(sum(d[t] for d in winexp_regr)/num_repetitions)

    #winexp_expected_bids = [ [0 for _ in range(0,T)] for _ in range(0,num_bidders)]
    winexp_expected_bids = [ [0 for _ in range(0,T)] for _ in range(0,num_adaptive)]
    #for i in range(0, num_bidders):
    for i in range(0, num_adaptive):
        for t in range(0,T):
            s_b = 0
            for rep in range(0, num_repetitions):
                s_b += bids_inside[rep][t][i]
            winexp_expected_bids[i][t] = s_b/num_repetitions
        

    for r in range(0,num_repetitions):
        s = ""
        for t in range(0,T):
            s += ("%.5f "%winexp_regr[r][t])
        s += "\n"
        winexp_regrets.write(s) 
    

    #print winexp_expected_bids
    #final_winexp_regr = [winexp_expected_regr[t]/t for t in range(1,T-1)]
    bidders      = [i for i in range(0, num_adaptive)]
    rounds       = [t for t in range(0,T,10)]
    plotted_bids = [[winexp_expected_bids[i][t] for t in range(0,T,10)] for i in range(0,num_adaptive)]
    final_winexp_regr = winexp_expected_regr
    matplotlib.rcParams.update({'font.size': 17})
    fig1 = plt.figure()
    fig1.set_figheight(10)
    fig1.set_figwidth(10)

    num_plots = num_adaptive

    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)])

    labels = []
    for i in range(0, num_plots):
        if i == 0:
            plt.plot(rounds, plotted_bids[i], 'ro')
            plt.plot(rounds, plotted_bids[i], 'r-')
        elif i == 1:
            plt.plot(rounds, plotted_bids[i], 'go')
            plt.plot(rounds, plotted_bids[i], 'g-')
            labels.append(r'Bidder %d'%i)
        else: 
            plt.plot(rounds, plotted_bids[i], 'bo')
            plt.plot(rounds, plotted_bids[i], 'b-')
            labels.append(r'Bidder %d'%i)

    plt.legend(labels, ncol=4, loc='upper center', 
               bbox_to_anchor=[0.5, 1.1], 
               columnspacing=1.0, labelspacing=0.0,
               handletextpad=0.0, handlelength=1.5,
               fancybox=True, shadow=True)

    #plt.plot(rounds, final_winexp, 'ro', label = 'WIN-EXP')
    #plt.plot(rounds,final_winexp, 'r-')
    #plt.plot(rounds, final_exp3, 'bs', label = 'EXP3')
    #plt.plot(rounds,final_exp3, 'b-')
    #plt.legend(loc='best')
    plt.xlabel('number of rounds')
    plt.ylabel('bids')
    plt.title('WINEXP Bids over time eps=%.5f'%bidder[0].eps)
    plt.savefig('bids_winexp.png')
    winexp_regrets.close()
    return final_winexp_regr 


def regret_exp3(bidder, T,num_repetitions, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,num_auctions,bids,num_adaptive):
    f2 = "exp3_regrets.txt"
    exp3_regrets = open(f2,"w")
    epx3_regrets.write("eps=%.5f\n"%bidder[0].eps)
    #exp3_regr is now a num_repetitionsxT matrix
    exp3_regr   = []
    bids_inside = [[] for _ in range(0,num_repetitions)]
    print ("EXP3")
    for rep in range(0, num_repetitions):
        print ("Repetition rep %d for exp3"%rep)
        # at each repetition, a whole array of size T is returned: This corresponds to the regrets at each one of the T rounds
        (returned_regret, returned_bids) = main_exp3(bidder,rep, T, num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values,num_auctions,bids,num_adaptive)
        exp3_regr.append(returned_regret)
        bids_inside[rep]=returned_bids
        #print ("Current Regrets")
        #print exp3_regr
        for i in range(0,num_adaptive):
            bidder[i].loss           = [0 for j in range(0,bidder[i].bid_space)]
            bidder[i].pi             = [1.0/bidder[i].bid_space for j in range(0,bidder[i].bid_space)]
            bidder[i].weights        = [1 for j in range(0,bidder[i].bid_space)]
            bidder[i].avg_utility    = [[] for _ in range(0, T)]
            bidder[i].avg_reward     = [[] for _ in range(0, T)]
            bidder[i].alloc_func     = [[[] for t in range(0,T)] for _ in range(0,num_auctions)] 
            bidder[i].pay_func       = [[] for t in range(0,T)]
            bidder[i].reward_func    = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
            bidder[i].utility        = [[[] for t in range(0,T)] for _ in range(0,num_auctions)]
 

        
    # below, we compute the cumulative regret for the number of repetitions we ran rounds 0->T
    exp3_expected_regr = []
    for t in range(0,T):
        exp3_expected_regr.append(sum(d[t] for d in exp3_regr)/num_repetitions)
    
    for r in range(0,num_repetitions):
        s = ""
        for t in range(0,T):
            s += ("%.5f "%exp3_regr[r][t])
        s += "\n"
        exp3_regrets.write(s) 

    #exp3_expected_bids = [ [0 for _ in range(0,T)] for _ in range(0,num_bidders)]
    exp3_expected_bids = [ [0 for _ in range(0,T)] for _ in range(0,num_adaptive)]
    #for i in range(0, num_bidders):
    for i in range(0, num_adaptive):
        for t in range(0,T):
            s_b = 0
            for rep in range(0, num_repetitions):
                s_b += bids_inside[rep][t][i]
            exp3_expected_bids[i][t] = s_b/num_repetitions
    
    #print exp3_expected_bids
    bidders      = [i for i in range(0, num_adaptive)]
    rounds       = [t for t in range(0,T,10)]
    plotted_bids = [[exp3_expected_bids[i][t] for t in range(0,T,10)] for i in range(0,num_adaptive)]
    #print ("Inside master_file.py")
    #print ("Expected regret (div by num_repetitions)")
    final_exp3_regr = exp3_expected_regr
    #print final_exp3_regr
    matplotlib.rcParams.update({'font.size': 17})
    fig2 = plt.figure()
    fig2.set_figheight(10)
    fig2.set_figwidth(10)


    num_plots = num_adaptive

    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)])

    labels = []
    for i in range(0, num_plots):
        if i == 0:
            plt.plot(rounds, plotted_bids[i], 'ro')
            plt.plot(rounds, plotted_bids[i], 'r-')
        elif i == 1:
            plt.plot(rounds, plotted_bids[i], 'go')
            plt.plot(rounds, plotted_bids[i], 'g-')
            labels.append(r'Bidder %d'%i)
        else: 
            plt.plot(rounds, plotted_bids[i], 'bo')
            plt.plot(rounds, plotted_bids[i], 'b-')
            labels.append(r'Bidder %d'%i)

    plt.legend(labels, ncol=4, loc='upper center', 
               bbox_to_anchor=[0.5, 1.1], 
               columnspacing=1.0, labelspacing=0.0,
               handletextpad=0.0, handlelength=1.5,
               fancybox=True, shadow=True)

    #plt.plot(rounds, final_winexp, 'ro', label = 'WIN-EXP')
    #plt.plot(rounds,final_winexp, 'r-')
    #plt.plot(rounds, final_exp3, 'bs', label = 'EXP3')
    #plt.plot(rounds,final_exp3, 'b-')
    #plt.legend(loc='best')
    plt.xlabel('number of rounds')
    plt.ylabel('bids')
    plt.title('EXP3 Bids over time eps=%.5f'%bidder[0].eps)
    plt.savefig('bids_exp3.png')
    exp3_regrets.close()
    return (final_exp3_regr)
