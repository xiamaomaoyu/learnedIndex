import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches



def add_query(query,ax):
    (xrange, yrange) = query
    mins = (xrange[0], yrange[0])
    maxs = (xrange[1], yrange[1])
    rect = patches.Rectangle(mins, maxs[0] - mins[0], maxs[1] - mins[1], linewidth=1, edgecolor='r',
                             facecolor='none', zorder=5)
    ax.add_patch(rect)

def plot_queries(queries,ax):
    for i in range(len(queries)):
        add_query(queries[i],ax)

def plot_data(X,ax):
    ax.scatter(X[:, 0], X[:, 1])


def pt2Square(center,length):
    (x,y) = center
    minx = int(x-length/2)
    maxx = int(x+length/2)
    miny = int(y-length/2)
    maxy = int(y+length/2)
    return [[minx,maxx],[miny,maxy]]

def pts2squares(centers,length):
    results = []
    for i in range(len(centers)):
        results.append(pt2Square(centers[i],length))
    return results

def generate_points(center,quantity):
    l = [center]
    (x_c,y_c) = center
    x = np.random.normal(x_c,10,quantity-1)
    y = np.random.normal(y_c,10,quantity-1)
    for i in range(quantity-1):
        l.append((x[i],y[i]))
    return l

def generate_queries(center,quantity,size):
    pts = generate_points(center, quantity)
    return pts2squares(pts,size)


X = np.genfromtxt('./data/poi/poi1w_1000.csv',delimiter=",",skip_header=True)
# queries = [[[250,270],[80,100]],
#            [[251,271],[81,101]]]


queries = []

center = (1700,2100)
queries += generate_queries(center,quantity=3000,size=30)
center = (1780,2150)
queries += generate_queries(center,quantity=2000,size=20)
center = (1870,2260)
queries += generate_queries(center,quantity=3000,size=30)
center = (1840,2200)
queries += generate_queries(center,quantity=2000,size=10)

fig, ax = plt.subplots(figsize=(20, 10))
plot_data(X,ax)
plot_queries(queries,ax)
fig.show()

print(queries)
print(len(queries))

