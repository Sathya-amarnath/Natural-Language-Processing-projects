#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 18:36:57 2018

@author: sathyanarayanan
"""
import numpy as np
import sys
print()
print("University of Central Florida")
print("CAP6640 Spring 2018 - Dr. Glinos")
print()
print("Viterbi Algorithm HMM Tagger by Sathya Narayanan Amarnath")
print()
print("All Tags Observed:")
print()

#read a file
inputfile=sys.argv[1]
file_open=open(inputfile,'r')
lines=file_open.read()

#read a test file
input_test_file=sys.argv[2]
file_open_test=open(input_test_file,'r')
sentence_test=file_open_test.read()

sentences=lines.split("\n\n")
sentences=sentences[:-1]

sample_tag=[]
sample_words=[]
for i in range(len(sentences)):
    sample_tag.append(sentences[i].split()[1::2])
    sample_words.append(sentences[i].split()[0::2])

word=np.array([np.array(xi) for xi in sample_words])    

tag=np.array([np.array(xi) for xi in sample_tag])

tags=[]
words=[]
for i in range(len(sentences)):
    tags.append(' '.join(sample_tag[i]))

#unique
tags_unique = []
for i in sample_tag:
    tags_unique += i

distinct_tag = list(set(tags_unique))
#sorting it
sorted_distinct_tag=sorted(distinct_tag)
#printing it
for i in range(len(sorted_distinct_tag)):
    print(i+1, end="\t")
    print(sorted_distinct_tag[i])
    
print()
print("Initial Distribution:")
print()

#create a dictionary
dict_tag_count={}
for i in range(len(tag)):
    for j in range(len(tag[i])):
        k=tag[i][j]
        if(k in dict_tag_count.keys()):
            dict_tag_count[k]=dict_tag_count[k]+1
        else:
            dict_tag_count[k]=1
            
#calculate initial prob
initial_prob=[]
for i in range(len(sorted_distinct_tag)):
    count=0
    val=0
    for j in range(len(tags)):
        if(tags[j].split()[0]==sorted_distinct_tag[i]):
            count=count+1
    val=count/len(tags)
    initial_prob.append(val)
    
initial_dic={}
    
for i in range(len(sorted_distinct_tag)):
    if(initial_prob[i]==0.0):
        continue
    print("start [ "+ sorted_distinct_tag[i]+" |  ] "+str(round(initial_prob[i], 6)))

    

for i in range(len(sorted_distinct_tag)):
    key1=sorted_distinct_tag[i]
    key2=" "
    initial_dic[key1,key2]=round(initial_prob[i], 6)
    
    


print()
print("Emission Probabilities:")
print()

for i in range(len(word)):
    for j in range(len(word[i])):
        
        word[i][j]=word[i][j].lower()
        
        if(word[i][j].endswith("sses") or word[i][j].endswith("xes")):
            word[i][j]=word[i][j][:-2]
            
        elif(word[i][j].endswith("ses") or word[i][j].endswith("zes")):
            word[i][j]=word[i][j][:-1]
            
        elif(word[i][j].endswith("ches") or word[i][j].endswith("shes")):
            word[i][j]=word[i][j][:-2]
            
        elif(word[i][j].endswith("men")):
            word[i][j]=word[i][j][:-2]+"an"
            
        elif(word[i][j].endswith("ies")):
            word[i][j]=word[i][j][:-3]+"y"
            
            
#dictionary for emission
dict_emission={}
for i in range(len(word)):
    for j in range(len(word[i])):
        
        k=word[i][j],tag[i][j]
        if(k in dict_emission.keys()):
            dict_emission[k]=dict_emission[k]+1
        else:
            dict_emission[k]=1
            
#sorting the dictionary
import collections
ordered_dict=collections.OrderedDict(sorted(dict_emission.items()))

emi_dict={}
for key1,key2 in ordered_dict:
    
    prob='{0:.6f}'.format(round(ordered_dict[key1,key2]/dict_tag_count[key2],6))
    print('{:>15}  {:>15}  {:>15}'.format(key1,key2,str(prob)))
    emi_dict[key1,key2]=float(prob)
    



print()
print("Transition Probabilities:")
print()
#create another dictionary
dict_trans={}
for i in range(len(tag)):
    j=0
    k=1
    while(j<=len(tag[i])-2 and k<=len(tag[i])-1):
        

        l=tag[i][j],tag[i][k]
            
        if(l in dict_trans.keys()):
            dict_trans[l]=dict_trans[l]+1
        else:
            dict_trans[l]=1
        j+=1
        k+=1
        
    
ordered_dict_trans=collections.OrderedDict(sorted(dict_trans.items()))

trans_final_dict={}
for i in range(len(sorted_distinct_tag)):
    if(initial_prob[i]==0.0):
        continue

    key1=sorted_distinct_tag[i]
    key2=" "
    trans_final_dict[key1,key2]='{0:.6f}'.format(round(initial_prob[i], 6))



for key1,key2 in ordered_dict_trans:
    prob='{0:.6f}'.format(round(ordered_dict_trans[key1,key2]/dict_tag_count[key1],6))

    trans_final_dict[key2,key1]=prob


for i in range(len(sorted_distinct_tag)):
    count=0
    val=0
    for j in range(len(tags)):
        if(tags[j].split()[-1]==sorted_distinct_tag[i]):
            count=count+1
    val=round(count/len(tags),6)
    if(val!=0):
        key1=" "
        key2=sorted_distinct_tag[i]
        trans_final_dict[key1,key2]='{0:.6f}'.format(round(val, 6))
    

for key in trans_final_dict:
    trans_final_dict[key]=float(trans_final_dict[key])



sum=0
for key1,key2 in trans_final_dict:
    if (key2.isspace()):
        sum=sum+trans_final_dict[key1,key2]

print("["+str(sum)+"]",end=" ")

for key1,key2 in trans_final_dict:
    if(key2.isspace()):
            print("["+key1+"|"+key2+"] "+str(trans_final_dict[key1,key2]), end=" ")
print()            

total_list=[]
for i in range(len(sorted_distinct_tag)):
    total=0
    for key1,key2 in trans_final_dict:
        if(key2==sorted_distinct_tag[i]):
           total=round(total+trans_final_dict[key1,key2],4)
    total_list.append(total)


for i in range(len(sorted_distinct_tag)):
    print("["+str(total_list[i])+"]",end=" ")
    for key1,key2 in trans_final_dict:
        if(key2==sorted_distinct_tag[i]):
            print("["+key1+"|"+key2+"] "+str(trans_final_dict[key1,key2]), end=" ")
    print()


li=[]
for i in range(len(word)):
    li.append(word[i].tolist())


lexical = []
for i in li:
    lexical += i
    


print()
print("Corpus Features:")
print()
print("Total # tags        : "+str(len(sorted_distinct_tag)))
print("Total # bigrams     : "+str(len(trans_final_dict)))
print("Total # lexicals    : "+str(len(set(lexical))))
print("Total # sentences   : "+str(len(word)))      

print()
print()
print("Test Set Tokens Found in Corpus:")


print()

test_sentences=sentence_test.split("\n")
test_sentences=test_sentences[:-1]

for i in range(len(test_sentences)):
    test_sentences[i]=test_sentences[i].lower()

sample_test_list=[]
for i in range(len(test_sentences)):
    sample_test_list.append(test_sentences[i].split())

def viterbi(wor,ta):
    
    Matrix = np.zeros((len(ta)+2, len(wor)))
    Backtrace=[]
    for row in range(len(ta)):
        Backtrace += [[0]*len(wor)]
    sum=0
    for i in range(0,len(ta)):
        key1=wor[0]
        key2=ta[i]
        l=key1,key2
        if(l in emi_dict.keys()):
            sum=sum+(initial_dic[ta[i]," "] * emi_dict[key1,key2])
            Matrix[i][0]=initial_dic[ta[i]," "] * emi_dict[key1,key2]
            
        else:
            Matrix[i][0]=0
    for i in range(len(ta)):
        Matrix[i][0]=Matrix[i][0]/sum
    
    print("Iteration  1 : "+wor[0]+" : ",end=" ")
    for i in range(len(ta)):
        if(Matrix[i][0]!=0):
            print(ta[i]+" ( "+ '{0:.6f}'.format(Matrix[i][0])+", null)", end=" ")
    print()
#        
    for i in range(1,len(wor)):
        sum1=0
        for j in range(len(ta)):
            key1=wor[i]
            key2=ta[j]
            l=key1,key2
            if(l in emi_dict.keys()):
                result_array = np.array([])

                for k in range(len(ta)):
                    if(Matrix[k][i-1]!=0):
                        k1=ta[j]
                        k2=ta[k]
                        m=k1,k2
                        if(m in trans_final_dict.keys()):
                            result_array=np.append(result_array,float(Matrix[k][i-1]*trans_final_dict[k1,k2]*emi_dict[key1,key2]))
                        else:
                            result_array=np.append(result_array,float(Matrix[k][i-1]*0.0001*emi_dict[key1,key2]))
                Matrix[j][i]=np.amax(result_array)               
                ind=np.argmax(result_array)
                counter=-1
                for q in range(len(ta)):
                    if(Matrix[q][i-1]!=0):
                        counter+=1
                        if(counter==ind):
                            Backtrace[j][i]=ta[q] 
                        
                            
                               
        for x in range(len(ta)):
            sum1=sum1+Matrix[x][i]
        for y in range(len(ta)):
            Matrix[y][i]=Matrix[y][i]/sum1
                
                 
    for r1 in range(1,len(wor)):
        print("Iteration  "+str(r1+1)+" : "+wor[r1]+" :",end=" ")
        
        for r2 in range(len(ta)):
            if(Matrix[r2][r1]!=0):
                print(ta[r2] +"("+'{0:.6f}'.format(Matrix[r2][r1])+","+str(Backtrace[r2][r1])+")", end=" ")
        print()        
            

    print()    
    print()
    print("Viterbi Tagger Output:")
    print()
    max_val=np.max(Matrix,axis=0)
    for i in range(len(wor)):
        for j in range(len(ta)):
            if(Matrix[j][i]==max_val[i]):
                print("\t\t"+wor[i]+"\t"+ta[j])
        
    
    return Matrix

#        
for i in range(len(sample_test_list)):
    viterbi_tags=[]

    for j in range(len(sample_test_list[i])):
        
         
            print(sample_test_list[i][j]+"  :",end=" ")
            
                
            for key1,key2 in emi_dict:
                if(key1==sample_test_list[i][j]):
                    print("  "+key2+"  ("+'{0:.6f}'.format((emi_dict[key1,key2]))+")",end=" ")
                    viterbi_tags.append(key2)
                
            print()
    ta=sorted(list(set(viterbi_tags)))
    
    print()
    print()
    print("Intermediate Results of Viterbi Algorithm:")
    print()       
    x=viterbi(sample_test_list[i],ta)            
    

