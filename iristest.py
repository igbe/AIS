import numpy as np
import sklearn.neighbors.kd_tree as kt
import random
import matplotlib.pyplot as plt

data=open("/home/obinna/NSL-KDD/iris.txt","r")
r=3
def get_data(data):
    train=[]
    response=[]
    for i in data:
        t=i.strip().split(",")
        train.append([int(float(i)*10) for i in t[2:len(t)-1]])
        response.append(t[-1])
    train=np.array(train)
    response=np.array(response)
    return train,response,min(train[:,0]),max(train[:,0]),min(train[:,1]),max(train[:,1])


def get_plot(train,detector,r1=3,r2=3.3):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    area=np.pi*(r1)**2
    area1=np.pi*(r2)**2
    ax1.scatter(detector[:,0], detector[:,1], s=area1,c='r', label='nonself')
    ax1.scatter(train[:,0], train[:,1], s=area, c='b',label='self')#, c=colors, alpha=0.5)

    plt.legend(loc='upper left')

    plt.show()





train,response,maxx,maxy,maxx1,maxy1=get_data(data)

detector=[]

for i in range(0,10000):
    detector.append([np.random.random_integers(maxx,maxy+1),np.random.random_integers(maxx1,maxy1+1)])

detector=np.array(detector)

#print maxx,maxy,maxx1,maxy1

get_plot(train,detector)

#print response






#detector=np.array(detector)

#print train

