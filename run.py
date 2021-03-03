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



X = np.genfromtxt('./data/poi/poi1w_1000.csv',delimiter=",",skip_header=True)


queries = [[[1685, 1715], [2085, 2115]], [[1686, 1716], [2100, 2130]], [[1706, 1736], [2097, 2127]], [[1686, 1716], [2081, 2111]], [[1689, 1719], [2100, 2130]], [[1675, 1705], [2093, 2123]], [[1690, 1720], [2074, 2104]], [[1698, 1728], [2099, 2129]], [[1691, 1721], [2085, 2115]], [[1670, 1700], [2067, 2097]], [[1690, 1720], [2079, 2109]], [[1687, 1717], [2082, 2112]], [[1680, 1710], [2067, 2097]], [[1665, 1695], [2073, 2103]], [[1687, 1717], [2079, 2109]], [[1674, 1704], [2072, 2102]], [[1669, 1699], [2089, 2119]], [[1681, 1711], [2098, 2128]], [[1684, 1714], [2079, 2109]], [[1697, 1727], [2078, 2108]], [[1770, 1790], [2140, 2160]], [[1770, 1790], [2151, 2171]], [[1748, 1768], [2141, 2161]], [[1782, 1802], [2144, 2164]], [[1771, 1791], [2153, 2173]], [[1765, 1785], [2145, 2165]], [[1757, 1777], [2122, 2142]], [[1771, 1791], [2133, 2153]], [[1763, 1783], [2134, 2154]], [[1785, 1805], [2138, 2158]], [[1855, 1885], [2245, 2275]], [[1859, 1889], [2240, 2270]], [[1854, 1884], [2234, 2264]], [[1840, 1870], [2238, 2268]], [[1860, 1890], [2254, 2284]], [[1847, 1877], [2253, 2283]], [[1868, 1898], [2235, 2265]], [[1852, 1882], [2246, 2276]], [[1849, 1879], [2247, 2277]], [[1852, 1882], [2248, 2278]], [[1854, 1884], [2239, 2269]], [[1862, 1892], [2244, 2274]], [[1859, 1889], [2253, 2283]], [[1866, 1896], [2239, 2269]], [[1871, 1901], [2251, 2281]], [[1865, 1895], [2246, 2276]], [[1859, 1889], [2245, 2275]], [[1861, 1891], [2256, 2286]], [[1858, 1888], [2252, 2282]], [[1844, 1874], [2255, 2285]], [[1835, 1845], [2195, 2205]], [[1837, 1847], [2183, 2193]], [[1813, 1823], [2193, 2203]], [[1841, 1851], [2194, 2204]], [[1840, 1850], [2182, 2192]], [[1847, 1857], [2198, 2208]], [[1831, 1841], [2189, 2199]], [[1841, 1851], [2183, 2193]], [[1827, 1837], [2193, 2203]], [[1829, 1839], [2194, 2204]]]

gts = groundTruth(X,queries)



sa = SA(initTemp=90,minTemp=1,maxIter=200,tempDelta=1,X=X,base=2)
kernels = sa.learnAll(queries,gts)


