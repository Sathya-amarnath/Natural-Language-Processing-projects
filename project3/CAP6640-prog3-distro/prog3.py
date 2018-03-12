#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 23:09:40 2018

@author: sathyanarayanan
"""
import numpy as np
import sys
print()
print("University of Central Florida")
print("CAP6640 Spring 2018 - Dr. Glinos")
print("Dependency Parser by Sathya Narayanan Amarnath")
print()
print("Corpus Statistics:")
print()
#read a file
corpusfile="wsj-clean.txt"
file_open=open(corpusfile,'r')
lines=file_open.read()

sentences=lines.split("\n\n")

#test file
testfile=sys.argv[1]
test_file_open=open(testfile,'r')
test_line=test_file_open.read()


print("     # sentences  : "+str(len(sentences)))

index_number=[]
tokens=[]
tags=[]
index_num_of_head=[]
for i in range(len(sentences)):
    index_number.append(sentences[i].split()[0::4])
    tokens.append(sentences[i].split()[1::4])
    tags.append(sentences[i].split()[2::4])
    index_num_of_head.append(sentences[i].split()[3::4])

#token_arr=np.array([np.array(xi) for xi in tokens])   
#print(str(tokens).count(",")+1)

#print(str(tokens))


def recursive_len(item):
    if type(item) == list:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1

print("     # tokens     : "+str(recursive_len(tokens)))
      

import itertools, collections

print("     # POS tags   : "+str(len(collections.Counter(itertools.chain(*tags)))))


      
#print(index_number[0])
#print(tokens[0])
#print(tags[0])
#print(index_num_of_head[0])
#
for i in range(len(index_number)):
    index_number[i]=list(map(int, index_number[i]))
    index_num_of_head[i]=list(map(int, index_num_of_head[i]))

left_arc={}
right_arc={}

for i in range(len(tags)):
    for j in range(len(tags[i])):
        x=0
        
        if(index_num_of_head[i][j]!=0 and index_number[i][j] < index_num_of_head[i][j]):
            key1=tags[i][j]
            x=index_num_of_head[i][j]-1
            key2=tags[i][x]
            if((key1,key2) in left_arc.keys()):
                left_arc[key1,key2]=left_arc[key1,key2]+1
            else:
                left_arc[key1,key2]=1
        elif(index_num_of_head[i][j]!=0 and index_number[i][j] > index_num_of_head[i][j]):
            key1=tags[i][j]
            x=index_num_of_head[i][j]-1
            key2=tags[i][x]
            if((key1,key2) in right_arc.keys()):
                right_arc[key1,key2]=right_arc[key1,key2]+1
            else:
                right_arc[key1,key2]=1
                

import collections
left_arc = collections.OrderedDict(sorted(left_arc.items()))

right_arc=collections.OrderedDict(sorted(right_arc.items()))

print("     # Left-Arcs  : "+str(sum(left_arc.values())))

print("     # Right-Arcs : "+str(sum(right_arc.values())))
      
print("     # Root-Arcs  : "+str(len(sentences)))

print()      
print()

print("Left Arc Array Nonzero Counts:")
print()


#for key1,key2 in left_arc:
sorted_tags=list(collections.Counter(itertools.chain(*tags)))
sorted_tags=sorted(sorted_tags)
#print(x)
for i in range(len(sorted_tags)):
    print(sorted_tags[i]+":",end=" ")
    for key1,key2 in left_arc:
        if(key1==sorted_tags[i]):
            print("[  "+key2+",  "+str(left_arc[key1,key2])+"]", end=" ")
    print()
    

print()
print("Right Arc Array Nonzero Counts:")
print()
for i in range(len(sorted_tags)):
    print(sorted_tags[i]+":",end=" ")
    for key1,key2 in right_arc:
        if(key1==sorted_tags[i]):
            print("[  "+key2+",  "+str(right_arc[key1,key2])+"]", end=" ")
    print()

print()
print("Arc Confusion Array:")
print()
#$ : [   CD, 237,   3]
#left_arc_set = set(left_arc)
#right_arc_set = set(right_arc)
#
##c=0
#for key1,key2 in left_arc_set.intersection(right_arc_set):
##    c=c+1
#    print(dict(left_arc_set[key1,key2]))


confusion_arc={}
for k1,k2 in left_arc:
    if(k1,k2) in right_arc:
        confusion_arc[k1,k2]=left_arc[k1,k2],right_arc[k1,k2]
        

#
#print(confusion_arc)
from collections import defaultdict
target_dict = defaultdict(dict)
for keys1,keys2 in confusion_arc:
    target_dict[keys1][keys2]=confusion_arc[keys1,keys2]
      
for i in range(len(sorted_tags)):
    print(sorted_tags[i]+":",end=" ")
    if(sorted_tags[i] not in target_dict):
        print(" ")
    else:
        for key in target_dict[sorted_tags[i]]:
            print("[  "+key+",  "+str(target_dict[sorted_tags[i]][key][0])+",  "+str(target_dict[sorted_tags[i]][key][1])+"]", end=" ")
        print()

print()
print("      Number of confusing arcs = "+str(len(confusion_arc)))
   
#developing the oracle
print()
print()
print("Input Sentence:")
test_line1=test_line.split("\n")
for i in range(len(test_line1)):
    print(test_line1[i], end=" ")
print()
print()
print()
print("Parsing Actions and Transitions:")
print()
#building the parser
test_line2=[]
test_line1=test_line1[:-1]
for i in range(len(test_line1)):
    test_line2.append(test_line1[i].split("/"))

flat_list = [item for sublist in test_line2 for item in sublist]
list_tokens=[]
list_tags=[]
for i in range(len(flat_list)):
    if(i%2==0):
        list_tokens.append(flat_list[i])
    else:
        list_tags.append(flat_list[i])

#buffer
buffer=list(test_line1)
#stack
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop_top(self):
         return self.items.pop()
     
     def pop_second(self):
         return self.items.pop(-2)

     def peek_top(self):
         return self.items[len(self.items)-1]
    
     def peek_second(self):
         return self.items[len(self.items)-2]

     def size(self):
         return len(self.items)
     
     def stack(self):
         return self.items
     
s=Stack()


print("[]",end=" ")
print("[ ",end=" ")
print(*test_line1, sep=', ',end=" ")
print("]",end=" ")
print("SHIFT")
s.push(buffer.pop(0))

print("[ "+s.peek_top()+"]",end=" ")
print("[ ",end=" ")
print(*buffer,sep=', ',end=" ")
print("] SHIFT")
s.push(buffer.pop(0))

while(not s.isEmpty()):
    x1=""
    x2=""
    seperator="/"
    
    if(s.size()==1 and len(buffer)==0):
        print("[ "+str(*s.stack())+"] [] ROOT --> "+str(*s.stack()))
        s.pop_top()
    else:
        x1=x1+s.peek_top()
        x2=x2+s.peek_second()
        i=x2[x2.index(seperator) + len(seperator):]
        j=x1[x1.index(seperator) + len(seperator):]
        if((i.startswith("V") and j.startswith(".") and s.size()>=2) or (i.startswith("V") and j.startswith("R") and s.size()>=2)):
            print("[ ",end=" ")
            print(*s.stack(),sep=",",end=" ")
            print("]",end=" ")
            print("[ ",end=" ")
            print(*buffer,sep=', ',end=" ")
            print("] Right-Arc: "+s.peek_second()+" --> "+s.peek_top())
            s.pop_top()
        elif(s.size()>2 and i.startswith("I") and j.startswith(".")):
            print("[ ",end=" ")
            print(*s.stack(),sep=",",end=" ")
            print("]",end=" ")
            print("[ ",end=" ")
            print(*buffer,sep=', ',end=" ")
            print("] SWAP")
            s.pop_second()
            buffer=[x2]+buffer
        elif(len(buffer)!=0 and (i.startswith("V") or i.startswith("I")) and (j.startswith("D") or j.startswith("I") or j.startswith("J") or j.startswith("P") or j.startswith("R"))):
            print("[ ",end=" ")
            print(*s.stack(),sep=",",end=" ")
            print("]",end=" ")
            print("[ ",end=" ")
            print(*buffer,sep=', ',end=" ")
            print("] SHIFT")
            s.push(buffer.pop(0))
        else:
            k=i,j
            if(s.size()>=2 and (k in left_arc and k not in confusion_arc)):
                print("[ ",end=" ")
                print(*s.stack(),sep=",",end=" ")
                print("]",end=" ")
                print("[ ",end=" ")
                print(*buffer,sep=', ',end=" ")
                print("] Left-Arc: "+s.peek_second()+" <-- "+s.peek_top())
                s.pop_second()
            elif(s.size()>=2 and (k in right_arc and k not in confusion_arc)):
                print("[ ",end=" ")
                print(*s.stack(),sep=",",end=" ")
                print("]",end=" ")
                print("[ ",end=" ")
                print(*buffer,sep=', ',end=" ")
                print("] Right-Arc: "+s.peek_second()+" --> "+s.peek_top())
                s.pop_top()
            elif(s.size()>=2 and (k in confusion_arc)):
                ma=max(confusion_arc[k][0],confusion_arc[k][1])
                if(ma==confusion_arc[k][0]):
                    print("[ ",end=" ")
                    print(*s.stack(),sep=",",end=" ")
                    print("]",end=" ")
                    print("[ ",end=" ")
                    print(*buffer,sep=', ',end=" ")
                    print("] Left-Arc: "+s.peek_second()+" <-- "+s.peek_top())
                    s.pop_second()
                else:
                    print("[ ",end=" ")
                    print(*s.stack(),sep=",",end=" ")
                    print("]",end=" ")
                    print("[ ",end=" ")
                    print(*buffer,sep=', ',end=" ")
                    print("] Right-Arc: "+s.peek_second()+" --> "+s.peek_top())
                    s.pop_top()
            else:
                print("[ ",end=" ")
                print(*s.stack(),sep=",",end=" ")
                print("]",end=" ")
                print("[ ",end=" ")
                print(*buffer,sep=', ',end=" ")
                print("] SHIFT")
                s.push(buffer.pop(0))
                
            



            
            







