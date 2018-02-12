import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
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
    weights = [math.pow(beta, len(bids)-i-1) for i in range(0, len(bids))]
    weights_arr = np.array(weights)

    # now for each bid, we have a label
    X = [[bids[i], math.pow(bids[i],2), math.pow(bids[i],3)] for i in range(0,len(bids))]
    X_arr        = np.array(X)
    labels_arr      = np.array(labels)
    logistic = linear_model.LogisticRegression()
    logistic.fit(X_arr,labels_arr, weights_arr)

    b = [i*eps for i in range(0,bid_space)]
    bb = [[bi, math.pow(bi,2), math.pow(bi,3)] for bi in b]
    b_arr = np.array(bb)
    output = logistic.predict_proba(b_arr)
    one = output[:,1]

    matplotlib.rcParams.update({'font.size': 17})
    fig = plt.figure()
    fig.set_figheight(10)
    fig.set_figwidth(10)
    plt.figure(1,figsize=(10,10))
    plt.plot(b,one, 'ro')
    plt.show()




def compute_payment_function(bids, payment, bid_space,eps):
    x = np.array(bids)
    y = np.array(payment)
    X = x[:, np.newaxis]
    #X_plot = x_plot[:, np.newaxis]

    plt.scatter(x, y, color='blue', s=30, marker='o', label="training points")

    degree = 1
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    b = [i*eps for i in range(0,bid_space)]
    b = np.array(b)
    Bb = b[:, np.newaxis]
    
    y_plot = model.predict(Bb)
    plt.plot(Bb, y_plot, color='red', linewidth=2, label="degree %d" % degree)

    plt.legend(loc='lower left')
    plt.show()
