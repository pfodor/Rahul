import rstr
from itertools import product
import sys
import os
import random
import math
import re
import string
################################# HELPER FUNCTIONS ############################

def forbiddenChecker(word, posORneg, checkForbidden):
    if posORneg == "POS":
        return checkForbidden(word)
    if posORneg == "NEG":
        return not checkForbidden(word)


#This Function checks if a word is forbidden in SP2

def checkForbiddenSP2(word):
    forbidden = False
    if re.search(".*".join("ab"), word):
        return True
    return False

#This Function checks if a word is forbidden in SP4

def checkForbiddenSP4(word):
    forbidden = False
    if re.search(".*".join("abba"), word):
        return True
    return False

#This Function checks if a word is forbidden in SP8

def checkForbiddenSP8(word):
    forbidden = False
    if re.search(".*".join("abbaabba"), word):
        return True
    return False

############################### GENERATE SP FUNCTIONS #########################

def generateSPPositive(alphabet, sampleAmount, checkForbidden, minWordLength, maxWordLength):
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
            print(word, x, maxWordLength,len(samplePerLength), sampleAmount)        
        if len(samplePerLength) == sampleAmount:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples

##########################################################################
########################NEGATIVE SAMPLES##################################
##########################################################################

def generateSPNegativeWord(alphabet, sSize, p, checkForbidden):
    s=''
    chosen = False
    while not chosen:
        r = random.choice(p)
        x= sSize-len(r)
        if x >= 0:
            chosen = True
    l=list(r)
    while len(l)<sSize:
        c = random.choice(list(alphabet))
        l.insert(random.randint(0,len(l)),c)
    s=''.join(l)
    forbidden = checkForbidden(s)
    if forbidden:
        return s
    else:
        print(s, 'error')
        sys.exit()


def generateSPNegative(alphabet, minWordLength, maxWordLength, sampleAmount, checkForbidden, p):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    x = minWordLength 
    while x < maxWordLength+1:
        word = generateSPNegativeWord(alphabet, x,p, checkForbidden)
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
            print(word, len(word), 'generateSPNegative', checkForbidden)
        if len(samplePerLength) == sampleAmount:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples



########################### WRITE TRAINING DATA ###############################

def writeTrainingData(trainDir,sp, alphabet,x):
    tSP = "./"+trainDir+"/Training_"+sp+"_positive.txt"
    f=open(tSP, "w")
    f.seek(0)

    tSP = "./"+trainDir+"/Training_"+sp+"_negative.txt"
    f1=open(tSP, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]

    if sp == "SP2":
        trainingPos = generateSPPositive(alphabet, x, checkForbiddenSP2, 1, 25)
        trainingNeg = generateSPNegative(alphabet, 2, 25, x, checkForbiddenSP2, ['ab'])
    elif sp =="SP4":
        trainingPos = generateSPPositive(alphabet, x, checkForbiddenSP4, 1, 25)
        trainingNeg = generateSPNegative(alphabet, 4, 25, x, checkForbiddenSP4, ['abba'])
    else:
        trainingPos = generateSPPositive(alphabet, x, checkForbiddenSP8, 1, 25)
        trainingNeg = generateSPNegative(alphabet, 8, 25, x, checkForbiddenSP8, ['abbaabba'])

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f1.write(x)
        f1.write('\n')
    f.close()
    f1.close()
    return (trainingPos, trainingNeg)

