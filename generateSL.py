

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

def generateSL8neg(alphabet, x):
    allCombos = [''.join(x) for x in product(alphabet, repeat = x)]
    ret = []
    for x in allCombos:
        if not checkForbiddenSL8(x):
            ret.append(x)
    return ret

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
            print(word, len(word))
        if len(samplePerLength) == sampleAmount:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples


##########################################################################
######################## NEGATIVE SAMPLES ##################################
##########################################################################

def generateSLNegative(alphabet, minWordLength, maxWordLength, sampleAmount, checkForbidden):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    while len(samplePerLength)<(sampleAmount*minWordLength):
        word = rstr.rstr(alphabet,minWordLength)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
    x = minWordLength+1
    negSamples+=samplePerLength
    samplePerLength = []
    while x < maxWordLength+1:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == sampleAmount:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

def generateSL4_8Negative(alphabet, minWordLength, maxWordLength, sampleAmount, checkForbidden, testOrTrain):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    regTemplate = ""
    if checkForbidden == checkForbiddenSL4:
        regTemplate = '(bbb[alphabet]{})'+ '|' +'([alphabet]{}aaaa[alphabet]{})'+ '|' +'([alphabet]{}bbbb[alphabet]{})'+ '|' +'([alphabet]{}aaa)'
    if checkForbidden == checkForbiddenSL8:
        regTemplate = '(bbbbbbb[alphabet]{})'+ '|' +'([alphabet]{}aaaaaaaa[alphabet]{})'+ '|' +'([alphabet]{}bbbbbbbb[alphabet]{})'+ '|' +'([alphabet]{}aaaaaaa)'
    regTemplate = regTemplate.replace('alphabet',alphabet)
    partitions=[]
    x = 0
    if testOrTrain == "train":
        while len(samplePerLength)<(sampleAmount*minWordLength):
            regMod=""
            if checkForbidden == checkForbiddenSL8:
                regMod =  '(bbbbbbb)'+ '|' + '(aaaaaaa)'
            if checkForbidden == checkForbiddenSL4:
                regMod = '(bbb)|(aaa)'
            word = rstr.xeger(regMod)
            # check if word is forbidden
            forbidden = checkForbidden(word)
            if forbidden:
                samplePerLength.append(word)
                print(word, len(word), testOrTrain)
        x = minWordLength+1
    else:
        x = minWordLength
    negSamples+=samplePerLength
    samplePerLength = []
    while x < maxWordLength+1:
        partitions = []
        if checkForbidden == checkForbiddenSL4:
            partitions += findPartition(1,x-3)
            partitions += findPartition(2,x-4)
            partitions += findPartition(2,x-4)
            partitions += findPartition(1,x-3)
        if checkForbidden == checkForbiddenSL8:
            partitions += findPartition(1,x-7)
            partitions += findPartition(2,x-8)
            partitions += findPartition(2,x-8)
            partitions += findPartition(1,x-7)
        regMod = regTemplate
        for e in partitions:
            rep = "{"+str(e)+"}"
            regMod=regMod.replace("{}",rep,1)
        word = rstr.xeger(regMod)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
            print(word, len(word), testOrTrain)
        if len(samplePerLength) == sampleAmount:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

############################## WRITE TRAINING DATA ##########################

