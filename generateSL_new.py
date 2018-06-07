

import string
import rstr
from itertools import product
import sys
import os
import random
import math
#################################HELPER FUNCTIONS ############################

#This Function checks if a word is forbidden in SL2

def forbiddenChecker(word, posORneg, checkForbidden):
    if posORneg == "POS":
        return checkForbidden(word)
    if posORneg == "NEG":
        return not checkForbidden(word)

def checkForbiddenSL2(word):
    forbidden = False
    if(word[0] == 'b'):
        forbidden = True
    elif "aa" in word:
        forbidden = True
    elif "bb" in word:
        forbidden = True
    elif word[-1:] == "a":
        forbidden = True
    return forbidden

#This Function checks if a word is forbidden in SL4

def checkForbiddenSL4(word):
    forbidden = False
    if(word[0:3] == 'bbb'):
        forbidden = True
    elif "aaaa" in word:
        forbidden = True
    elif "bbbb" in word:
        forbidden = True
    elif word[-3:] == "aaa":
        forbidden = True
    return forbidden

#This Function checks if a word is forbidden in SL8

def checkForbiddenSL8(word):
    forbidden = False
    if(word[0:7] == 'bbbbbbb'):
        forbidden = True
    elif "aaaaaaaa" in word:
        forbidden = True
    elif "bbbbbbbb" in word:
        forbidden = True
    elif word[-7:] == "aaaaaaa":
        forbidden = True
    return forbidden

def findPartition(n,length):
    x=0
    partitions = []
    t=length
    y=0
    while len(partitions) < n-1:
        if t!=0:
            y = random.randint(0,t)
            t=t-y
            x+=y
            partitions.append(y)
        if t==0:
            break
    if x!= length:
        if t!=0:
            partitions.append(length-x)
    if t==0:
        while len(partitions)<n:
            partitions.append(0)
    return partitions


############################### GENERATE SL FUNCTIONS #########################

def generateSLPositive(alphabet, sampleAmount, checkForbidden, minWordLength, maxWordLength):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = minWordLength
    while x < maxWordLength+1:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if not forbidden:
            samplePerLength.append(word)
            print(word, len(word), 'generateSLPositive')
        if len(samplePerLength) == sampleAmount:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples



##########################################################################
######################## NEGATIVE SAMPLES ##################################
##########################################################################

def generateSLNegativeWord(alphabet, sSize,p, checkForbidden):
    s=''
    chosen = False
    while not chosen:
        r = random.choice(p)
        x= sSize-len(r)
        if x >= 0:
            chosen = True
    word = rstr.rstr(alphabet,x)
    if r==p[0]:
        s+=r
        s+=word
    elif r==p[3]:
        s+=word
        s+=r
    else:
        if len(word) == 0:
            s=r
        else:
            l=list(word)
            l.insert(random.randint(0,len(l)),r)
            s=''.join(l)
    forbidden = checkForbidden(s)
    if forbidden:
        return s
    else:
        print(s, 'error')
        sys.exit()

def generateSLNegative(alphabet, minWordLength, maxWordLength, sampleAmount, checkForbidden, p):
    negSamples = []
    samplePerLength = []
    x = minWordLength 
    while x < maxWordLength+1:
        word = generateSLNegativeWord(alphabet, x,p, checkForbidden)
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
            print(word, len(word), 'generateSLNegative', checkForbidden)
        if len(samplePerLength) == sampleAmount:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

############################## WRITE TRAINING DATA ##########################

