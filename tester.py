[?2004h[?1049h[?1h=[?2004h[1;33r[?12;25h[?12l[?25h[27m[m[H[2J[?25l[33;1H"runner.py" 65L, 2628C[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m50[m
winexp = []
exp3 = []
min_num_rounds = [31m10[m
max_num_rounds = [31m100[m
step = [31m10[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]
[38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds, max_num_rounds,step):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions)
    [34m# bids of the "adversaries" are considered fixed[m
    bids = []
    [38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):[21;9Hbids.append([[36mround[m(np.random.uniform([31m0[m,[31m1[m),[31m2[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])[22;9H[36mprint[m ([31m"Bids for timestep %d"[m%t)[23;9H[36mprint[m bids[t]
    [34m# Preferred Discretizations for the learner
[m    [34m#epsilon = []
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    epsilon.append(0.1)[m
    epsilon = [31m0.1[m[30;5H[34m# Create the bidders and store them in a list
[m    [34m#bidder = [] #list of bidder objects
[m    [34m#for i in range(0,num_bidders):[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m50[m
winexp = []
exp3 = []
min_num_rounds = [31m10[m
max_num_rounds = [31m100[m
step = [31m10[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]
[38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds, max_num_rounds,step):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions)
    [34m# bids of the "adversaries" are considered fixed[m
    bids = []
    [38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):[21;9Hbids.append([[36mround[m(np.random.uniform([31m0[m,[31m1[m),[31m2[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])[22;9H[36mprint[m ([31m"Bids for timestep %d"[m%t)[23;9H[36mprint[m bids[t]
    [34m# Preferred Discretizations for the learner
[m    [34m#epsilon = []
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    epsilon.append(0.1)[m
    epsilon = [31m0.1[m[30;5H[34m# Create the bidders and store them in a list
[m    [34m#bidder = [] #list of bidder objects
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    bidder.append(Bidder(i, epsilon[i], T, outcome_space, num_repetitions))[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m50[m
winexp = []
exp3 = []
min_num_rounds = [31m10[m
max_num_rounds = [31m100[m
step = [31m10[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]
[38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds, max_num_rounds,step):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions)
    [34m# bids of the "adversaries" are considered fixed[m
    bids = []
    [38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):[21;9Hbids.append([[36mround[m(np.random.uniform([31m0[m,[31m1[m),[31m2[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])[22;9H[36mprint[m ([31m"Bids for timestep %d"[m%t)[23;9H[36mprint[m bids[t]
    [34m# Preferred Discretizations for the learner
[m    [34m#epsilon = []
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    epsilon.append(0.1)[m
    epsilon = [31m0.1[m[30;5H[34m# Create the bidders and store them in a list
[m    [34m#bidder = [] #list of bidder objects
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    bidder.append(Bidder(i, epsilon[i], T, outcome_space, num_repetitions))[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m50[m
winexp = []
exp3 = []
min_num_rounds = [31m10[m
max_num_rounds = [31m100[m
step = [31m10[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]
[38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds, max_num_rounds,step):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions)
    [34m# bids of the "adversaries" are considered fixed[m
    bids = []
    [38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):[21;9Hbids.append([[36mround[m(np.random.uniform([31m0[m,[31m1[m),[31m2[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])[22;9H[36mprint[m ([31m"Bids for timestep %d"[m%t)[23;9H[36mprint[m bids[t]
    [34m# Preferred Discretizations for the learner
[m    [34m#epsilon = []
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    epsilon.append(0.1)[m
    epsilon = [31m0.1[m[30;5H[34m# Create the bidders and store them in a list
[m    [34m#bidder = [] #list of bidder objects
[m    [34m#for i in range(0,num_bidders):[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m50[m
winexp = []
exp3 = []
min_num_rounds = [31m10[m
max_num_rounds = [31m100[m
step = [31m10[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]
[38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds, max_num_rounds,step):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions)
    [34m# bids of the "adversaries" are considered fixed[m
    bids = []
    [38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):[21;9Hbids.append([[36mround[m(np.random.uniform([31m0[m,[31m1[m),[31m2[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])[22;9H[36mprint[m ([31m"Bids for timestep %d"[m%t)[23;9H[36mprint[m bids[t]
    [34m# Preferred Discretizations for the learner
[m    [34m#epsilon = []
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    epsilon.append(0.1)[m
    epsilon = [31m0.1[m[30;5H[34m# Create the bidders and store them in a list
[m    [34m#bidder = [] #list of bidder objects
[m    [34m#for i in range(0,num_bidders):[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m50[m
winexp = []
exp3 = []
min_num_rounds = [31m10[m
max_num_rounds = [31m100[m
step = [31m10[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]
[38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds, max_num_rounds,step):
    (num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_ree[18;1Hpetitions)
    [34m# bids of the "adversaries" are considered fixed[m
    bids = []
    [38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):[22;9Hbids.append([[36mround[m(np.random.uniform([31m0[m,[31m1[m),[31m2[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])[23;9H[36mprint[m ([31m"Bids for timestep %d"[m%t)[24;9H[36mprint[m bids[t]
    [34m# Preferred Discretizations for the learner
[m    [34m#epsilon = []
[m    [34m#for i in range(0,num_bidders):
[m    [34m#    epsilon.append(0.1)[m
    epsilon = [31m0.1[1;1H[?12l[?25h[30;1H[?2004l[m[?2004l[?1l>[?1049lVim: Error reading input, exiting...
Vim: Finished.
[30;1H[J