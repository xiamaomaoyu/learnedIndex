# select 500 points from dataset
# scale
# and plot

import numpy as np


import pandas as pd
import random

filename = "poi.csv"

p = 0.1  # 1% of the lines
# keep the header, then take only 1% of lines
# if random from [0,1] interval is greater than 0.01 the row will be skipped
df = pd.read_csv(
         filename,
         header=0,
         skiprows=lambda i: i>0 and random.random() > p
)

a = df.loc[:, 'latitude_radian':'longitude_radian']

a = np.ceil(a * 1000)
a['latitude_radian'] = a['latitude_radian'] - min(a['latitude_radian'])
a['longitude_radian'] = a['longitude_radian'] - min(a['longitude_radian'])
a = a.reindex(columns=['longitude_radian','latitude_radian'])
# print(a)
window = [[1500,2200],[2000,2600]]
b_l = []
for i in range(len(a)) :
    pts = (a.values[i,0],a.values[i,1])
    if pts[0]> window[0][0] and pts[0] < window[0][1] \
            and pts[1]>window[1][0] and pts[1]< window[1][1]:
        b_l.append(pts)
b = np.array(b_l)
print(len(b_l))


from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(20, 15))
ax.scatter(b[:, 0], b[:, 1])
fig.show()
pd.DataFrame(b).to_csv('poi1w_1000.csv',index=False)



