import numpy as np
from matplotlib import pyplot as plt
from model import Model,SA
from flex import flexOrder,Kernel,getRandomKernel
import matplotlib.patches as patches
from math import log,ceil
from copy import deepcopy
import pandas as pd


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

def generate_init_k_values(base):
    init_k_value = []
    for i in range(base):
        newl = []
        for j in range(base):
            newl.append(i * base + j)
        init_k_value.append(newl)
    return init_k_value

def kernelswithValue(kernel_values):
    kernels = []
    for i in range(len(kernel_values)):
        k = Kernel(kernel_values[i])
        kernels.append(k)
    return kernels

def kernelsInit(base):
    init_k_value = generate_init_k_values(base)
    kernels_values = []
    for i in range(9):
        kernels_values.append(deepcopy(init_k_value))
    return kernelswithValue(kernels_values)

kernel_0 = [[2, 3], [1, 0]]
kernel_1 = [[0, 2], [3, 1]]
kernel_2 = [[3, 2], [0, 1]]
kernel_3 = [[0, 2], [1, 3]]
kernel_4 = [[0, 2], [1, 3]]
kernel_5 = [[0, 1], [2, 3]]
kernel_6 = [[0, 2], [1, 3]]
kernel_7 = [[1, 2], [0, 3]]
kernel_8 = [[0, 2], [1, 3]]
kernel_values = [kernel_0,
                 kernel_1,
                 kernel_2,
                 kernel_3,
                 kernel_4,
                 kernel_5,
                 kernel_6,
                 kernel_7,
                 kernel_8]

#kernels = kernelswithValue(kernel_values)
kernels = kernelsInit(2)


orderModel = flexOrder(kernels,base=2)

X = np.genfromtxt('poi151482_100_US.csv',delimiter=",",skip_header=True)
queries = []
gts = groundTruth(X,queries)



m = Model(orderModel)
m.fit(X)
print(m.D[:,2])
pd.DataFrame(m.D[:,2]).to_csv('1dExample.csv',index=False)
# check_i = 0
# #m.plot_query(queries[check_i])
# print(m.inefficiency_batch(queries,gts))
# plt.plot(m.D[:,2])
# plt.show()
ranges = []
for i in range(len(queries)):
    ranges.append(m.search(queries[i]))
pd.DataFrame(ranges).to_csv('1dQueriesExample.csv',index=False)