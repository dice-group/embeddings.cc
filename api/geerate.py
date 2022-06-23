
import numpy as np
 
import random
import numpy as np


def random_int_list(start, stop, length):

    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))

    length = int(abs(length)) if length else 0

    random_list = []

    for i in range(length):

        random_list.append(random.randint(start, stop))

    return random_list

a=['http://example.com/Another_similarity_tes', [3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 0.0, 1.1, 2.2]],
a="['http://example.com/test"

i=0
finalout=[]

with open('/Users/ljymacbook/Downloads/index_test', 'w') as fa:
    while i<10000:
     numlist=random_int_list(1,100,10)
    # if (i-10==0):
     out="http://example.com/test"+str(i)

     #for i in range(rows):
     finalout.append([])
      
     finalout[i].append(out)     
     finalout[i].append(numlist)
     i=i+1
   # print(finalout)  
     
    # else:
     # out="['http://example.com/test"+str(i)+"',"+str(numlist)+"],"
     #finalout.append(out)
     #finalout2.append(str(numlist))

    #matrix = [[m for m in rang[finalout])] for n in finalout2]
    #matrix = [[finalout[i-1]] for n in finalout2[i-1]]
    fa.writelines(str(finalout))





with open('/Users/ljymacbook/Downloads/index_test', 'r') as f:
  lines = f.read()
  # line=lines.strip(',')

   
    
    
   
print(lines)   



