from math import log,ceil,floor
from random import randint

class Code:
    ###
    # value list = [15,20,09]
    # each number is in decimal
    # but represent a digit in 'base'
    # ###
    def __init__(self, base, length):
        self.base = base
        self.length = length
        self.value_list = []
        for i in range(self.length):
            self.value_list.append(0)

    ### Construct By List
    def byList(self,valuelist):
        self.value_list = valuelist
        return self

    def setValue(self,level,value):
        if value < self.base:
            self.value_list[level] = value

    def getValue(self,level):
        return self.value_list[level]


    ### Construct By Value
    def byValue(self,value):
        residual = value
        value_l = []
        for i in reversed(range(0,self.length)):
            base_at_level = self.base**i
            digit = int(residual/base_at_level)
            residual = residual - digit*base_at_level
            value_l.append(digit)
        self.value_list = value_l
        return self


    # return the value of current list
    def value(self):
        v = 0
        for i in range(0,self.length):
            v += self.value_list[i] * self.base ** (self.length-i-1)
        return v

    # return rounded value to level
    # eg. base=2 list=[1,1,1] = 7
    # round to level 1 = [1,1,0]base2 = 6
    def roundToLevel(self,level):
        level = min(self.length,level+1)
        v = 0
        for i in range(0,level):
            v += self.value_list[i] * self.base ** (self.length-i-1)
        return v

    # return range at level
    # eg base=2 list=[1,1,1] = 7
    # range at level 0 = [0,1,0,0] - [1,0,0,0] = 4 - 8
    # range at level 1 = [0,1,1,0] - [1,0,0,0] = 6 - 8
    def rangeAtLevel(self,level):
        min = self.roundToLevel(level)
        max = min + self.base**(self.length-level-1)-1
        return (min,max)



class Kernel:

    def __init__(self,array):
        self.values = array
        self.height = len(self.values)
        self.width = len(self.values[0])
        self.min = 0
        self.max = self.width * self.height


    def valueToIndex(self,value):
        for j in range(self.height):
            for i in range(self.width):
                if self.values[j][i] == value:
                    return (i,j)
        # print("wrong look up value",value)
        return (-1,-1)

    def indexToValue(self,x,y):
        return self.values[y][x]

    # xrange = [0,1]
    # return [[minvalue,(minx,miny)],[maxvalue,(maxx,maxy)]]
    def rangeSearch(self,xrange,yrange):
        if xrange[1] < xrange[0]:
            xrange[1] = xrange[1] + self.width
        if yrange[1] < yrange[0]:
            yrange[1] = yrange[1] + self.height
        candidates = []
        for j in range(yrange[0], yrange[1] + 1):
            for i in range(xrange[0], xrange[1] + 1):
                candidates.append(self.values[j%self.height][i%self.width])
        minvalue = min(candidates)
        maxvalue = max(candidates)
        (minx,miny) = self.valueToIndex(minvalue)
        (maxx,maxy) = self.valueToIndex(maxvalue)
        return [[minvalue, (minx, miny)], [maxvalue, (maxx, maxy)]]

    def randomSwap(self):
        a = (randint(0,self.width-1),randint(0,self.height-1))
        b = (randint(0,self.width-1),randint(0,self.height-1))
        temp = self.values[a[0]][a[1]]
        self.values[a[0]][a[1]] = self.values[b[0]][b[1]]
        self.values[b[0]][b[1]] = temp


def getRandomKernel():
    k_value = [[0, 1, 2, 3],
               [4, 5, 6, 7],
               [8, 9, 10, 11],
               [12, 13, 14, 15]]
    k = Kernel(k_value)
    for i in range(100):
        k.randomSwap()
    return k






