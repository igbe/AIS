#!/usr/bin/env python
import scipy.spatial.distance as dist
import numpy as np
import math
class Ais:
    def __init__(self):
        pass

    def hamming(self,x,y):
        """
        :param x: is the 1D detector or training/test array (i.e normal python array) to be compared to y
        :param y: is the 1D training/test or detector array (i.e normal python array) to be compared to x
        :return:
        """
        x=np.array(x)
        y=np.array(y)
        output=(dist.hamming(x,y))*len(x) #given that scipy divides by length of array for a boolean data, i have divided by n too.
        return output

    def euclidean(self,x,y):
        """
        :param x: is the 1D detector or training/test array (i.e normal python array) to be compared to y
        :param y: is the 1D training/test or detector array (i.e normal python array) to be compared to x
        :return:
        """
        output=math.sqrt(dist.sqeuclidean(x,y))
        return output





