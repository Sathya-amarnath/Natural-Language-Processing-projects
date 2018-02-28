#import numpy library for arrays manipulation, sys for reading external file, re is for regular expression
import numpy as np
import sys
import re
#print the header information
print()
print("University of Central Florida")
print("CAP6640 Spring 2018 - Dr. Glinos")
print()
print("Text Similarity Analysis by Sathya Narayanan Amarnath")

#Open the file, read it and store it in variables seq1 and seq2
inputfile=sys.argv[1]
outputfile=sys.argv[2]
file_input=open(inputfile,'rt')
seq1=file_input.read()
file_output=open(outputfile,'rt')
seq2=file_output.read()
#close the files
file_input.close()
file_output.close()
#printing the source and target file data
print()
print("Source file: "+sys.argv[1])
print("Target file: "+sys.argv[2])

#Tokenization, splitting the strings into list
se1=seq1.split()
se2=seq2.split()
result_seq1=(' '.join(se1))
result_seq2=(' '.join(se2))

#normalization
#converting uppercase to lowercase tokens
norm_1=result_seq1.lower()
norm_2=result_seq2.lower()

#printing the tokens
print()
print("Raw Tokens:")
print("Source > "+norm_1)
print("Target > "+norm_2)

#2nd point:Forward stripping (looking for non alphanumeric characters in the beginning and spliiting it into seperate tokens)
p=re.compile('[a-zA-Z0-9]') 
str1=""
str2=""
for j in range(len(norm_1.split())):
    temp=""
    count=0
    if(p.search(norm_1.split()[j]) and not (p.match(norm_1.split()[j]))):
        
        i=0
        while (p.match(norm_1.split()[j][i])==None):
            temp=temp+norm_1.split()[j][i]
            i=i+1
            count=count+1
        str1=str1+" "+temp+" "+norm_1.split()[j][count:]
    else:
        str1=str1+" "+norm_1.split()[j]

for j in range(len(norm_2.split())):
    temp=""
    count=0
    if(p.search(norm_2.split()[j]) and not (p.match(norm_2.split()[j]))):
        
        i=0
        while (p.match(norm_2.split()[j][i])==None):
            temp=temp+norm_2.split()[j][i]
            i=i+1
            count=count+1
        str2=str2+" "+temp+" "+norm_2.split()[j][count:]
    
    else:
        str2=str2+" "+norm_2.split()[j]
        
#3rd point:Backward stripping (looking for non alphanumeric characters in the end and spliiting it into seperate tokens)
str3=""
str4=""
for j in range(len(str1.split())):
    temp=""
    count=0
    if(p.search(str1.split()[j]) and not (p.match(str1.split()[j],len(str1.split()[j])-1))):
        i=len(str1.split()[j])-1
        
        while (p.match(str1.split()[j][i])==None):
            temp=temp+str1.split()[j][i]
            i=i-1
            count=count+1
            temp=temp[::-1]
        if(temp[0]=="'" or temp[0]=='"'):
            str3=str3+" "+str1.split()[j][0:i+1]+" "+temp[0]+" "+temp[1]
        else:    
            str3=str3+" "+str1.split()[j][0:i+1]+" "+temp
    else:
        if(str1.split()[j].endswith("'s")):
            index=str1.split()[j].find("'")
            temp=temp+str1.split()[j][index:]
            str3=str3+" "+str1.split()[j][0:index]+" "+temp
        elif(str1.split()[j].endswith("n't")):
            index=str1.split()[j].find("n")
            temp=temp+"not"
            str3=str3+" "+str1.split()[j][0:index]+" "+temp
        elif(str1.split()[j].endswith("'m")):
            index=str1.split()[j].find("'")
            temp=temp+"am"
            str3=str3+" "+str1.split()[j][0:index]+" "+temp
        else:    
            str3=str3+" "+str1.split()[j]
        
