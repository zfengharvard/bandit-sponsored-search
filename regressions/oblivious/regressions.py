import numpy as np
import math
from sklearn import linear_model, decomposition, datasets
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def compute_allocation_function(bids, allocated, bid_space, eps):
    beta = 0.95
    # if you get a CTR > 0 -> your label is 1
    labels = []
    for i in range(0,len(bids)):
        if allocated[i] != 0:
            labels.append(1)
        else: 
            labels.append(0)
    if (1 in labels and 0 in labels):
        # samples that are more recent, are getting exponentially more weight
        weights = [np.power(beta, len(bids)-i-1) for i in range(0, len(bids))]
        weights_arr = np.array(weights)

        # we use as features for each bid, the 2nd and the 3rd power 
        X = [[bids[i], np.power(bids[i],2), np.power(bids[i],3)] for i in range(0,len(bids))]
        X_arr           = np.array(X)
        labels_arr      = np.array(labels)
        logistic        = linear_model.LogisticRegression(solver='lbfgs')
        logistic.fit(X_arr,labels_arr, weights_arr)

        # based on how the regression was trained (from previous bids and allocations)
        # output the updated probabilities of the discretized space
        b       = [i*eps for i in range(0,bid_space)]
        bb      = [[bi, np.power(bi,2), np.power(bi,3)] for bi in b]
        b_arr   = np.array(bb)
        output  = logistic.predict_proba(b_arr)
        one     = output[:,1]
        return (one)
    else:
        return ([0 for _ in range(0,bid_space)])



def compute_payment_function(bids, payment, bid_space,eps):
    x = np.array(bids)
    y = np.array(payment)
    X = x[:, np.newaxis]

    degree = 1
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    b = [i*eps for i in range(0,bid_space)]
    b = np.array(b)
    Bb = b[:, np.newaxis]
    
    y_plot = model.predict(Bb)
    return (y_plot)
