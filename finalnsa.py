#!/usr/bin/env python
import AIS
import random
import numpy as np
import math
ais_instance1=AIS.Ais()
file1=open("/home/obinna/NSL-KDD/KDDTrain+_20Percent.arff","r")


cfs_genetic_15=[3,4,5,6,12,16,18,25,26,29,30,31,36,37,38]
ig_ranking_15=[5,3,6,4,30,29,33,34,35,38,12,39,25,23,26]
#ig_ranking_20=[5,3,6,4,30,29,33,34,35,38,12,39,25,23,26,37,32,36,31,24]

feature_to_use_number=[5,3,6,4,30,29,33,34,35,38,12,39,25,23,26]
#feature_to_use.sort()
category=['nu','no','nu','no','nu','nu','nu','nu','nu','nu','b','nu','nu','nu','nu']
feature_to_use=['src_bytes','service','dst_bytes','flag','diff_srv_rate','same_srv_rate','dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_serror_rate','logged_in','dst_host_srv_serror_rate','serror_rate','count','srv_serror_rate']
normalized=['logged_in','serror_rate','srv_serror_rate','same_srv_rate','diff_srv_rate','dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_serror_rate','dst_host_srv_serror_rate']       #string of normalized features
unnormalized=['src_bytes','dst_bytes','count','dst_host_srv_count']     #unnormalized features represented in strings e.g "count", "srv_count" etc.
#protocol=[]
string_service_bin=['0000001','0000010','0000011','0000100','0000101','0000110','0000111','0001000','0001001','0001010','0001011','0001100','0001101','0001110','0001111','0010000','0010001','0010010','0010011','0010100','0010101','0010110','0010111','0011000','0011001','0011010','0011011','0011100','0011101','0011110','0011111','0100000','0100001','0100010','0100011','0100100','0100101','0100110','0100111','0101000','0101001','0101010','0101011','0101100','0101101','0101110','0101111','0110000','0110001','0110010','0110011','0110100','0110101','0110110','0110111','0111000','0111001','0111010','0111011','0111100','0111101','0111110','0111111','1000000','1000001','1000010','1000011','1000100','1000101','1000110']
service=['aol', 'auth', 'bgp', 'courier', 'csnet_ns', 'ctf', 'daytime', 'discard', 'domain', 'domain_u', 'echo', 'eco_i', 'ecr_i', 'efs', 'exec', 'finger', 'ftp', 'ftp_data', 'gopher', 'harvest', 'hostnames', 'http', 'http_2784', 'http_443', 'http_8001', 'imap4', 'IRC', 'iso_tsap', 'klogin', 'kshell', 'ldap', 'link', 'login', 'mtp', 'name', 'netbios_dgm', 'netbios_ns', 'netbios_ssn', 'netstat', 'nnsp', 'nntp', 'ntp_u', 'other', 'pm_dump', 'pop_2', 'pop_3', 'printer', 'private', 'red_i', 'remote_job', 'rje', 'shell', 'smtp', 'sql_net', 'ssh', 'sunrpc', 'supdup', 'systat', 'telnet', 'tftp_u', 'tim_i', 'time', 'urh_i', 'urp_i', 'uucp', 'uucp_path', 'vmnet', 'whois', 'X11', 'Z39_50']
string_flag_bin=['0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011']
flag=['OTH', 'REJ', 'RSTO', 'RSTOS0', 'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH']

unnormalized_feature_stat={}

def norminal_to_bin(string_service_bin,service):
    m=[]
    final=[]
    for i in string_service_bin:
        for j in i:
            m.append(int(j))
        final.append(m)
        m=[]
    #print final
    k=0
    serv_dic={}

    for i in service:
        serv_dic[i]=final[k]
        k=k+1
    return serv_dic

serv_dic=norminal_to_bin(string_service_bin,service)
flag_dic=norminal_to_bin(string_flag_bin,flag)

def get_type(file1):
    no_of_attributes=1
    attributes=[]
    numeric=[]
    norminal=[]
    binary=[]

    for lines in file1:
        line=lines.strip().split(" ")
        #print line
        if line[0]=='@attribute':
            attributes.append(line[1].strip("'"))

            if line[2]=='real':
                numeric.append(no_of_attributes)
            elif line[2]==("{'0'," or "'1'}"):
                binary.append(no_of_attributes)
            else:
                norminal.append(no_of_attributes)

            no_of_attributes=no_of_attributes+1

        if line[0]=='@data':
            break
    datatypes={'numeric':numeric,'norminal':norminal,'binary':binary}
    return no_of_attributes,attributes,datatypes




