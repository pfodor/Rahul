import subprocess
import sys

directoriesSL = [['../sl_train3','../sl_test3','alphabet size : 3'],['../sl_train10','../sl_test10','alphabet size : 10'],['../sl_train56','../sl_test56', 'alphabet size : 56']]
directoriesSP = [['../sp_train3','../sp_test3'],['../sp_train10','../sp_test10'],['../sp_train56','../sp_test56']]
SL = ['SL2','SL4','SL8']
SP= ['SP2','SP4','SP8']
k_chunks = ['1k']
vsize = [10,30,100]

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
                print(sl, str(k))

                test1 = []
                test2 = []
                
                for x in range(0,10):
                    p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in p.stdout.readlines():
                        l = line.decode('utf-8')[:-1]
                        if 'Test1' in l:
                            l = l.split(' ')
                            l=l[-1:][0]
                            test1.append(float(l))
                        if 'Test2' in l:
                            l = l.split(' ')
                            l=l[-1:][0]
                            test2.append(float(l))
                
                t=''
                for t1 in test1:
                    t+='{0:.4f}'.format(t1)
                    t+=' '
                print('Test1 Accuracies : ',t)
                t=''
                for t2 in test2:
                    t+='{0:.4f}'.format(t2)
                    t+=' '
                print('Test2 Accuracies : ',t)
                #print(d[3])
        print('\n\n')