##########################GENERATE TEST 1######################################
def generateSPTest1(alphabet,trainingSP, sampleAmount, posORneg, checkForbidden,m,p):
    samples = []
    if posORneg == 'POS':
        for t in range(1,m):
            if allCombos[t] == None:
                allCombos[t] = [''.join(x) for x in product(alphabet, repeat = t)]
            unknown = [k for k in allCombos[t] if k not in trainingSP]
            print("generateSLTest1","--1--","t== ",t,"    ",m)
            for x in unknown:
                if len(x) == t:
                    if not forbiddenChecker(x, posORneg, checkForbidden):
                        samplePerLength = []
                        while len(samplePerLength)<sampleAmount:
                            word = random.choice(unknown)
                            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                            if not forbidden:
                                if word not in trainingSP:
                                    print(x, len(x),word, posORneg, "generateSPTest1",checkForbidden)
                                    samplePerLength.append(word)
                                    samples+=samplePerLength
                        break
        for t in range(m,26):
            samplePerLength=[]
            while len(samplePerLength)<sampleAmount:
                word = rstr.rstr(alphabet, t)
                forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                if not forbidden:
                    if word not in trainingSP:
                        samplePerLength.append(word)
                        found = True
                        print(word, len(word), len(samplePerLength), sampleAmount, posORneg, "generateSPTest1",checkForbidden)
                #else:
                    #print(word, posORneg, "generateSLTest1", checkForbidden, "didn't make it")
            samples+=samplePerLength
        extraSamples = []
        while len(extraSamples) < sampleAmount*10:
            word = rstr.rstr(alphabet, 25)
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSP:
                    extraSamples.append(word)
                    print(word, posORneg, "generateSPTest1",checkForbidden)
            #else:
                #print(word, posORneg, "generateSLTest1", checkForbidden, "didn't make it")
        samples+=extraSamples

    if posORneg == 'NEG':
        x=0
        if checkForbidden == checkForbiddenSP2:
            x=3
        elif checkForbidden == checkForbiddenSP4:
            x=5
        else:
            x=9
        for t in range(x,26):
            o=[]
            z=''
            samplePerLength = []
            if t==(x):
                for y in trainingSP:
                    if len(y) == t:
                        if y not in o:
                            o.append(y)
                j=len(alphabet)*len(p[0])
                if len(o) != j:
                    b=[]
                    for a in alphabet:
                        for q in range(len(p)):
                            b.append(p[0][0:q]+a+p[0][q:])
                        b.append(p[0]+a)
                    unique = [c for c in b if c not in o]
                    while len(samplePerLength) < sampleAmount:
                        z = random.choice(unique)
                        samplePerLength.append(z)
                        print(z, len(z), len(samplePerLength), sampleAmount, posORneg, "generateSPTest1",checkForbidden)
                    samples+=samplePerLength
            else:
                while len(samplePerLength)<sampleAmount:
                    word=generateSPNegativeWord(alphabet, t,p, checkForbidden)
                    forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                    if not forbidden:
                        if word not in trainingSP:
                            samplePerLength.append(word)
                            found = True
                            print(word, len(word), len(samplePerLength), sampleAmount, posORneg, "generateSPTest1",checkForbidden)
            samples+=samplePerLength
        extraSamples=[]
        while len(extraSamples) < sampleAmount*10:
            word=generateSPNegativeWord(alphabet, 25,p, checkForbidden)
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSP:
                    extraSamples.append(word)
                    print(word, posORneg, "generateSPTest1",checkForbidden)
            #else:
                #print(word, posORneg, "generateSLTest1", checkForbidden, "didn't make it")
        samples+=extraSamples
    return samples



##########################GENERATE TEST 2######################################



############################# WRITE TEST DATA #################################


def writeTest1data(testDir,sp,alphabet,x):
    tSP = "./"+testDir+"/test1_"+sp+"_positive.txt"
    f1=open(tSP, "w")
    f1.seek(0)

    tSP = "./"+testDir+"/test1_"+sp+"_negative.txt"
    f2=open(tSP, "w")
    f2.seek(0)
    
    trainingPos=[]
    trainingNeg=[]
    negSamples = []
    m = 3
    if sp == "SP2":            
        trainingPos = generateSPTest1(alphabet,trainingPosSP2, x, 'POS', checkForbiddenSP2,m,['ab'])
        trainingNeg = generateSPTest1(alphabet,trainingNegSP2, x, 'NEG', checkForbiddenSP2,m,['ab'])
    elif sp =="SP4":        
        trainingPos = generateSPTest1(alphabet,trainingPosSP4, x, 'POS', checkForbiddenSP4,m,['abba'])
        trainingNeg = generateSPTest1(alphabet,trainingNegSP4, x, 'NEG', checkForbiddenSP4,m,['abba'])
    else:
        trainingPos = generateSPTest1(alphabet,trainingPosSP8, x, 'POS', checkForbiddenSP8,m,['abbaabba'])
        trainingNeg = generateSPTest1(alphabet,trainingNegSP8, x, 'NEG', checkForbiddenSP8,m,['abbaabba'])

    for x in trainingPos:
        f1.write(x)
        f1.write('\n')
    for x in trainingNeg:
        f2.write(x)
        f2.write('\n')

    f1.close()
    f2.close()
    return (trainingPos, trainingNeg)