def extract_features(file1):
    k=0
    selfset=[]
    nonselfset=[]
    allset=[]
    for lines in file1:
        line=lines.strip().split(" ")

        if line[0]=='@data':
            k=1
            continue
        if k==1:
            m=[]
            t=line[0].split(",")
            L=len(t)
            for i in feature_to_use_number:
                m.append(t[i-1])
            allset.append(m)
            if t[L-1]=="normal":
                selfset.append(m)
            else:
                nonselfset.append(m)

    return selfset, nonselfset,allset

def normalizer(selfset):
    global unnormalized_feature_stat
    for i in unnormalized:
        j=feature_to_use.index(i)

        picked=[]
        for features in selfset:
            picked.append(int(features[j]))

        unnormalized_feature_stat[i]=[min(picked),max(picked)]
    return unnormalized_feature_stat


def norminal_convert(feature,i):
    v=feature_to_use[i]
    flagmax=11
    flagmin=1
    servmax=70
    servmin=1
    if v=='flag':
        newvalue=flag_dic[feature]
        dtvalue=((flag.index(feature)+1)-flagmin)/(float(flagmax-flagmin))
        return newvalue,dtvalue
    if v=='service':
        newvalue=serv_dic[feature]
        dtvalue=((service.index(feature)+1)-servmin)/(float(servmax-servmin))
        return newvalue,dtvalue
def convert_to_binary(num, length=7):
    binary_string_list = list(format(num, '0{}b'.format(length)))
    return [int(digit) for digit in binary_string_list]
def convert_normalized(feature):
    newvalue=(float(feature)) *100
    newvalue=int(round(newvalue,0))
    distvalue=convert_to_binary(newvalue)
    return distvalue

def convert_unnormalized(feature,i,round_off):
    min2,max2=unnormalized_feature_stat[feature_to_use[i]]
    feature=int(round(float(feature),2)) #covert to string to float, then round up to nearest whole no, then convert back to int
    try:
        x=((feature-min2)/(float(max2-min2)))
        return round(x,round_off)
    except:
        return round(0,round_off)


unnormalized_feature_stat={}

def chromosomes(inputset,round_off):
    global unnormalized_feature_stat
    #selfset,nonselfset,allset=extract_features(file1)
    #unnormalized_feature_stat=normalizer(allset)
    global unnormalized_feature_stat
    #print unnormalized_feature_stat
    newfet=[]
    newfetd=[]
    i=0
    #for u in range(0,10):
    #    featureset=selfset[u]

    for featureset in inputset:
        newset=[]
        distchrom=[]
        #print featureset
        for feature in featureset:
            if category[i]=='b':
                newset.append([int(feature)])
                distchrom.append(int(feature))
                i=i+1
            elif category[i]=='no':
                a,b=norminal_convert(feature,i)
                newset.append(a)
                distchrom.append(round(b,round_off))
                i=i+1
            elif category[i]=='nu':
                if feature_to_use[i] in normalized:
                    r=convert_normalized(feature)
                    newset.append(r)
                    distchrom.append(round(float(feature),round_off))
                    i=i+1
                else:
                    if feature_to_use[i]=='count':
                        newset.append(convert_to_binary(int(feature),9))
                    elif feature_to_use[i]=='src_bytes':
                        newset.append(convert_to_binary(int(feature),31))
                    elif feature_to_use[i]=='dst_bytes':
                        newset.append(convert_to_binary(int(feature),31))
                    elif feature_to_use[i]=='dst_host_srv_count':
                        newset.append(convert_to_binary(int(feature),8))
                    distchrom.append(convert_unnormalized(feature,i,round_off))
                    i=i+1
        #print newset
        #print distchrom
        #print "\n\n"
        newfet.append(newset)
        newfetd.append(distchrom)
        i=0
    return  newfet,newfetd

