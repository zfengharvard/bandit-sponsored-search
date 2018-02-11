[?2004h[?1049h[?1h=[?2004h[1;29r[?12;25h[?12l[?25h[27m[m[H[2J[?25l[29;1H"runner-dp.py" 73L, 2879C[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m10[m
winexp = []
exp3 = []
min_num_rounds = [31m0[m
max_num_rounds = [31m200[m
step = [31m2[m
num_auctions = [31m5[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]


[34m#initialize the bidders once for the maximum number of rounds [m
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions,num_aa[22;1Huctions)
[34m# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders[m
bids = []
tmp = []
[38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):
    tmp.append([np.random.uniform([31m0[m,[31m1[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m10[m
winexp = []
exp3 = []
min_num_rounds = [31m0[m
max_num_rounds = [31m200[m
step = [31m2[m
num_auctions = [31m5[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]


[34m#initialize the bidders once for the maximum number of rounds [m
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions,num_aa[22;1Huctions)
[34m# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders[m
bids = []
tmp = []
[38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):
    tmp.append([np.random.uniform([31m0[m,[31m1[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])
[34m# each auction in the batch for timestep t, same bids[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m10[m
winexp = []
exp3 = []
min_num_rounds = [31m0[m
max_num_rounds = [31m200[m
step = [31m2[m
num_auctions = [31m5[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]


[34m#initialize the bidders once for the maximum number of rounds [m
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions,num_aa[22;1Huctions)
[34m# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders[m
bids = []
tmp = []
[38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):
    tmp.append([np.random.uniform([31m0[m,[31m1[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])
[34m# each auction in the batch for timestep t, same bids[1;1H[?12l[?25h[27m[m[H[2J[?25l[1;1H[35mfrom[m bidder [35mimport[m *
[35mfrom[m copy [35mimport[m deepcopy
[35mfrom[m master_file [35mimport[m regret_winexp, regret_exp3
[35mfrom[m auction_parameters [35mimport[m set_auction_params
[35mimport[m matplotlib
[35mimport[m matplotlib.pyplot [38;5;130mas[m plt


num_repetitions = [31m10[m
winexp = []
exp3 = []
min_num_rounds = [31m0[m
max_num_rounds = [31m200[m
step = [31m2[m
num_auctions = [31m5[m
rounds = [T [38;5;130mfor[m T [38;5;130min[m [36mrange[m(min_num_rounds,max_num_rounds, step)]


[34m#initialize the bidders once for the maximum number of rounds [m
T = max_num_rounds
(num_bidders, num_slots, outcome_space, rank_scores, ctr, reserve, values) = set_auction_params(T,num_repetitions,num_aa[22;1Huctions)
[34m# bids of the "adversaries" are considered fixed
# bids size now: num_auctions x T x num_bidders[m
bids = []
tmp = []
[38;5;130mfor[m t [38;5;130min[m [36mrange[m([31m0[m,T):
    tmp.append([np.random.uniform([31m0[m,[31m1[m) [38;5;130mfor[m i [38;5;130min[m [36mrange[m([31m0[m,num_bidders)])
[34m# each auction in the batch for timestep t, same bids[1;1H[?12l[?25h[30;1H[?2004l[m[?2004l[?1l>[?1049lVim: Error reading input, exiting...
Vim: Finished.
[30;1H[J