import AIS
import matplotlib.pyplot as plt
import GeneticAlgorithm
import sklearn.neighbors.kd_tree as kt
import random
import numpy as np
import math

#Note in this file i have set the decimal points to be 11
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar2\\normalized8kdd20percenttrain.csv")#normalall15my20perkddtrain+.csv","r")
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar2\\sixty_six\\normal.csv")
file2=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar2\\sixty_six\\34percenttest.csv")

#file3=open("C:\Users\Obinna\Desktop\NSL-KDD\\biostar\\detector.txt","w")
#file2=open("C:\Users\Obinna\Desktop\NSL-KDD\irisself.csv","r")
#file1=open("C:\Users\Obinna\Desktop\NSL-KDD\irisall.csv","r")

ais_instance1=AIS.Ais()

def generate_ga_detectors(num_pop,num_gen,self_set,p_mutation,p_crossover,max_individual_dist,round_off=1):
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
    k=0
    for i in range(0,num_gen):
        print "Generation",k
        k=k+1

        for j in range(0,num_pop):
            print "generation", k
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
            f0=ga_instance.fitness(children[0],self_set,100)
            print "f0=",f0
            f1=ga_instance.fitness(children[1],self_set,100)
            print "f1=",f1
            f2=ga_instance.fitness(parent1,self_set,100)
            print "f2=",f2
            f3=ga_instance.fitness(parent2,self_set,100)
            print "f3=",f3
            if (d0>max_individual_dist)and(f0>f2):
                print "replacing parent1 which child 1"
                pop[l1]=children[0]
            elif (d1>max_individual_dist)and(f1>f3):
                print "replacing parent2 which child 2"
                pop[l2]=children[1]
            #print '\n'
    return  pop#print pop1
#note pass a test list/array with the third row, then use the 3rd row for classification
def test_detector(detector_population,test_set,radius=0.0):
    false_positive=0  #when a normal gets classified as an attack
    false_negative=0  #when an attack gets classified as normal
    true_positive=0   #Also called sensitivity is the proportion of attacks that are correctly classified
    true_negative=0    #Also called Specificity is the proportion of non-attacks that gets correctly classified as such
    i=0
    #print "test",test_set
    #print "detector", detector_population
    for value in test_set:
        #print "picking new test set value"
        for detector in detector_population:
            d=ais_instance1.manhattan(detector,value[0:-1])
            if d<radius:
                print "attack detected"
                #attack.append(value)
                if test_set[i][-1]=='normal':
                    false_positive=false_positive+1
                else:
                    true_positive=true_positive+1
                break
            else:
                print "no attack detected"
                #print "text set i is= ", test_set[i][-1]
                if test_set[i][-1]=='normal':
                    true_negative=true_negative+1
                else:
                    false_negative=false_negative+1
                break
        i=i+1
        print "FP= ",false_positive," FN= ",false_negative, "TP= ", true_positive, " TN= ",true_negative
    #print "number classified as attack =",len(attack)

    print "FP= ",false_positive," FN= ",false_negative, "TP= ", true_positive, " TN= ",true_negative
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
    #print test
    #print classification_list1

    #normal_list=np.array(normal_list1)
    #classification_list=np.array(classification_list1)
    #print normal_list
    #print classification_list


    #to get the maximum values between self_set values. To be used in genetic algorithm for distance and fitness child replacement
#    out=ais_instance1.distance_matrix(normal_list1,'cityblock')


    #ais_instance1.squareform(out) #to print the whole symetric distance matrix
    #print len(out)


#    max_individual_dist=0.5#out.max()#0.293079


    #plt.plot(normal_list[:,1],normal_list[:,0], 'ro')
    #plt.show()
    #detector_population=
    population=(normal_list1)
    num_pop=10000
    num_gen=5
    p_mutation=1.0/len(normal_list1[0])
    print "prob of mutation=",p_mutation
    p_crossover=1.0
    print "prob of crossover=",p_crossover
#    detector_population=generate_ga_detectors(num_pop,num_gen,normal_list1,p_mutation,p_crossover,max_individual_dist)   #in mutation, try flipping more than one attribute(0,2,3 and5)
    #print detector_population
#    file3.write("{0}".format(detector_population))
#    file3.close()
    #print pop
    test_detector(detector_population,test,radius=1.7000)
    #print max_individual_dist
    #y=np.array(pop)
    #plt.plot(y[:,1],y[:,0], 'bo')
    #plt.show()
if __name__=="__main__":
    main()


