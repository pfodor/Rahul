from statistics import mean
import subprocess
import sys

sl_train = sys.argv[1]
sl_test = sys.argv[2]
sp_train = sys.argv[3]
sp_test = sys.argv[4]
combineDirectory = sys.argv[5]

SL = ['SL2','SL4','SL8']
SP = ['SP2','SP4','SP8']
dataSizes = ['1k','10k','100k']

for ds in dataSizes:
    for sl in SL:
        s= 'mkdir -p '+ combineDirectory+'/SL/'+sl+'/'+ds+'/'
        print(s)
        p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s = 'cp ~/rahul/Rahul/'+sl_test+'/'+ds+'/*'+sl+'* '+ combineDirectory+'/SL/'+sl+'/'+ds+'/'
        print(s)
        p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s = 'cp ~/rahul/Rahul/'+sl_train+'/'+ds+'/*'+sl+'* '+ combineDirectory+'/SL/'+sl+'/'+ds+'/'
        print(s)
        p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

for ds in dataSizes:
    for sp in SP:
        s= 'mkdir -p '+ combineDirectory+'/SP/'+sp+'/'+ds+'/'
        print(s)
        p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s = 'cp ~/rahul/Rahul/'+sp_test+'/'+ds+'/*'+sp+'* '+ combineDirectory+'/SP/'+sp+'/'+ds+'/'
        print(s)
        p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s = 'cp ~/rahul/Rahul/'+sp_train+'/'+ds+'/*'+sp+'* '+ combineDirectory+'/SP/'+sp+'/'+ds+'/'
        print(s)
        p = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
