import numpy as np
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from math import log,ceil,exp
from flex import Kernel,flexOrder
from copy import deepcopy
from random import random




def generate_init_k_values(base):
    init_k_value = []
    for i in range(base):
        newl = []
        for j in range(base):
            newl.append(i * base + j)
        init_k_value.append(newl)
    return init_k_value


class Model:

    def __init__(self,orderModel):
        self.orderModel = orderModel

    def fit(self,X):
        D = []
        for i in range(len(X)):
            point = (int(X[i][0]), int(X[i][1]))
            zvalue = self.orderModel.encode(point)
            D.append((point[0], point[1], zvalue))
        D.sort(key=lambda x: x[2])
        D = np.array(D)
        self.D = D

    def search(self,query):
        return self.orderModel.search(query)

    def inefficiency(self,query,gt):
        (search_min,search_max) = self.search(query)
        candidates = []
        for point in self.D:
            if point[2] >= search_min and point[2] <= search_max:
                candidates.append(point)
        if len(candidates) == 0:
            return 0
        return 1-len(gt)/len(candidates)

    def inefficiency_batch(self,queries,gts):
        ret = 0
        for i in range(len(queries)):
            ineff =self.inefficiency(queries[i],gts[i])
            ret += ineff
            #print(i,ineff)
        return ret/len(queries)

    def inefficiency_batch_nonblank(self,queries,gts):
        ret = 0
        count = 0
        for i in range(len(queries)):
            if gts[i] > 0:
                ret += self.inefficiency(queries[i],gts[i])
                count += 1
        return ret/count

    def plot_query(self,query):
        (search_min, search_max) = self.search(query)

        fig, ax = plt.subplots(figsize=(20, 10))
        ax.scatter(self.D[:, 0], self.D[:, 1])

        for point in self.D:
            if point[2] >= search_min and point[2] <= search_max:
                ax.scatter(point[0], point[1], c='b')
            else:
                ax.scatter(point[0], point[1], c='k')

        (xrange, yrange) = query
        mins = (xrange[0], yrange[0])
        maxs = (xrange[1], yrange[1])
        rect = patches.Rectangle(mins, maxs[0] - mins[0], maxs[1] - mins[1], linewidth=1, edgecolor='r',
                                 facecolor='none', zorder=5)
        ax.add_patch(rect)

        fig.show()



class SA:

    def __init__(self,initTemp,minTemp,maxIter,tempDelta,X,base):
        self.initTemp = initTemp
        self.minTemp = minTemp
        self.maxIter = maxIter
        self.tempDelta = tempDelta


        init_k_value = generate_init_k_values(base=base)
        treeheight = max(ceil(log(max(X[:,0]),base)),ceil(log(max(X[:,1]),base)))
        self.treeheight = treeheight
        kernels_values = []
        for i in range(treeheight):
            kernels_values.append(deepcopy(init_k_value))
        kernels = []
        for i in range(treeheight):
            k = Kernel(kernels_values[i])
            kernels.append(k)


        self.init_kernels = kernels
        self.X = X
        self.base = base

    def learnAll(self,q,gt):
        print("start_learning!")
        kernels = deepcopy(self.init_kernels)
        for i in range(0,self.treeheight):
            kernels,ineffiency = self.learnLevel(i,q,gt,kernels,printMessage=False)
            print("trained level ", i)
            for j in range(0, self.treeheight):
                print('kernel_',j,'=',kernels[j].values)
            print(ineffiency)
        return kernels

    def learnLevel(self,level,q,gt,kernels,printMessage=False):

        m = self.fit_model(kernels,self.base)
        energy = m.inefficiency_batch(q,gt)

        iters = 0
        temp = self.initTemp
        while iters < self.maxIter and temp > self.minTemp:
            if printMessage:
                print("current temp = ",temp)
            # generate new kernel
            new_kernels = deepcopy(kernels)
            new_kernels[level].randomSwap()
            m = self.fit_model(new_kernels,self.base)
            new_energy = m.inefficiency_batch(q, gt)

            if new_energy < energy: # accept that solution
                kernels = new_kernels
                temp -= self.tempDelta
                energy = new_energy
                iters = 0
                if printMessage:
                    print("better solution accepted")
                    print(kernels[level].values)
                    print(new_energy)
                    print("!!!!!!!!!!!")
            elif random() < self.accept_probability(new_energy,energy,temp):
                kernels = new_kernels
                temp -= self.tempDelta
                energy = new_energy
                iters = 0
                if printMessage:
                    print("worse solution accepted")
                    print(kernels[level].values)
                    print(new_energy)

            else:
                iters += 1
                if printMessage:
                    print(iters,"worse solution rejected ",new_energy)

        return (kernels,energy)




    def fit_model(self,kernels,base):
        orderModel = flexOrder(kernels, base)
        m = Model(orderModel)
        m.fit(self.X)
        return m

    def accept_probability(self,new_energy,energy,temp):
        energy_delta = (new_energy - energy)/energy
        a = (10000*(energy_delta))/temp
        return exp(-a)