for j in range(len(str2.split())):
    temp=""
    count=0
    index=0
    if(p.search(str2.split()[j]) and not (p.match(str2.split()[j],len(str2.split()[j])-1))):
        i=len(str2.split()[j])-1
        
        while (p.match(str2.split()[j][i])==None):
            temp=temp+str2.split()[j][i]
            i=i-1
            count=count+1
            temp=temp[::-1]
            
        if(temp[0]=="'" or temp[0]=='"'):
            str4=str4+" "+str2.split()[j][0:i+1]+" "+temp[0]+" "+temp[1]
        
        else:    
            str4=str4+" "+str2.split()[j][0:i+1]+" "+temp
        
    else:
        if(str2.split()[j].endswith("'s")):
            index=str2.split()[j].find("'")
            temp=temp+str2.split()[j][index:]
            str4=str4+" "+str2.split()[j][0:index]+" "+temp
        elif(str2.split()[j].endswith("n't")):
            index=str2.split()[j].find("n")
            temp=temp+"not"
            str4=str4+" "+str2.split()[j][0:index]+" "+temp
        elif(str2.split()[j].endswith("'m")):
            index=str2.split()[j].find("'")
            temp=temp+"am"
            str4=str4+" "+str2.split()[j][0:index]+" "+temp
        else:    
            str4=str4+" "+str2.split()[j]

#printing the normalized tokens
print()
print("Normalized Tokens:")
print("Source > "+str3)
print("Target > "+str4)

#smith waterman algorithm implementation
gap=-1
mismatch=-1
match=2

rows=len(str3.split())+1
cols=len(str4.split())+1

#creating a trace matrix
trace_matrix = np.array([['  ' for col in range(cols)] for row in range(rows)])
#function definitions for calculating score and storing values in trace matrix and score matrix
def calc_score(matrix, x, y):
    similarity = match if str3.split()[x-1] == str4.split()[y-1] else mismatch
    diag_score = matrix[x - 1][y - 1] + similarity
    up_score   = matrix[x - 1][y] + gap
    left_score = matrix[x][y - 1] + gap
    if(diag_score > up_score and diag_score > left_score and diag_score > 0):
        trace_matrix[x][y]="DI"
    elif(up_score >= diag_score and up_score >= left_score and up_score > 0):
        trace_matrix[x][y]="UP"
    elif(left_score >= diag_score and left_score >= up_score and left_score > 0):
        trace_matrix[x][y]="LT"
    else:
        trace_matrix[x][y]=" "
    return max(0,diag_score,up_score,left_score)

def create_score_matrix(rows, cols):
    score_matrix = np.array([[0 for col in range(cols)] for row in range(rows)])
    max_score = 0
    max_pos   = None 
    for i in range(1, rows):
        for j in range(1, cols):
            score = calc_score(score_matrix, i, j)
            
            if score > max_score:
                max_score = score
                max_pos   = (i, j)

            score_matrix[i][j] = score
            

    assert max_pos is not None, 'the x, y position with the highest score was not found'

    return score_matrix, max_pos, max_score
    

# Initialize the scoring matrix.
score_matrix, start_pos, maxi_score = create_score_matrix(rows, cols)

#printing edit distance table
print()
print("Edit Distance Table:")
print()

str5=""
for i in range(len(str4.split())+1):
    str5=str5+"\t"+str(i)
print("\t",str5)

str6=""
for i in range(len(str4.split())+1):
    if(i==0):
        str6=str6+"\t"+"#"
    else:
        if(len(str4.split()[i-1])>3):
            str6=str6+"\t"+str4.split()[i-1][0:3]
        else:
            str6=str6+"\t"+str4.split()[i-1]
print("\t",str6)
            
for i in range(len(score_matrix)):
    if(i==0):
        print(i,end='\t')
        print("#",end='\t')
    else:
        print(i,end='\t')
        if(len(str3.split()[i-1])>3):
            print(str3.split()[i-1][0:3],end='\t')
        else:
            print(str3.split()[i-1],end='\t')

    
    
    for j in range(len(score_matrix[i])):
        
        print(score_matrix[i][j], end='\t')
    print()


#printing trace matrix
print()
print("Backtrace Table:")
print()
str7=""
for i in range(len(str4.split())+1):
    str7=str7+"\t"+str(i)
print("\t",str7)

str8=""
for i in range(len(str4.split())+1):
    if(i==0):
        str8=str8+"\t"+"#"
    else:
        if(len(str4.split()[i-1])>3):
            str8=str8+"\t"+str4.split()[i-1][0:3]
        else:
            str8=str8+"\t"+str4.split()[i-1]
print("\t",str8)
            
