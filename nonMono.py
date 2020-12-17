from math import log, ceil

class COrder:

    def __init__(self,kernels,base,tree_height=2):
        self.kernels = kernels
        self.x_base = base
        self.y_base = base
        self.z_base = self.x_base*self.y_base
        self.tree_height = tree_height

    def encode(self,point):
        (x,y) = point
        strlen = self.tree_height
        x_b = dec_to_base(x,self.x_base,strlen)
        y_b = dec_to_base(y,self.y_base,strlen)
        z_l = []
        for i in range(0,strlen):
            z_l.append(self.kernels[i][int(x_b[i])][int(y_b[i])])

        z_b = "".join(z_l)
        z = int(z_b, self.z_base)
        return z

    def decode(self,z):
        strlen = self.tree_height
        z_b = dec_to_base(z,self.z_base,strlen)
        x_l = []
        y_l = []
        for i in range(0,strlen):
            (x_bit,y_bit) = kernel_lookup(self.kernels[i],z_b[i])
            x_l.append(str(x_bit))
            y_l.append(str(y_bit))
        x_b = "".join(x_l)
        y_b = "".join(y_l)

        x = int(x_b, self.x_base)
        y = int(y_b, self.y_base)
        point = (x,y)
        return point

    def search(self,query):
        min_q = query
        max_q = query
        min_b_l = []
        max_b_l = []
        for i in range(0,self.tree_height):
            (min_bit, _), (min_q, _) = self.search_at_level(i,min_q)
            (_,max_bit),(_,max_q) = self.search_at_level(i,max_q)
            min_b_l.append(str(min_bit))
            max_b_l.append(str(max_bit))
        min_b = "".join(min_b_l)
        max_b = "".join(max_b_l)
        min = int(min_b,self.z_base)
        max = int(max_b,self.z_base)
        return (min,max)


    def search_at_level(self,level,query):
        (mins, maxs) = query
        (min_x, min_y) = mins
        (max_x, max_y) = maxs
        strlen = self.tree_height
        minx_b = dec_to_base(min_x, self.x_base, strlen)
        miny_b = dec_to_base(min_y, self.y_base, strlen)
        maxx_b = dec_to_base(max_x, self.x_base, strlen)
        maxy_b = dec_to_base(max_y, self.y_base, strlen)
        query_b = [[minx_b[level], miny_b[level]], [maxx_b[level], maxy_b[level]]]
        (new_min, new_max) = kernel_rangeSearch(self.kernels[level], query_b)

        x_base = self.x_base ** (self.tree_height-1-level)
        y_base = self.y_base ** (self.tree_height-1-level)

        (new_min_x_b, new_min_y_b) = kernel_lookup(self.kernels[level], str(new_min))
        min_block_xmin = x_base * new_min_x_b
        min_block_ymin = y_base * new_min_y_b
        min_block_xmax = x_base * (new_min_x_b + 1) - 1
        min_block_ymax = y_base * (new_min_y_b + 1) - 1
        min_block = [[min_block_xmin, min_block_ymin], [min_block_xmax, min_block_ymax]]
        min_rect = rect_intersect(min_block, query)

        (new_max_x_b, new_max_y_b) = kernel_lookup(self.kernels[level], str(new_max))
        max_block_xmin = x_base * new_max_x_b
        max_block_ymin = y_base * new_max_y_b
        max_block_xmax = x_base * (new_max_x_b + 1) - 1
        max_block_ymax = y_base * (new_max_y_b + 1) - 1
        max_block = [[max_block_xmin, max_block_ymin], [max_block_xmax, max_block_ymax]]
        max_rect = rect_intersect(max_block, query)

        return ((new_min, new_max), (min_rect, max_rect))







def kernel_lookup(kernel,value):
    res = []
    for i in range(len(kernel)):
        for j in range(len(kernel[0])):
            if kernel[i][j] == value:
                res = (i,j)
    return res


def dec_to_base(num,base,strlen):  # Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num%base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  # Using uppercase letters
        num //= base
    base_num = base_num[::-1]  # To reverse the string
    while len(base_num) < strlen:
        base_num = "0" + base_num
    return base_num


# rect is defined as
# a = [mins,maxs]    a = [[0,0],[40,20]]
def rect_intersect(a,b):
    c_xmin = max(a[0][0],b[0][0])
    c_xmax = min(a[1][0],b[1][0])
    c_ymin = max(a[0][1],b[0][1])
    c_ymax = min(a[1][1],b[1][1])
    if c_xmin < c_xmax and c_ymin < c_ymax:
        return [[c_xmin,c_ymin],[c_xmax,c_ymax]]
    else:
        return [[0,0],[0,0]]



def kernel_rangeSearch(kernel,query):
    x_min = int(query[0][0])
    x_max = int(query[1][0])
    y_min = int(query[0][1])
    y_max = int(query[1][1])
    base = len(kernel)**2
    candidates = []
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            candidates.append(int(kernel[i][j],base=base))
    return(min(candidates),max(candidates))

# kernel1 = [['0','1','2'],
#           ['3','4','5'],
#           ['6','7','8']]
#
# query = [[1,1],
#          [5,7]]
#
# print(kernel_rangeSearch(kernel1,query))


# rect = [[0,0],[2,2]]
# print(rect_intersect(query,rect))


