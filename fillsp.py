import os
import sys

sp_dirs = [x for x in os.listdir('./') if 'sp_' in x]
#print(sp_dirs)
#sys.exit()
t=[]
for x in sp_dirs:
    t+=[x+j for j in ['/1k','/10k','/100k']]
#print(t)
sp_dirs=t

for x in sp_dirs:
    count = 0
    if '1k' in x:
        count = 500
    elif '10k' in x:
        count = 5000
    elif '100k' in x:
        count = 50000
    else:
        print('error')
        sys.exit()

    files = [x+'/'+j for j in os.listdir(x) if 'negative' in j]
    for f in files:
        rf = open(f, 'r')
        actualCount = 0
        for l in rf:
            actualCount+=1
        rf.close()
        wf = open(f,'a')
        appendCount = count-actualCount
        if appendCount > 0:
            string=''
            if 'SP2' in f:
                string='ab\n'
            elif 'SP4' in f:
                string='abba\n'
            elif 'SP8' in f:
                string='abbaabba\n'
            else:
                print('error')
                sys.exit()
            for i in range(appendCount):
                wf.write(string)
            wf.close()
        
