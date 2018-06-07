#this file combines the data files created by Rahul's programs on compute4 system to match the format of the jh_repo


import sys
import random

#print(sys.argv)
pf = open(sys.argv[1], 'r')
nf = open(sys.argv[2], 'r')
wf = open(sys.argv[3],'w+')
cutoff=int(sys.argv[4])

inputList=[]
for l in pf:
    x = l.strip()
    x = x + '\tTRUE\n'
    inputList.append(x)

inputList=inputList[:cutoff]
random.shuffle(inputList)

for x in inputList:
    wf.write(x)

inputList=[]
for l in nf:
    x = l.strip()
    x = x + '\tFALSE\n'
    inputList.append(x)

inputList=inputList[:cutoff]
random.shuffle(inputList)

for x in inputList:
    wf.write(x)


pf.close()
nf.close()
wf.close()