for i in range(len(trace_matrix)):
    if(i==0):
        print(i,end='\t')
        print("#",end='\t')
    else:
        print(i,end='\t')
        if(len(str3.split()[i-1])>3):
            print(str3.split()[i-1][0:3],end='\t')
        else:
            print(str3.split()[i-1],end='\t')

    
    
    for j in range(len(trace_matrix[i])):
        
        print(trace_matrix[i][j], end='\t')
    print()
    
#printing maximum value in the edit distance table
print()
print("Maximum value in the distance table: "+str(maxi_score))
print()

ls_max=[]

##for finding the index of maximum score
for i in range(len(score_matrix)):
    for j in range(len(score_matrix[i])):
        if(score_matrix[i][j]==maxi_score):
            ls_max.append(i)
            ls_max.append(j)
    


#for splitting a list 
def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

ls_max_array=split(ls_max,2)

#maximum value in the score matrix
print("Maxima:")
for i in range(len(ls_max_array)):
    print("\t",ls_max_array[i])
    print()
    
print()
    
#finding maximal local alignment and finding insertion, deletion and substitution locations.
def traceback(trace_matrix, start_pos):
    END, DIAG, UP, LEFT = range(4)
    aligned_seq1 = []
    aligned_seq2 = []
    x, y= start_pos
    move= next_move(trace_matrix, x, y)
    while move != END:
        if move == DIAG:
            aligned_seq1.append(str3.split()[x-1])
            aligned_seq2.append(str4.split()[y-1])
            x -= 1
            y -= 1
            
        elif move == UP:
            aligned_seq1.append(str3.split()[x-1])
            aligned_seq2.append('-')
            x -= 1
            
        else:
            aligned_seq1.append('-')
            aligned_seq2.append(str4.split()[y-1])
            y -= 1
            
        move = next_move(trace_matrix, x, y)

    
    aligned_seq1=aligned_seq1[::-1]
    aligned_seq2=aligned_seq2[::-1]
    
    aligned_seq1 = '\t'.join(map(str, aligned_seq1))
    aligned_seq2 = '\t'.join(map(str, aligned_seq2))
    

    ali_array=np.array(['' for i in range(len(aligned_seq1.split()))])
    for j in range(len(aligned_seq1.split())):
        if(aligned_seq1.split()[j]=="-"):
            ali_array[j]='i'
        elif(aligned_seq2.split()[j]=="-"):
            ali_array[j]='d'
        elif(aligned_seq1.split()[j]!=aligned_seq2.split()[j]):
            ali_array[j]='s'
        else:
            ali_array[j]=''
    
    
    return aligned_seq1,aligned_seq2,ali_array,x,y
        

def next_move(trace_matrix, x, y):
    if(trace_matrix[x][y]=="DI"):
        return 1
    elif(trace_matrix[x][y]=="UP"):
        return 2
    elif(trace_matrix[x][y]=="LT"):
        return 3
    else:
        return 0

print()
print("Maximal-similarity alignments:")
print()

#call traceback function
for i in range(len(ls_max_array)):
    
    seq1_aligned, seq2_aligned,ali_array,stop_x,stop_y= traceback(trace_matrix, ls_max_array[i])
    print("Alignment "+str(i)+" ( length "+str(len(seq1_aligned.split()))+" )")
    print()
    print("Source at "+str(stop_x)+" :   " +seq1_aligned)
    print()
    print("target at "+str(stop_y)+" :   " +seq2_aligned)
    print()
    print("Edit action :   ", end="")
    for k in range(len(ali_array)):        
        print(ali_array[k], end="\t")
    print()
    print()



# sum1=0
#                for i in range(len(val)):
#                    sum1=sum1+val[i]
#                for i in range(len(val)):
#                    val[i]=val[i]/sum1
#                
#                print(max(val))
##                Matrix[j][i]=max(val)
    
    
#print(initial_dic)
#print(emi_dict)
#print(trans_final_dict)
#viterbi_tags=[]
#for i in range(len(test_word)):
#    for j in range(len(test_word[i])):
#        print(test_word[i][j]+"    :",end=" ")
#        for key1,key2 in emi_dict:
#            if(key1==test_word[i][j]):
#                print("  "+key2+"  ("+str(emi_dict[key1,key2])+")", end=" ")
#                viterbi_tags.append(key2)
#        print()
##ta=sorted(list(set(viterbi_tags)))
#wor=["time","travel","will","work"]








#x=viterbi(wor,ta)

