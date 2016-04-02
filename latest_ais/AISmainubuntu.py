import AIS
import GeneticAlgorithm
import sklearn.neighbors.kd_tree as kt
import random
import numpy as np
import math


file2=open("/home/obinna/PycharmProjects/AIS/8kddnormalizedtrain20.txt","r")
file3=open("/home/obinna/PycharmProjects/AIS/detector.txt","w")

ais_instance1=AIS.Ais()

def initial_individual_sample(pop_size):
    i=0
    detector=[]
    while i < pop_size:
        at=[]
        for k in range(0,8):
            a=random.random()
            b=random.choice([1,1,1,1,1,1,1,1,1,1,1,0,0,0,0.1,0.01,0.001,0.0001,0.00001,0.000001,0.0000001,0.00000001,0.000000001])
            p=a*b
            at.append(p)
        #print at
        detector.append(at)
        i=i+1
    return detector



def generate_ga_detectors(num_gen, individual_sample, p_mutation, p_crossover, self_distance_tree, self_radius):
    ga_instance=GeneticAlgorithm.GeneticAlgorithm()
    pop=individual_sample
    #z=pop
    print "performing GA..."
    print "Initial population"
    #print z
    num_pop=len(individual_sample)
    for i in range(0, num_gen):
        print "Generation",i

        for j in range(0,num_pop):
            print "generation", i
            parent1,parent2=random.sample(pop,2) #np.array(random.sample(pop,2))
            l1=pop.index(parent1)
            l2=pop.index(parent2)
            print "parent1",parent1
            print  "parent2",parent2
            child_pair=ga_instance.crossover(parent1,parent2,1,p_crossover)
            print "cross_child",child_pair
            children=ga_instance.mutate1(child_pair,p_mutation)
            print "mutat_child",children

            d0=ais_instance1.euclidean(children[0],parent1)
            print "d0=",d0
            d1=ais_instance1.euclidean(children[1],parent2)
            print "d1=",d1
            f0=ga_instance.fitnesstest(children[0],self_distance_tree,self_radius)
            print "f0=",f0
            f1=ga_instance.fitnesstest(children[1],self_distance_tree,self_radius)
            print "f1=",f1
            f2=ga_instance.fitnesstest(parent1,self_distance_tree,self_radius)
            print "f2=",f2
            f3=ga_instance.fitnesstest(parent2,self_distance_tree,self_radius)
            print "f3=",f3
            if (d0>self_radius)and(f0>f2):
                print "replacing parent1 with child 1"
                pop[l1]=children[0]
            if (d1>self_radius)and(f1>f3):
                print "replacing parent2 with child 2"
                pop[l2]=children[1]
            #print '\n'
    return  pop#print pop1


#note pass a test list/array with the third row, then use the 3rd row for classification
def test_detector(detector_population,test_set,self_radius=0.0):

    tree= kt.KDTree(detector_population, leaf_size=100000, metric='euclidean') #euclidean

    false_positive=0  #when a normal gets classified as an attack
    false_negative=0  #when an attack gets classified as normal
    true_positive=0   #Also called sensitivity is the proportion of attacks that are correctly classified
    true_negative=0    #Also called Specificity is the proportion of non-attacks that gets correctly classified as such

    i=0
    for value in test_set:
        #print "picking new test set value"
        dist,ind=tree.query([value[0:-1]], k=2, return_distance=True)
        print "distance= ", dist[0][1]
        if dist[0][1]<=self_radius:
            print "attack detected"
            if test_set[i][-1]=='normal':   #'Iris-setosa':
                false_positive=false_positive+1
            else:
                true_positive=true_positive+1
        else:
            print "no attack detected"
            #print "text set i is= ", test_set[i][-1]
            if test_set[i][-1]=='normal':       #'Iris-setosa':
                true_negative=true_negative+1
            else:
                false_negative=false_negative+1
        i=i+1
        print "FP= ",false_positive," FN= ",false_negative, "TP= ", true_positive, " TN= ",true_negative
    #print "number classified as attack =",len(attack)

    print "FP= ",false_positive," FN= ",false_negative, "TP= ", true_positive, " TN= ",true_negative
    try:
        DR=(float(true_positive)/(true_positive+false_negative))
    except ZeroDivisionError:
        DR=0.0
    try:
        FA=(float(false_positive)/(false_positive+true_negative))
    except ZeroDivisionError:
        FA=0.0

    print "Detector Rate (DR)= ", DR,"False Alarm Rate (FA)= ", FA
    stat=[false_positive,false_negative,true_positive,true_negative]
    return stat


def main():
    ##To partition the dataset into two. One for training and another for testing
    percentage_split=66   #value to give to training
    all=[]
    normal=[]
    for i in file2:
        a=i.strip().split("\t")
        b=[]
        for k in a:
            if k == "normal":
                b.append(k)
            elif k== "anomaly":
                b.append(k)
            else:
                b.append(float(k))
        #print(b)
        all.append(b)

    len_of_all=len(all)
    split_point=int(round((percentage_split/float(100))*len_of_all,0))
    #print len_of_all
    test=all[split_point:]
    j=0
    for i in all:
        if (i[-1]=="normal")and (j<split_point):
            normal.append(i[0:-1])
            j=j+1


    #print normal
    #To get the distance tree for all the normal samples
    self_distance_tree= kt.KDTree(normal, leaf_size=100000, metric="euclidean")#'manhattan')

    #number of detector population and no of generations
    num_pop=60000
    num_gen=20

    #to get the initial detector population sample to be used for the GA we use
    initial_pop=initial_individual_sample(num_pop)

    p_mutation=2.0/len(normal[0])
    print "prob of mutation=",p_mutation
    p_crossover=1.0
    print "prob of crossover=",p_crossover
    self_radius=0.38000#0.56911

    detector_population=generate_ga_detectors(num_gen,initial_pop,p_mutation,p_crossover,self_distance_tree,self_radius)   #in mutation, try flipping more than one attribute(0,2,3 and5)
    #print detector_population

    test_detector(detector_population,test,self_radius)
    #print len(test)

    #To write these generated detectors to a file
    file3.write("{0}".format(detector_population))
    file3.close()

if __name__=="__main__":
    main()