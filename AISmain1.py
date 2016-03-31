import AIS
import matplotlib.pyplot as plt
import GeneticAlgorithm
import sklearn.neighbors.kd_tree as kt
import random
import numpy as np
import math

#Note in this file i have set the decimal points to be 11
file2=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar2\\new\\normal500.csv")
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar2\\new\\test1300.csv")
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar2\\sixty_six\\normal.csv")
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar2\\sixty_six\\34percenttest.csv")

file3=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar\\detector.txt","w")
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\irisself.csv","r")
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\irisall.csv","r")

ais_instance1=AIS.Ais()

def generate_ga_detectors(num_pop,num_gen,self_set,p_mutation,p_crossover,self_distance_tree,self_radius):
    ga_instance=GeneticAlgorithm.GeneticAlgorithm()
    pop=self_set
    #pop=np.ndarray.tolist(self_set)
    #pop=self_set
    if num_pop>len(pop):
        diff=num_pop-len(pop)
        for y in range(diff):
            q=random.sample(pop,1)
            pop.append(q[0])


    #z=pop
    print "performing GA..."
    print "Initial population"
    #print z

    for i in range(0,num_gen):
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
            children=ga_instance.mutate(child_pair,p_mutation)
            print "mutat_child",children

            d0=ais_instance1.manhattan(children[0],parent1)
            print "d0=",d0
            d1=ais_instance1.manhattan(children[1],parent2)
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
                print "replacing parent1 which child 1"
                pop[l1]=children[0]
            if (d1>self_radius)and(f1>f3):
                print "replacing parent2 which child 2"
                pop[l2]=children[1]
            #print '\n'
    return  pop#print pop1
#note pass a test list/array with the third row, then use the 3rd row for classification
def test_detector(detector_population,test_set,normal_list1,self_radius=0.0):
    tree= kt.KDTree(detector_population, leaf_size=100000, metric='manhattan') #euclidean
    false_positive=0  #when a normal gets classified as an attack
    false_negative=0  #when an attack gets classified as normal
    true_positive=0   #Also called sensitivity is the proportion of attacks that are correctly classified
    true_negative=0    #Also called Specificity is the proportion of non-attacks that gets correctly classified as such
    i=0
    #print "test",test_set
    #print "detector", detector_population
    for value in normal_list1:
        #print "picking new test set value"
        dist,ind=tree.query([value], k=2, return_distance=True)
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

    test=[]
    normal_list1=[]
    classification_list1=[]
    #use the location of the attributes as their index
    for i in file2:
        a=i.strip().split(",")[0:-1]
        b=i.strip().split(",")
        #print "a is: ", a
        normal_list1.append([float(i) for i in a ])
        classification_list1.append(b[-1])
        print "still prcessing file"
    #print normal_list1
    L=len(normal_list1)
    for m in range(L):
        test.append(normal_list1[m]+[classification_list1[m]])
    #detector_population=

    self_distance_tree= kt.KDTree(normal_list1, leaf_size=100000, metric='manhattan')
    num_pop=100000
    num_gen=20
    p_mutation=2.0/len(normal_list1[0])
    print "prob of mutation=",p_mutation
    p_crossover=1.0
    print "prob of crossover=",p_crossover
    self_radius=0.020000#0.56911
    detector_population=generate_ga_detectors(num_pop,num_gen,normal_list1,p_mutation,p_crossover,self_distance_tree,self_radius)   #in mutation, try flipping more than one attribute(0,2,3 and5)
    #print detector_population
    file3.write("{0}".format(detector_population))
    file3.close()
    #print pop
    #test_detector(detector_population,test,normal_list1,self_radius)
    #print max_individual_dist
    #y=np.array(pop)
    #plt.plot(y[:,1],y[:,0], 'bo')
    #plt.show()
if __name__=="__main__":
    main()