def writeTest2data(testDir,sp,alphabet,x):
    tSP = "./"+testDir+"/test2_"+sp+"_positive.txt"
    f=open(tSP, "w")
    f.seek(0) 

    tSP = "./"+testDir+"/test2_"+sp+"_negative.txt"
    f1=open(tSP, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]
    print("start test2 data")
    if sp == "SP2":
        trainingPos = generateSPPositive(alphabet, x, checkForbiddenSP2, 26, 50)
        trainingNeg = generateSPNegative(alphabet, 26, 50, x, checkForbiddenSP2,['ab'])
    elif sp =="SP4":
        print("start sp4 test2 data")
        trainingPos = generateSPPositive(alphabet, x, checkForbiddenSP4, 26, 50)
        trainingNeg = generateSPNegative(alphabet, 26, 50, x, checkForbiddenSP4, ['abba'])
    else:
        print("start sp8 test2 data")
        trainingPos = generateSPPositive(alphabet, x, checkForbiddenSP8, 26, 50)
        trainingNeg = generateSPNegative(alphabet, 26, 50, x, checkForbiddenSP8, ['abbaabba'])

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

############################################################################
######################### CREATE TRAINING SETS #############################
############################################################################

aSize=int(aSize)
alphabet=string.ascii_letters+string.digits
r=aSize-len(alphabet)
point = 161
for x in range(r):
    alphabet+=chr(point)
    point+=1

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
    
    tset = writeTrainingData(trainDir,"SP2", alphabet, x)
    trainingPosSP2 = tset[0]
    trainingNegSP2 = tset[1]

    tset = writeTrainingData(trainDir,"SP4", alphabet, x)
    trainingPosSP4 = tset[0]
    trainingNegSP4 = tset[1]

    tset = writeTrainingData(trainDir,"SP8", alphabet, x)
    trainingPosSP8 = tset[0]
    trainingNegSP8 = tset[1]


    ############################################################################
    ######################### CREATE TEST SETS #################################
    ############################################################################

    #########################   TEST 1  ######################################
    allCombos = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

    negSamples = []

    test1setSP2 = writeTest1data(testDir,"SP2",alphabet,x)
    test1PosSP2 = test1setSP2[0]
    test1NegSP2 = test1setSP2[1]

    test1setSP4 = writeTest1data(testDir,"SP4",alphabet,x)
    test1PosSP4 = test1setSP4[0]
    test1NegSP4 = test1setSP4[1]

    test1setSP8 = writeTest1data(testDir,"SP8",alphabet,x)
    test1PosSP8 = test1setSP8[0]
    test1NegSP8 = test1setSP8[1]

    #########################   TEST 2  ######################################
    
    test2setSP2 = writeTest2data(testDir,"SP2", alphabet,x)
    test2PosSP2 = test2setSP2[0]
    test2NegSP2 = test2setSP2[1]
    
    test2setSP4 = writeTest2data(testDir,"SP4", alphabet,x)
    test2PosSP4 = test2setSP4[0]
    test2NegSP4 = test2setSP4[1]
    
    test2setSP8 = writeTest2data(testDir,"SP8", alphabet,x)
    test2PosSP8 = test2setSP8[0]
    test2NegSP8 = test2setSP8[1]