def writeTrainingData(trainDir,sl, alphabet, x):
    tSL = "./"+trainDir+"/Training_"+sl+"_positive.txt"
    f=open(tSL, "w")
    f.seek(0)

    tSL = "./"+trainDir+"/Training_"+sl+"_negative.txt"
    f1=open(tSL, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSLPositive(alphabet, x, checkForbiddenSL2, 1, 25)
        trainingNeg = generateSLNegative(alphabet, 1, 25, x, checkForbiddenSL2, ['b','aa','bb','a'])
    elif sl =="SL4":
        trainingPos = generateSLPositive(alphabet, x, checkForbiddenSL4, 1, 25)
        trainingNeg = generateSLNegative(alphabet, 3, 25, x, checkForbiddenSL4, ['bbb','aaaa','bbbb','aaa'])
    else:
        trainingPos = generateSLPositive(alphabet, x, checkForbiddenSL8, 1, 25)
        trainingNeg = generateSLNegative(alphabet, 7, 25, x, checkForbiddenSL8, ['bbbbbbb','aaaaaaaa','bbbbbbbb','aaaaaaa'])
    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f1.write(x)
        f1.write('\n')

    f.close()
    f1.close()
    return (trainingPos, trainingNeg)

################################# GENERATE TEST 1 ########################

def generateSLTest1(alphabet,trainingSL, sampleAmount, posORneg, checkForbidden,m,p):
    samples = []
    if posORneg == 'POS':
        for t in range(1,m):
            if allCombos[t] == None:
                allCombos[t] = [''.join(x) for x in product(alphabet, repeat = t)]
            unknown = [k for k in allCombos[t] if k not in trainingSL]
            print("generateSLTest1","--1--","t== ",t,"    ",m)
            for x in unknown:
                if len(x) == t:
                    if not forbiddenChecker(x, posORneg, checkForbidden):
                        samplePerLength = []
                        while len(samplePerLength)<sampleAmount:
                            word = random.choice(unknown)
                            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                            if not forbidden:
                                if word not in trainingSL:
                                    print(x, len(x),word, posORneg, "generateSLTest1",checkForbidden)
                                    samplePerLength.append(word)
                        samples+=samplePerLength
                        break
        for t in range(m,26):
            samplePerLength=[]
            while len(samplePerLength)<sampleAmount:
                word = rstr.rstr(alphabet, t)
                forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                if not forbidden:
                    if word not in trainingSL:
                        samplePerLength.append(word)
                        found = True
                        print(word, len(word), len(samplePerLength), sampleAmount, posORneg, "generateSLTest1",checkForbidden)
                #else:
                    #print(word, posORneg, "generateSLTest1", checkForbidden, "didn't make it")
            samples+=samplePerLength
        extraSamples = []
        while len(extraSamples) < sampleAmount*10:
            word = rstr.rstr(alphabet, 25)
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSL:
                    extraSamples.append(word)
                    print(word, posORneg, "generateSLTest1",checkForbidden)
            #else:
                #print(word, posORneg, "generateSLTest1", checkForbidden, "didn't make it")
        samples+=extraSamples

    if posORneg == 'NEG':
        x=0
        if checkForbidden == checkForbiddenSL2:
            x=1
        elif checkForbidden == checkForbiddenSL4:
            x=3
        else:
            x=7
        for t in range(x,26):
            o=[]
            z=''
            samplePerLength = []
            if t==x:
                for y in trainingSL:
                    if len(y) == t:
                        if y not in o:
                            o.append(y)
                if len(o) != 2:
                    if p[0] not in o:
                        z=p[0]
                    elif p[3] not in o:
                        z=p[3]
                    else:
                        print('error', o, p, t)
                        sys.exit()
                    while len(samplePerLength) < sampleAmount:
                        if z == '':
                            print(p)
                            print(o)
                            sys.exit()
                        samplePerLength.append(z)
                        print(p, p[0], p[3], o)
                        print(z, len(z), len(samplePerLength), sampleAmount, posORneg, "generateSLTest1",checkForbidden)
                    samples+=samplePerLength
            elif t==(x+1):
                for y in trainingSL:
                    if len(y) == t:
                        if y not in o:
                            o.append(y)
                j=len(alphabet)*2
                if x == 1:
                    j=j-1
                #j=j+2
                if len(o) != j:
                    """
                    if p[0] not in o:
                        z=p[0]
                    elif p[3] not in o:
                        z=p[3]
                    else:
                        print('error', t)
                        sys.exit()
                    """
                    b=[]
                    for a in alphabet:
                        if p[0]+a not in b:
                            b.append(p[0]+a)
                        if a+p[3] not in b:
                            b.append(a+p[3])
                    if p[1] not in b:
                        b.append(p[1])
                    if p[2] not in b:
                        b.append(p[2])
                    print('o == ' , o)
                    unique = [c for c in b if c not in o]
                    while len(samplePerLength) < sampleAmount:
                        z = random.choice(unique)
                        samplePerLength.append(z)
                        print(z, len(z), len(samplePerLength), sampleAmount, posORneg, "generateSLTest1",checkForbidden)
                    samples+=samplePerLength
            else:
                while len(samplePerLength)<sampleAmount:
                    word=generateSLNegativeWord(alphabet, t,p, checkForbidden)
                    forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                    if not forbidden:
                        if word not in trainingSL:
                            samplePerLength.append(word)
                            found = True
                            print(word, len(word), len(samplePerLength), sampleAmount, posORneg, "generateSLTest1",checkForbidden)
            samples+=samplePerLength
        extraSamples=[]
        while len(extraSamples) < sampleAmount*10:
            word=generateSLNegativeWord(alphabet, 25,p, checkForbidden)
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSL:
                    extraSamples.append(word)
                    print(word, posORneg, "generateSLTest1",checkForbidden)
            #else:
                #print(word, posORneg, "generateSLTest1", checkForbidden, "didn't make it")
        samples+=extraSamples
    return samples

############################## WRITE TEST DATA ################################

def writeTest1data(testDir,sl,alphabet,x):
    tSL = "./"+testDir+"/test1_"+sl+"_positive.txt"
    f=open(tSL, "w")
    f.seek(0)

    tSL = "./"+testDir+"/test1_"+sl+"_negative.txt"
    f1=open(tSL, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]
    m = 3
    if sl == "SL2":
        trainingPos = generateSLTest1(alphabet,trainingPosSL2, x, 'POS', checkForbiddenSL2,m,['b','aa','bb','a'])
        trainingNeg = generateSLTest1(alphabet,trainingNegSL2, x, 'NEG', checkForbiddenSL2,m,['b','aa','bb','a'])
    elif sl =="SL4":
        trainingPos = generateSLTest1(alphabet,trainingPosSL4, x, 'POS', checkForbiddenSL4,m,['bbb','aaaa','bbbb','aaa'])
        trainingNeg = generateSLTest1(alphabet,trainingNegSL4, x, 'NEG', checkForbiddenSL4,m,['bbb','aaaa','bbbb','aaa'])
    else:
        trainingPos = generateSLTest1(alphabet,trainingPosSL8, x, 'POS', checkForbiddenSL8,m,['bbbbbbb','aaaaaaaa','bbbbbbbb','aaaaaaa'])
        trainingNeg = generateSLTest1(alphabet,trainingNegSL8, x, 'NEG', checkForbiddenSL8,m,['bbbbbbb','aaaaaaaa','bbbbbbbb','aaaaaaa'])

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f1.write(x)
        f1.write('\n')

    f.close()
    f1.close()
    return (trainingPos, trainingNeg)


def writeTest2data(testDir, sl,alphabet,x):
    tSL = "./"+testDir+"/test2_"+sl+"_positive.txt"
    f=open(tSL, "w")
    f.seek(0)
    tSL = "./"+testDir+"/test2_"+sl+"_negative.txt"
    f1=open(tSL, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSLPositive(alphabet, x, checkForbiddenSL2, 26, 50)
        trainingNeg = generateSLNegative(alphabet, 26, 50, x, checkForbiddenSL2,['b','aa','bb','a'])
    elif sl =="SL4":
        trainingPos = generateSLPositive(alphabet, x, checkForbiddenSL4, 26, 50)
        trainingNeg = generateSLNegative(alphabet, 26, 50, x, checkForbiddenSL4,['bbb','aaaa','bbbb','aaa'])
    else:
        trainingPos = generateSLPositive(alphabet, x, checkForbiddenSL8, 26, 50)
        trainingNeg = generateSLNegative(alphabet, 26, 50, x, checkForbiddenSL8,['bbbbbbb','aaaaaaaa','bbbbbbbb','aaaaaaa'])

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f1.write(x)
        f1.write('\n')

    f.close()
    f1.close()
    return (trainingPos, trainingNeg)



##############################################################################
##############################################################################
if __name__ == "__main__":
    aSize=sys.argv[1]
    trainDirOrig=sys.argv[2]
    testDirOrig=sys.argv[3]
    if not os.path.exists(trainDirOrig):
        os.makedirs(trainDirOrig)
    if not os.path.exists(testDirOrig):
        os.makedirs(testDirOrig)


#########################################################################
######################### CREATE TRAINING SETS ##########################
#########################################################################

aSize=int(aSize)
alphabet=string.ascii_letters+string.digits
alphabet=alphabet.replace('0','')
r=aSize-len(alphabet)
point = 161
for x in range(r):
    alphabet+=chr(point)
    point+=1
tempAlpha=''
if aSize<=len(alphabet):
    for a in alphabet:
        if len(tempAlpha)<aSize:
            tempAlpha+=a
        else:
            break
    alphabet = tempAlpha

    
sampleSizes = [20,200,2000]

for x in sampleSizes:

    i = x * 25 * 2
    i = int(i / 1000)
    trainDir = trainDirOrig
    testDir = testDirOrig
    trainDir +='/'+str(i)+'k'
    testDir +='/'+str(i)+'k'

    if not os.path.exists(trainDir):
        os.makedirs(trainDir)
    if not os.path.exists(testDir):
        os.makedirs(testDir)
    
    tset = writeTrainingData(trainDir, "SL2", alphabet,x)
    trainingPosSL2 = tset[0]
    trainingNegSL2 = tset[1]
    
    tset = writeTrainingData(trainDir, "SL4", alphabet,x)
    trainingPosSL4 = tset[0]
    trainingNegSL4 = tset[1]
    
    tset = writeTrainingData(trainDir, "SL8", alphabet,x)
    trainingPosSL8 = tset[0]
    trainingNegSL8 = tset[1]
    
    ##########################################################################
    ######################### CREATE TEST SETS #################################
    ##########################################################################

    #########################   TEST 1  ######################################
    allCombos = [None,None,None,None,None,None,None,None,None,None,None,None,None,None]
    
    test1setSL2 = writeTest1data(testDir, "SL2",alphabet,x)
    test1PosSL2 = test1setSL2[0]
    test1NegSL2 = test1setSL2[1]
    
    test1setSL4 = writeTest1data(testDir, "SL4",alphabet,x)
    test1PosSL4 = test1setSL4[0]
    test1NegSL4 = test1setSL4[1]
    
    test1setSL8 = writeTest1data(testDir, "SL8",alphabet,x)
    test1PosSL8 = test1setSL8[0]
    test1NegSL8 = test1setSL8[1]
    
    #########################   TEST 2  ######################################
    
    test2setSL2 = writeTest2data(testDir, "SL2", alphabet,x)
    test2PosSL2 = test2setSL2[0]
    test2NegSL2 = test2setSL2[1]

    test2setSL4 = writeTest2data(testDir, "SL4", alphabet,x)
    test2PosSL4 = test2setSL4[0]
    test2NegSL4 = test2setSL4[1]

    test2setSL8 = writeTest2data(testDir, "SL8", alphabet,x)
    test2PosSL8 = test2setSL8[0]
    test2NegSL8 = test2setSL8[1]
    