class Ga:

    def __init__(self):
        pass

    def pop(self,self_list,pop_num):
        """

        :param self_list: list of self attributes
        :return: randomly selected population
        """
        try:
            #pop=np.array(random.sample(self_list,pop_num))
            pop=random.sample(self_list,pop_num)
        except ValueError:
            print('Sample size exceeded population size.')
        return pop

    def fitness(self,individual,normal,perc_match):

        """
        [3,4,5],[3,4,6]
        :param individual: the GA individual
        :param normal: the list of self samples
        :param perc_match: an intger 1-100
        :return: the value 0-1
        """
        p=(perc_match/float(100))*len(individual)
        #print "p",p
        #print len(individual)
        perc_num_of_feat=int(round(p,0))
        match=0
        for individuals in normal:
            ans=(individual[0:perc_num_of_feat]==individuals[0:perc_num_of_feat])
            #print individual[0:perc_num_of_feat],individuals[0:perc_num_of_feat]
            if ans==True:
                match=match+1
        p=match/float(len(normal))
        #print "p is ",p
        f=math.exp(-p)
        #print "exp(-f) = ",f
        return f#match/float(len(normal))

    def crossover(self,parent1,parent2,crossover_point,p_crossover):
        """

        :param parent1: first parent with best fitness
        :param parent2: second parent with second best fitness
        :param p_crossover: the probability of crossover
        :return: a child after performing single point crossover
        """
        if random.random()>=p_crossover:
            return parent1
        child=parent1[0:crossover_point]+parent2[crossover_point:]
        return child #np.array(child)

    def mutate(self,child,location,p_mutation,round_off=2,set_to_choose_from=0):
        """

        :param child: the child to be mutated
        :param location: the index of feature to mutate
        :param set_to_choose_from: set containing the range of value to mutate with
        :return: choose a item from the given set range and replace the value at location
        """
        if random.random()<p_mutation:
            child[location]=round(np.random.random(),round_off)
            return child
        else:
            return child



#t=Ga()
#print "GA",t.pop([[1,2],[2,3],[3,3],[4,4],[1,4],[7,6],[1,2],[3,2]],3)
#print "crossover",t.crossover([0,"SF",2,3,4,5,6,7,7],[10,"RT",13,15,17,19,20,17],3)
#print "mutation",t.mutate([0,"SF",2,3,4,5,6,7,7],3,4)

def generate_ga_detectors(num_pop,num_gen,self,p_mutation,p_crossover,round_off=2):
    ga_instance=Ga()

    pop=ga_instance.pop(self,num_pop)
    z=pop
    print "performing GA..."
    print "Initial population"
    print z
    k=0
    for i in range(0,num_gen):
        print "Generation",k
        k=k+1

        for j in range(0,num_pop):
            parent1,parent2=random.sample(pop,2) #np.array(random.sample(pop,2))
            l1=pop.index(parent1)
            l2=pop.index(parent2)
            print "parent1",parent1
            print  "parent2",parent2
            child=ga_instance.crossover(parent1,parent2,3,p_crossover)
            print "cross_child",child
            child=ga_instance.mutate(child,0,p_mutation,round_off)
            print "mutat_child",child

            d1=ais_instance1.euclidean(child,parent1)
            print "d1=",d1
            d2=ais_instance1.euclidean(child,parent2)
            print "d2=",d2
            f=ga_instance.fitness(child,self,90)
            print "f=",f
            f1=ga_instance.fitness(parent1,self,90)
            print "f1=",f1
            f2=ga_instance.fitness(parent2,self,90)
            print "f2=",f2
            if (d1<d2)and(f>f1):
                print "replacing parent1 which child"
                pop[l1]=child
            elif (d2<=d1)and(f>f2):
                print "replacing parent2 which child"
                pop[l2]=child
            print '\n'
    return  pop#print pop1


def test_detector(pop,nselfd,radius=0.0):
    print "actual number =",len(nselfd)
    attack=[]
    #nonattack1=[]
    for value in nselfd:
        #attack=[]
        #nonattack=[]
        for detector in pop:
            d=ais_instance1.euclidean(detector,value)
            if d<=radius:
                attack.append(value)
                break


    print "number classified as attack =",len(attack)
    #print "number classified as nonattack =",len(nonattack)
    return attack#,nonattack
    #return min(mnx),max(mnx)









def main():
    global unnormalized_feature_stat
    selfset,nonselfset,allset=extract_features(file1)
    unnormalized_feature_stat=normalizer(allset)
    print unnormalized_feature_stat
    self,selfd=chromosomes(selfset,2)
    nself,nselfd=chromosomes(nonselfset,2)
    #print selfset[0:2]
    #print"self",self[0:2]
    #print "selfd",selfd[0:2]
    #print "nselfd",nselfd[0:2]
    p_mutation=1.0/len(self[0])
    print "prob of mutation=",p_mutation
    p_crossover=1.0
    print "prob of crossover=",p_crossover
    pop=generate_ga_detectors(500,50,selfd,p_mutation,p_crossover)
    test_detector(pop,nselfd,2.0)


#    ap=[]

#    for i in range(0,10):
#        for x in range(0,10):
#            #print ais_instance1.euclidean(nselfd[0],selfd[i])
#            ap.append(ais_instance1.euclidean(nselfd[i],selfd[x]))
        #print selfd[i]
        #print nselfd[i]
        #print "\n\n"
#        print ap
#    print min(ap),max(ap)

if __name__=="__main__":
    main()
