from statistics import mean
import subprocess
import sys

#directoriesSL = [['../sl_train3','../sl_test3','alphabet size : 3'],['../sl_train10','../sl_test10','alphabet size : 10'],['../sl_train56','../sl_test56', 'alphabet size : 56']]
directoriesSL=[['../sl_train10','../sl_test10','alphabet size : 10']]
#directoriesSP = [['../sp_train3','../sp_test3'],['../sp_train10','../sp_test10'],['../sp_train56','../sp_test56']]
directoriesSP=[['../sp_train3','../sp_test3','alphabet size : 3']]
#SL = ['SL2','SL4','SL8']
SL = ['SL8']
SP = ['SP2','SP4','SP8']
k_chunks = ['1k','10k','100k']
vsize = [10,30,100]
#vsize=[10]

#p = subprocess.Popen('python3 tf.py SL8 1k 30 ../sl_train3 ../sl_test3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#for line in p.stdout.readlines():
#    print(line.decode('utf-8')[:-1])

print('\n\n')

for d in directoriesSL:
    for sl in SL:
        for v in vsize:
            print('==========================================================')
            print('vector size : ', v)
            print(d[2])
            for k in k_chunks:
                s = 'python3 tf.py '+sl+' '+k+' '+str(v)+' '+d[0]+' '+d[1]
                print(s)
                print(sl, str(k))

                test1 = []
                test2 = []
                test1WordLengthAccuracies={}
                test2WordLengthAccuracies={}
                test1WordLengthAccuracies={str(key):[] for key in range(1,26)}
                test2WordLengthAccuracies={str(key):[] for key in range(26,51)}
                for x in range(0,1):
                    p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in p.stdout.readlines():
                        l = line.decode('utf-8')[:-1]
                        #print(l)
                        if 'Test1' in l and 'length' in l:
                            l=l.split(' ')
                            #print(l)
                            l=l[-6:]
                            #print(l)
                            test1WordLengthAccuracies[l[0]].append(float(l[2]))
                            test1WordLengthAccuracies[l[0]].append(float(l[5]))
                        elif 'Test1' in l:
                            l = l.split(' ')
                            l=l[-1:][0]
                            test1.append(float(l))
                        elif 'Test2' in l and 'length' in l:
                            l=l.split(' ')
                            l=l[-6:]
                            test2WordLengthAccuracies[l[0]].append(float(l[2]))
                            test2WordLengthAccuracies[l[0]].append(float(l[5]))
                        elif 'Test2' in l:
                            l = l.split(' ')
                            l=l[-1:][0]
                            test2.append(float(l))
                
                """
                t=''
                for t1 in test1:
                    t+='{0:.4f}'.format(t1)
                    t+=' '
                """
                print('Test1 Accuracies : ',mean(test1))
                """
                t=''
                for t2 in test2:
                    t+='{0:.4f}'.format(t2)
                    t+=' '
                """
                print('Test2 Accuracies : ',mean(test2))

                for x in range(1,51):
                    if str(x) in test1WordLengthAccuracies:
                        """
                        t=''
                        for t1 in test1WordLengthAccuracies[str(x)]:
                            t+='{0:.4f}'.format(t1)
                            t+=' '
                        """
                        #print(str(x))
                        t = test1WordLengthAccuracies[str(x)]
                        #print(test1WordLengthAccuracies)
                        if t != []:
                            print(x, ' ', t[0], ' count=',t[1])
                    if str(x) in test2WordLengthAccuracies:
                        """
                        t=''
                        for t1 in test2WordLengthAccuracies[str(x)]:
                            t+='{0:.4f}'.format(t1)
                            t+=' '
                        """
                        t = test2WordLengthAccuracies[str(x)]
                        if t != []:
                            print(x, ' ', t[0], 'count=', t[1])
                        
        print('\n\n')
