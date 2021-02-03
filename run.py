import numpy as np
from matplotlib import pyplot as plt
from model import Model,SA
from flex import flexOrder,Kernel,getRandomKernel
import matplotlib.patches as patches
from math import log,ceil
from copy import deepcopy




def plot(model,nrange=(0,9),delta=1):

    x = np.arange(nrange[0], nrange[1], delta)
    y = np.arange(nrange[0], nrange[1], delta)
    X, Y = np.meshgrid(x, y)
    X = X.ravel()
    Y = Y.ravel()

    D = []
    for i in range(len(X)):
        point = (X[i],Y[i])
        zvalue = model.encode(point)
        D.append((X[i],Y[i],zvalue))
    D.sort(key=lambda x: x[2])
    D = np.array(D)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(D[:, 0], D[:, 1])
    ax.plot(D[:, 0], D[:, 1])
    for i in range(0, len(D)):
        ax.annotate(D[i,2], (D[i, 0], D[i, 1]))
    fig.show()


def plot_query(model,query,nrange=(0,9),delta=1):
    x = np.arange(nrange[0], nrange[1], delta)
    y = np.arange(nrange[0], nrange[1], delta)
    X, Y = np.meshgrid(x, y)
    X = X.ravel()
    Y = Y.ravel()

    D = []
    for i in range(len(X)):
        point = (X[i],Y[i])
        zvalue = model.encode(point)
        D.append((X[i],Y[i],zvalue))
    D.sort(key=lambda x: x[2])
    D = np.array(D)
    (search_min,search_max) = model.search(query)
    print(search_min,search_max)

    fig, ax = plt.subplots(figsize=(20, 20))
    for point in D:
        if point[2]>= search_min and point[2] <= search_max:
            ax.scatter(point[0], point[1], c='b')
        else:
            ax.scatter(point[0], point[1], c='k')
    for i in range(0, len(D)):
        ax.annotate(D[i,2], (D[i, 0], D[i, 1]))

    (xrange,yrange) = query
    mins = (xrange[0],yrange[0])
    maxs = (xrange[1],yrange[1])
    rect = patches.Rectangle(mins, maxs[0]-mins[0], maxs[1]-mins[1], linewidth=1, edgecolor='r', facecolor='none',zorder=5)
    ax.add_patch(rect)

    fig.show()

def groundTruth(D,Q):
    truth = []
    for (xrange,yrange) in Q:
        result=[]
        for point in D:
            if point[0] >= xrange[0] and point[1] >= yrange[0] and point[0] <= xrange[1] and point[1] <= yrange[1]:
                result.append(point)
        truth.append(np.array(result))
    truth = np.array(truth)
    return truth



X = np.genfromtxt('poi1w_1000.csv',delimiter=",",skip_header=True)


queries = []
gts = groundTruth(X,queries)



sa = SA(initTemp=90,minTemp=1,maxIter=200,tempDelta=1,X=X,base=2)
kernels = sa.learnAll(queries,gts)