def writeTrainingData(trainDir,sl, alphabet):
    tSL = "./"+trainDir+"/Training_"+sl+"_positive.txt"
    f=open(tSL, "w")
    f.seek(0)

    tSL = "./"+trainDir+"/Training_"+sl+"_negative.txt"
    f1=open(tSL, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSLPositive(alphabet, 20, checkForbiddenSL2, 1, 25)
        trainingNeg = generateSLNegative(alphabet, 1, 25, 20, checkForbiddenSL2)
    elif sl =="SL4":
        trainingPos = generateSLPositive(alphabet, 200, checkForbiddenSL4, 1, 25)
        trainingNeg = generateSL4_8Negative(alphabet, 3, 25, 200, checkForbiddenSL4, "train")
    else:
        trainingPos = generateSLPositive(alphabet, 2000, checkForbiddenSL8, 1, 25)
        trainingNeg = generateSL4_8Negative(alphabet, 7, 25, 2000, checkForbiddenSL8, "train")
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

def generateSLTest1(alphabet, trainingSL, sampleAmount, posORneg, checkForbidden, m):
    samples=[]
    #m = int(math.log(sampleAmount, len(alphabet))+4)
    print("generateSLTest1",posORneg, sampleAmount,checkForbidden)
    for t in range(1,m):
        print("generateSLTest1","--1--","t== ",t,"    ",m)
        if allCombos[t] == None:
            allCombos[t] = [''.join(x) for x in product(alphabet, repeat = t)]
        print("generateSLTest1","--2--","t== ",t,"    ",m)
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
    for t in range(m, 26):
        samplePerLength = []
        found = False
        collect = []
        while len(samplePerLength)<sampleAmount:
            word = rstr.rstr(alphabet, t)
            if (checkForbidden == checkForbiddenSL4) and (posORneg == 'NEG'):
                partitions = []
                regex = '(bbb[alphabet]{})'+ '|' +'([alphabet]{}aaaa[alphabet]{})'+ '|' +'([alphabet]{}bbbb[alphabet]{})'+ '|' +'([alphabet]{}aaa)'
                regex = regex.replace("alphabet", alphabet)
                partitions += findPartition(1,t-3)
                partitions += findPartition(2,t-4)
                partitions += findPartition(2,t-4)
                partitions += findPartition(1,t-3)
                for e in partitions:
                    rep = "{"+str(e)+"}"
                    regex=regex.replace("{}",rep,1)
                word = rstr.xeger(regex)
            if (checkForbidden == checkForbiddenSL8) and (posORneg == 'NEG'):
                if t<7:
                    break
                if t == 7:
                    two = []
                    for tw in trainingSL:
                        if len(tw) == t:
                            if tw not in two:
                                two.append(tw)
                    if len(two) == 2:
                        break
                    regex =  '(bbbbbbb)'+ '|' + '(aaaaaaa)'
                    word = rstr.xeger(regex)
                possible = False
                num = math.pow(len(alphabet), t-7)
                num += math.pow(len(alphabet), t-8)
                num += math.pow(len(alphabet), t-8)
                num += math.pow(len(alphabet), t-7)
                num = num - (int(math.pow(len(alphabet), t-8))*2)
                num = int(num)
                p = []
                if num <= sampleAmount:
                    possible = True
                if possible and (not found):
                    for o in trainingSL:
                            if len(o) == t:
                                if o not in p:
                                    p.append(o)
                    if len(collect) == num and (not found):
                            print(num, len(collect))
                            collect = []
                            break
                if t > 8:
                    partitions = []
                    regex = '(bbbbbbb[alphabet]{})'+ '|' +'([alphabet]{}aaaaaaaa[alphabet]{})'+ '|' +'([alphabet]{}bbbbbbbb[alphabet]{})'+ '|' +'([alphabet]{}aaaaaaa)'
                    regex = regex.replace("alphabet", alphabet)
                    partitions += findPartition(1,t-7)
                    partitions += findPartition(2,t-8)
                    partitions += findPartition(2,t-8)
                    partitions += findPartition(1,t-7)
                    for e in partitions:
                        rep = "{"+str(e)+"}"
                        regex=regex.replace("{}",rep,1)
                    word = rstr.xeger(regex)
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSL:
                    samplePerLength.append(word)
                    found = True
                    print(word, len(word), len(samplePerLength), sampleAmount, posORneg, "generateSLTest1",checkForbidden)
            collect.append(word)
        samples+=samplePerLength

    #add extra samples
    extraSamples = []
    while len(extraSamples) < sampleAmount*10:
        word = rstr.rstr(alphabet, 25)
        # check if word is forbidden
        if (checkForbidden == checkForbiddenSL4) and (posORneg == 'NEG'):
            partitions = []
            regex = '(bbb[alphabet]{})'+ '|' +'([alphabet]{}aaaa[alphabet]{})'+ '|' +'([alphabet]{}bbbb[alphabet]{})'+ '|' +'([alphabet]{}aaa)'
            regex = regex.replace("alphabet", alphabet)
            partitions += findPartition(1,t-3)
            partitions += findPartition(2,t-4)
            partitions += findPartition(2,t-4)
            partitions += findPartition(1,t-3)
            for e in partitions:
                rep = "{"+str(e)+"}"
                regex=regex.replace("{}",rep,1)
            word = rstr.xeger(regex)
        if (checkForbidden == checkForbiddenSL8) and (posORneg == 'NEG'):
            partitions = []
            regex = '(bbbbbbb[alphabet]{})'+ '|' +'([alphabet]{}aaaaaaaa[alphabet]{})'+ '|' +'([alphabet]{}bbbbbbbb[alphabet]{})'+ '|' +'([alphabet]{}aaaaaaa)'
            regex = regex.replace("alphabet", alphabet)
            partitions += findPartition(1,25-7)
            partitions += findPartition(2,25-8)
            partitions += findPartition(2,25-8)
            partitions += findPartition(1,25-7)
            for e in partitions:
                rep = "{"+str(e)+"}"
                regex=regex.replace("{}",rep,1)
            word = rstr.xeger(regex)
        forbidden = forbiddenChecker(word, posORneg, checkForbidden)
        if not forbidden:
            if word not in trainingSL:
                extraSamples.append(word)
                print(word, posORneg, "generateSLTest1",checkForbidden)
    samples+=extraSamples
    return samples

############################## WRITE TEST DATA ################################

def writeTest1data(testDir,sl,alphabet):
    tSL = "./"+testDir+"/test1_"+sl+"_positive.txt"
    f=open(tSL, "w")
    f.seek(0)

    tSL = "./"+testDir+"/test1_"+sl+"_negative.txt"
    f1=open(tSL, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]
    m = 0
    if len(alphabet) <= 10:
        m = 7
    else:
        m = 4
    if sl == "SL2":
        trainingPos = generateSLTest1(alphabet,trainingPosSL2, 20, 'POS', checkForbiddenSL2,m)
        trainingNeg = generateSLTest1(alphabet,trainingNegSL2, 20, 'NEG', checkForbiddenSL2,m)
    elif sl =="SL4":
        if len(alphabet) > 10:
            m = 5
        trainingPos = generateSLTest1(alphabet,trainingPosSL4, 200, 'POS', checkForbiddenSL4,m)
        trainingNeg = generateSLTest1(alphabet,trainingNegSL4, 200, 'NEG', checkForbiddenSL4,m)
    else:
        trainingPos = generateSLTest1(alphabet,trainingPosSL8, 2000, 'POS', checkForbiddenSL8,m)
        trainingNeg = generateSLTest1(alphabet,trainingNegSL8, 2000, 'NEG', checkForbiddenSL8,m)

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f1.write(x)
        f1.write('\n')

    f.close()
    f1.close()
    return (trainingPos, trainingNeg)


def writeTest2data(testDir, sl,alphabet):
    tSL = "./"+testDir+"/test2_"+sl+"_positive.txt"
    f=open(tSL, "w")
    f.seek(0)
    tSL = "./"+testDir+"/test2_"+sl+"_negative.txt"
    f1=open(tSL, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSLPositive(alphabet, 20, checkForbiddenSL2, 26, 50)
        trainingNeg = generateSLNegative(alphabet, 26, 50, 20, checkForbiddenSL2)
    elif sl =="SL4":
        trainingPos = generateSLPositive(alphabet, 200, checkForbiddenSL4, 26, 50)
        trainingNeg = generateSL4_8Negative(alphabet, 26, 50, 200, checkForbiddenSL4, "test")
    else:
        trainingPos = generateSLPositive(alphabet, 2000, checkForbiddenSL8, 26, 50)
        trainingNeg = generateSL4_8Negative(alphabet, 26, 50, 2000, checkForbiddenSL8, "test")

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
    alphabet=sys.argv[1]
    trainDir=sys.argv[2]
    testDir=sys.argv[3]
    if not os.path.exists(trainDir):
        os.makedirs(trainDir)
    if not os.path.exists(testDir):
        os.makedirs(testDir)


#########################################################################
######################### CREATE TRAINING SETS ############################
#########################################################################

tset = writeTrainingData(trainDir, "SL2", alphabet)
trainingPosSL2 = tset[0]
trainingNegSL2 = tset[1]

tset = writeTrainingData(trainDir, "SL4", alphabet)
trainingPosSL4 = tset[0]
trainingNegSL4 = tset[1]

tset = writeTrainingData(trainDir, "SL8", alphabet)
trainingPosSL8 = tset[0]
trainingNegSL8 = tset[1]

##########################################################################
######################### CREATE TEST SETS #################################
##########################################################################

#########################   TEST 1  ######################################
allCombos = [None,None,None,None,None,None,None,None]

test1setSL2 = writeTest1data(testDir, "SL2",alphabet)
test1PosSL2 = test1setSL2[0]
test1NegSL2 = test1setSL2[1]

test1setSL4 = writeTest1data(testDir, "SL4",alphabet)
test1PosSL4 = test1setSL4[0]
test1NegSL4 = test1setSL4[1]

test1setSL8 = writeTest1data(testDir, "SL8",alphabet)
test1PosSL8 = test1setSL8[0]
test1NegSL8 = test1setSL8[1]

#########################   TEST 2  ######################################

test2setSL2 = writeTest2data(testDir, "SL2", alphabet)
test2PosSL2 = test2setSL2[0]
test2NegSL2 = test2setSL2[1]

test2setSL4 = writeTest2data(testDir, "SL4", alphabet)
test2PosSL4 = test2setSL4[0]
test2NegSL4 = test2setSL4[1]

test2setSL8 = writeTest2data(testDir, "SL8", alphabet)
test2PosSL8 = test2setSL8[0]
test2NegSL8 = test2setSL8[1]