class flexOrder:

    def __init__(self,kernels,base):
        self.kernels = kernels
        self.base = base
        self.z_base = base*base
        self.tree_height = len(kernels)

    def encode(self,point):
        (x,y) = point
        xcode = Code(base=self.base,length=self.tree_height).byValue(x)
        ycode = Code(base=self.base,length=self.tree_height).byValue(y)
        z_l = []
        for i in range(self.tree_height):
            z_v = self.kernels[i].indexToValue(xcode.value_list[i],ycode.value_list[i])
            z_l.append(z_v)
        zcode = Code(base=self.z_base,length=self.tree_height).byList(z_l)
        return zcode.value()

    def decode(self,v):
        x_l = []
        y_l = []
        zcode = Code(base=self.z_base,length=self.tree_height).byValue(v)
        for i in range(self.tree_height):
            (x_v,y_v) = self.kernels[i].valueToIndex(zcode.value_list[i])
            x_l.append(x_v)
            y_l.append(y_v)
        xcode = Code(base=self.base,length=self.tree_height).byList(x_l)
        ycode = Code(base=self.base,length=self.tree_height).byList(y_l)
        return (xcode.value(),ycode.value())


    ###
    # query = [[xmin,xmax],[ymin,ymax]]
    # ###
    def search(self,query):
        minxcode = Code(base=self.base,length=self.tree_height)
        minycode = Code(base=self.base,length=self.tree_height)
        mincode = Code(base=self.z_base,length=self.tree_height)
        maxxcode = Code(base=self.base,length=self.tree_height)
        maxycode = Code(base=self.base,length=self.tree_height)
        maxcode = Code(base=self.z_base,length=self.tree_height)
        self.search_min(query,0,mincode,minxcode,minycode)
        self.search_max(query,0,maxcode,maxxcode,maxycode)
        return (mincode.value(),maxcode.value())


    def search_min(self,query,level,zcode,xcode,ycode):
        # terminate condition
        if level >= self.tree_height:
            return

        # extract query
        q_xmin = Code(base=self.base, length=self.tree_height).byValue(query[0][0])
        q_xmax = Code(base=self.base, length=self.tree_height).byValue(query[0][1])
        q_ymin = Code(base=self.base, length=self.tree_height).byValue(query[1][0])
        q_ymax = Code(base=self.base, length=self.tree_height).byValue(query[1][1])

        # print("level:",level)
        # print(q_xmin.value_list,q_xmin.value())
        # print(q_xmax.value_list,q_xmax.value())
        # print(q_ymin.value_list,q_ymin.value())
        # print(q_ymax.value_list,q_ymax.value())



        # search at kernel
        [[minvalue, (minx, miny)], _] = self.kernels[level].rangeSearch(
            [q_xmin.getValue(level), q_xmax.getValue(level)],
            [q_ymin.getValue(level), q_ymax.getValue(level)])
        zcode.setValue(level, minvalue)
        xcode.setValue(level, minx)
        ycode.setValue(level, miny)
        # print(minx,miny,minvalue)
        # print('xcode',xcode.value_list,xcode.value())
        # print('ycode',ycode.value_list,ycode.value())
        # print('zcode',zcode.value_list,zcode.value())
        # update query

        block_xrange = xcode.rangeAtLevel(level)
        block_yrange = ycode.rangeAtLevel(level)
        new_query = rect_intersect([block_xrange, block_yrange], query)
        # print('block',[block_xrange, block_yrange])
        # print('query',query)
        # print('newquery',new_query)

        # recursion
        self.search_min(new_query, level + 1, zcode, xcode, ycode)


    def search_max(self, query, level, zcode, xcode, ycode):
        # terminate condition
        if level >= self.tree_height:
            return

        # extract query
        q_xmin = Code(base=self.base, length=self.tree_height).byValue(query[0][0])
        q_xmax = Code(base=self.base, length=self.tree_height).byValue(query[0][1])
        q_ymin = Code(base=self.base, length=self.tree_height).byValue(query[1][0])
        q_ymax = Code(base=self.base, length=self.tree_height).byValue(query[1][1])
        # print("level:",level)
        # print(q_xmin.value_list,q_xmin.value())
        # print(q_xmax.value_list,q_xmax.value())
        # print(q_ymin.value_list,q_ymin.value())
        # print(q_ymax.value_list,q_ymax.value())

        # search at kernel

        [_, [maxvalue, (maxx, maxy)]] = self.kernels[level].rangeSearch(
            [q_xmin.getValue(level), q_xmax.getValue(level)],
            [q_ymin.getValue(level), q_ymax.getValue(level)])
        zcode.setValue(level, maxvalue)
        xcode.setValue(level, maxx)
        ycode.setValue(level, maxy)
        # print(maxx,maxy,maxvalue)
        # print('xcode',xcode.value_list,xcode.value())
        # print('ycode',ycode.value_list,ycode.value())
        # print('zcode',zcode.value_list,zcode.value())

        # update query

        block_xrange = xcode.rangeAtLevel(level)
        block_yrange = ycode.rangeAtLevel(level)
        new_query = rect_intersect([block_xrange, block_yrange], query)

        # print('block',[block_xrange, block_yrange])
        # print('query',query)
        # print('newquery',new_query)

        # recursion
        self.search_max(new_query, level + 1, zcode, xcode, ycode)


###
# a = [[xmin,xmax],[ymin,ymax]]
# b = [[xmin,xmax],[ymin,ymax]]
# ###
def rect_intersect(a,b):
    xmin = max(a[0][0],b[0][0])
    ymin = max(a[1][0],b[1][0])
    xmax = min(a[0][1],b[0][1])
    ymax = min(a[1][1],b[1][1])
    if xmin <= xmax and ymin <= ymax:
        return [[xmin,xmax],[ymin,ymax]]


