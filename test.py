import numpy as np
import sklearn.neighbors.kd_tree as kt
import random
import matplotlib.pyplot as plt
import AIS

ais=AIS.Ais()
data=open("/home/obinna/NSL-KDD/iris.txt","r")
#print ais.fitness([1,3,4,5,6],[[1,1,2,2,3],[0,0,1,1,1],[2,3,3,3,6],[2,3,4,5,6],[4,5,6,6,4]],50)




#test=random.choice(train)

#print "selected test",test
#tree = kt.KDTree(train, leaf_size=100000)
#dist, ind = tree.query(test, k=3)
#print ind  # indices of 3 closest neighbors
#print dist  # distances to 3 closest neighbors
#print "\n"
#if response[ind[0][1]]=="Iris-virginica":
#    print "it is Iris-virginica"
#elif response[ind[0][1]]=="Iris-versicolor":
#    print "it is Iris-versicolor"
#
#else:
#    print "Iris-setosa"
#print "first indices is ",train[ind[0][1]]

#import math
#Plotting section

#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#k=[0,0.01,0.02,0.09,1.5]
#ax1.plot(k, [math.exp(i) for i in k], c='b',alpha=0.5, label='self')#, c=colors, alpha=0.5)
#ax1.scatter(detector[:,0], detector[:,1], s=area1,c='r',alpha=0.5, label='nonself')
#plt.legend(loc='upper left')

#plt.show()
for i in "hello":
    for j in "tehlat":
        if i==j:
            print i
            break
        print "2nd4"
    print "1st4"