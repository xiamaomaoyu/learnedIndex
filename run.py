import numpy as np
from matplotlib import pyplot as plt
from nonMono import COrder
import matplotlib.patches as patches




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

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(D[:, 0], D[:, 1])
    ax.plot(D[:, 0], D[:, 1])
    for i in range(0, len(D)):
        ax.annotate(D[i,2], (D[i, 0], D[i, 1]))

    (mins,maxs) = query
    rect = patches.Rectangle(mins, maxs[0]-mins[0], maxs[1]-mins[1], linewidth=1, edgecolor='r', facecolor='none',zorder=5)
    ax.add_patch(rect)

    fig.show()

kernel1 = [['0','1','2'],
          ['3','5','4'],
          ['6','7','8']]
kernel2 = [['8','7','6'],
          ['3','4','5'],
          ['2','1','0']]
query = [[1,1],[5,7]]
kernels = [kernel1,kernel2]
model = COrder(kernels,base=3)
plot_query(model,query)


(new_min, new_max), (min_rect, max_rect) = model.search_at_level(0,query)
print((new_min, new_max), (min_rect, max_rect))
print(model.search(query))