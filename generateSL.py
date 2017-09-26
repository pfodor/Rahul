import rstr
from itertools import product

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

# GENERATE SL2 FOR APLHABET = {a,b,c}


def generateSL2Positive(alphabet):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = 1
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSL2(word)
        if not forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 20:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples

def generateSL4Positive(alphabet):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = 1
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSL4(word)
        if not forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 200:
            x += 1
            posSamples += samplePerLength
            samplePerLength = []
    return posSamples

def generateSL8Positive(alphabet):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = 1
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSL8(word)
        if not forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 2000:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples

##########################################################################
########################NEGATIVE SAMPLES##################################
##########################################################################

def generateSL2Negative(alphabet):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    x = 1
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSL2(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 20:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

def generateSL4Negative(alphabet):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []

    while len(samplePerLength)<(20*4):
        word = rstr.rstr(alphabet,4)
        # check if word is forbidden
        forbidden = checkForbiddenSL4(word)
        if forbidden:
            samplePerLength.append(word)
    x = 5
    negSamples+=samplePerLength
    samplePerLength = []
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSL4(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 200:
            x += 1
            negSamples += samplePerLength
            samplePerLength = []
    return negSamples

def generateSL8Negative(alphabet):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    while len(samplePerLength)<(20*8):
        word = rstr.rstr(alphabet,8)
        # check if word is forbidden
        forbidden = checkForbiddenSL8(word)
        if forbidden:
            samplePerLength.append(word)
    x = 9
    negSamples+=samplePerLength
    samplePerLength = []
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSL8(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 2000:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

def writeTrainingData(sl, alphabet):
    tSL = "./training/T_"+sl+".txt"
    f=open(tSL, "w")
    f.seek(0)
    trainingPos=[]
    trainingNeg=[]

    if sl == "SL2":
        trainingPos = generateSL2Positive(alphabet)
        trainingNeg = generateSL2Negative(alphabet)
    elif sl =="SL4":
        trainingPos = generateSL4Positive(alphabet)
        trainingNeg = generateSL4Negative(alphabet)
    else:
        trainingPos = generateSL8Positive(alphabet)
        trainingNeg = generateSL8Negative(alphabet)

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f.write(x)
        f.write('\n')

    f.close()
    return (trainingPos, trainingNeg)

#########################################################################
#########################CREATE TRAINING SETS############################
#########################################################################
tset = writeTrainingData("SL2", 'abc')
trainingPosSL2 = tset[0]
trainingNegSL2 = tset[1]

print(trainingPosSL2)
print("=============================================================")

tset = writeTrainingData("SL4", 'abc')
trainingPosSL4 = tset[0]
trainingNegSL4 = tset[1]

#tset = writeTrainingData("SL8", 'abc')
#trainingPosSL8 = tset[0]
#trainingNegSL8 = tset[1]


##########################################################################
#########################CREATE TEST SETS#################################
##########################################################################

def generateSLTest1(alphabet,trainingSL, sampleAmount, posORneg, checkForbidden):
    samples=[]
    for t in range(1,26):
        allCombos = [''.join(x) for x in product(alphabet, repeat = t)]
        print(samples)
        print("#########################################################")
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

test1PosSL2 = generateSLTest1('abc',trainingPosSL2, 20, 'POS', checkForbiddenSL2)
test1PosSL4 = generateSLTest1('abc',trainingPosSL4, 200, 'POS', checkForbiddenSL4)
test1PosSL8 = generateSLTest1('abc',trainingPosSL8, 2000, 'POS', checkForbiddenSL8)

test1NegSL2 = generateSLTest1('abc',trainingNegSL2, 20, 'NEG', checkForbiddenSL2)
test1NegSL4 = generateSLTest1('abc',trainingNegSL4, 200, 'NEG', checkForbiddenSL4)
test1NegSL8 = generateSLTest1('abc',trainingNegSL8, 2000, 'NEG', checkForbiddenSL8)
