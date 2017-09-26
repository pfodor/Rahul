import rstr
from itertools import product
import sys

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

# GENERATE SL2 POSITIVE

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
    while len(samplePerLength)<(20*minWordLength):
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

############################## WRITE TRAINING DATA ##########################

def writeTrainingData(sl, alphabet):
    tSL = "./training/T_"+sl+".txt"
    f=open(tSL, "w")
    f.seek(0)
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSLPositive(alphabet, 20, checkForbiddenSL2, 1, 26)
        trainingNeg = generateSLNegative(alphabet, 1, 26, 20, checkForbiddenSL2)
    elif sl =="SL4":
        trainingPos = generateSLPositive(alphabet, 200, checkForbiddenSL4, 1, 26)
        trainingNeg = generateSLNegative(alphabet, 4, 26, 200, checkForbiddenSL4)
    else:
        trainingPos = generateSLPositive(alphabet, 2000, checkForbiddenSL8, 1, 26)
        trainingNeg = generateSLNegative(alphabet, 8, 26, 2000, checkForbiddenSL8)

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f.write(x)
        f.write('\n')

    f.close()
    return (trainingPos, trainingNeg)

################################# GENERATE TEST 1 ########################

def generateSLTest1(alphabet,trainingSL, sampleAmount, posORneg, checkForbidden):
    samples=[]
    for t in range(1,26):
        allCombos = [''.join(x) for x in product(alphabet, repeat = t)]
        for x in allCombos:
            if len(x) == t:
                if x not in trainingSL:
                    if not forbiddenChecker(x, posORneg, checkForbidden):
                        samplePerLength = []
                        while len(samplePerLength)<sampleAmount:
                            word = rstr.rstr(alphabet, t)
                            # check if word is forbidden
                            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                            if not forbidden:
                                if word not in trainingSL:
                                    samplePerLength.append(word)
                            samples+=samplePerLength
        #add extra samples
        extraSamples = []
        while len(extraSamples) < sampleAmount*10:
            word = rstr.rstr(alphabet, 25)
            # check if word is forbidden
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSL:
                    extraSamples.append(word)
        samples+=extraSamples
        return samples

############################## WRITE TEST DATA ################################

def writeTest1data(sl,alphabet):
    tSL = "./test/test1_"+sl+".txt"
    f=open(tSL, "w")
    f.seek(0)
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSLTest1(alphabet,trainingPosSL2, 20, 'POS', checkForbiddenSL2)
        trainingNeg = generateSLTest1(alphabet,trainingNegSL2, 20, 'NEG', checkForbiddenSL2)
    elif sl =="SL4":
        trainingPos = generateSLTest1(alphabet,trainingPosSL4, 200, 'POS', checkForbiddenSL4)
        trainingNeg = generateSLTest1(alphabet,trainingNegSL4, 200, 'NEG', checkForbiddenSL4)
    else:
        trainingPos = generateSLTest1(alphabet,trainingPosSL8, 2000, 'POS', checkForbiddenSL8)
        trainingNeg = generateSLTest1(alphabet,trainingNegSL8, 2000, 'NEG', checkForbiddenSL8)

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f.write(x)
        f.write('\n')

    f.close()
    return (trainingPos, trainingNeg)


def writeTest2data(sl,alphabet):
    tSL = "./test/test2_"+sl+".txt"
    f=open(tSL, "w")
    f.seek(0)
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSLPositive(alphabet, 20, checkForbiddenSL2, 26, 50)
        trainingNeg = generateSLNegative(alphabet, 26, 50, 20, checkForbiddenSL2)
    elif sl =="SL4":
        trainingPos = generateSLPositive(alphabet, 200, checkForbiddenSL4, 26, 50)
        trainingNeg = generateSLNegative(alphabet, 26, 50, 200, checkForbiddenSL4)
    else:
        trainingPos = generateSLPositive(alphabet, 2000, checkForbiddenSL8, 26, 50)
        trainingNeg = generateSLNegative(alphabet, 26, 50, 2000, checkForbiddenSL8)

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f.write(x)
        f.write('\n')

    f.close()
    return (trainingPos, trainingNeg)


##############################################################################
##############################################################################
if __name__ == "__main__":
    alphabet=sys.argv[1]

#########################################################################
######################### CREATE TRAINING SETS ############################
#########################################################################
tset = writeTrainingData("SL2", alphabet)
trainingPosSL2 = tset[0]
trainingNegSL2 = tset[1]

tset = writeTrainingData("SL4", alphabet)
trainingPosSL4 = tset[0]
trainingNegSL4 = tset[1]

#tset = writeTrainingData("SL8", alphabet)
#trainingPosSL8 = tset[0]
#trainingNegSL8 = tset[1]

##########################################################################
######################### CREATE TEST SETS #################################
##########################################################################

#########################   TEST 1  ######################################

test1setSL2 = writeTest1data("SL2",alphabet)
test1PosSL2 = test1setSL2[0]
test1NegSL2 = test1setSL2[1]

test1setSL4 = writeTest1data("SL4",alphabet)
test1PosSL4 = test1setSL4[0]
test1NegSL4 = test1setSL4[1]

test1setSL8 = writeTest1data("SL8",alphabet)
test1PosSL8 = test1setSL8[0]
test1NegSL8 = test1setSL8[1]

#########################   TEST 2  ######################################

test2setSL2 = writeTest2data("SL2", alphabet)
test2PosSL2 = test2setSL2[0]
test2NegSL2 = test2setSL2[1]

test2setSL4 = writeTest2data("SL4", alphabet)
test2PosSL4 = test2setSL4[0]
test2NegSL4 = test2setSL4[1]

test2setSL8 = writeTest2data("SL8", alphabet)
test2PosSL8 = test2setSL4[0]
test2NegSL8 = test2setSL4[1]
