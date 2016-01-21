#!/usr/bin/env python
import AIS

file1=open("C:\Users\Obinna\Desktop\NSL-KDD\KDDTrain+.arff")

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

def convert_unnormalized(feature,i):
    min2,max2=unnormalized_feature_stat[feature_to_use[i]]
    feature=int(round(float(feature),2)) #covert to string to float, then round up to nearest whole no, then convert back to int
    try:
        x=((feature-min2)/(float(max2-min2)))
        return x
    except:
        return 0


unnormalized_feature_stat={}

def chromosomes(inputset):
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
                distchrom.append(b)
                i=i+1
            elif category[i]=='nu':
                if feature_to_use[i] in normalized:
                    r=convert_normalized(feature)
                    newset.append(r)
                    distchrom.append(float(feature))
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
                    distchrom.append(convert_unnormalized(feature,i))
                    i=i+1
        #print newset
        #print distchrom
        #print "\n\n"
        newfet.append(newset)
        newfetd.append(distchrom)
        i=0
    return  newfet,newfetd


def main():
    global unnormalized_feature_stat
    selfset,nonselfset,allset=extract_features(file1)
    unnormalized_feature_stat=normalizer(allset)
    print unnormalized_feature_stat
    self,selfd=chromosomes(selfset)
    nself,nselfd=chromosomes(nonselfset)
    ap=[]
    ais_instance1=AIS.Ais()
    for i in range(0,10):
        for x in range(0,10):
            #print ais_instance1.euclidean(nselfd[0],selfd[i])
            ap.append(ais_instance1.euclidean(nselfd[i],selfd[x]))
        #print selfd[i]
        #print nselfd[i]
        #print "\n\n"
        print ap
    print min(ap),max(ap)







    #g=[3.558064122327236e-07, 0.2463768115942029, 0.0, 0.9, 0.0, 1.0, 0.09803921568627451, 0.17, 0.03, 0.0, 0, 0.0, 0.0, 0.003913894324853229, 0.0]
    #t=[1.0579987003254102e-07, 0.6086956521739131, 0.0, 0.9, 0.15, 0.08, 0.00392156862745098, 0.0, 0.6, 0.0, 0, 0.0, 0.0, 0.025440313111545987, 0.0]
    #print ais_instance1.euclidean(g,t)
        #print newfetd
        #print newfet
    #for u in range(0,10):
     #   featureset=selfset[u]
      #  print










   #print len(selfset)
    #print len(nonselfset)
    #print selfset
    #print nonselfset

#'service':['0000001','0000010','0000011','0000100','0000101','0000110','0000111','0001000','0001001','0001010','0001011','0001100','0001101','0001110','0001111','0010000','0010001','0010010','0010011','0010100','0010101','0010110','0010111','0011000','0011001','0011010','0011011','0011100','0011101','0011110','0011111','0100000','0100001','0100010','0100011','0100100','0100101','0100110','0100111','0101000','0101001','0101010','0101011','0101100','0101101','0101110','0101111','0110000','0110001','0110010','0110011','0110100','0110101','0110110','0110111','0111000','0111001','0111010','0111011','0111100','0111101','0111110','0111111','1000000','1000001','1000010','1000011','1000100','1000101','1000110'],'flag':['0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011']
#{'duration':[0,42862,305.054,2686.556],'protocol_type':['00','01','1,0'],'service':['0000001','0000010','0000011','0000100','0000101','0000110','0000111','0001000','0001001','0001010','0001011','0001100','0001101','0001110','0001111','0010000','0010001','0010010','0010011','0010100','0010101','0010110','0010111','0011000','0011001','0011010','0011011','0011100','0011101','0011110','0011111','0100000','0100001','0100010','0100011','0100100','0100101','0100110','0100111','0101000','0101001','0101010','0101011','0101100','0101101','0101110','0101111','0110000','0110001','0110010','0110011','0110100','0110101','0110110','0110111','0111000','0111001','0111010','0111011','0111100','0111101','0111110','0111111','1000000','1000001','1000010','1000011','1000100','1000101','1000110'],'flag':['0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011'],'src_bytes':[0,381709090,24330.628,2410805.402],'dst_bytes':[0,5151385,3491.847,88830.718],'land':['0','1'],'wrong_fragment':[0,3,0.024,0.26],'urgent':[0,1,0,0.006],'hot':[0,77,0.198,2.154],'num_failed_logins':[0,4,0.001,0.045],'logged_in':['0','1'],'num_compromised':[0,884,0.228,10.417],'root_shell':['0','1'],'su_attempted':[0,2,0.001,0.049],'num_root':[0,975,0.25,11.501],'num_file_creations':[0,40,0.015,0.53],'num_shells':[0,1,0,0.019],'num_access_files':[0,8,0.004,0.099],'num_outbound_cmds':[0,0,0,0],'is_host_login':['0','1'],'is_guest_login':['0','1'],'count':[1,511,84.591,114.673],'srv_count':[1,511,27.699,72.468],'dst_host_count':[0,255,182.532,98.994],'dst_host_srv_count':[0,255,115.063,110.647]}

if __name__=="__main__":
    main()