import rstr
import re

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

# GENERATE SP2 FOR APLHABET = {a,b,c}


def generateSP2Positive(alphabet):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = 1
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSP2(word)
        if not forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 20:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples

def generateSP4Positive(alphabet):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = 1
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSP4(word)
        if not forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 200:
            x += 1
            posSamples += samplePerLength
            samplePerLength = []
    return posSamples

def generateSP8Positive(alphabet):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = 1
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSP8(word)
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

def generateSP2Negative(alphabet):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []

    while len(samplePerLength)<(20*2):
        word = rstr.rstr(alphabet,2)
        # check if word is forbidden
        forbidden = checkForbiddenSP2(word)
        if forbidden:
            print(word)
            samplePerLength.append(word)
    x = 3
    negSamples+=samplePerLength
    samplePerLength = []
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSP2(word)
        if forbidden:
            samplePerLength.append(word)
            print(word , x, len(samplePerLength))
        if len(samplePerLength) == 20:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

def generateSP4Negative(alphabet):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []

    while len(samplePerLength)<(20*4):
        word = rstr.rstr(alphabet,4)
        # check if word is forbidden
        forbidden = checkForbiddenSP4(word)
        if forbidden:
            samplePerLength.append(word)
    x = 5
    negSamples+=samplePerLength
    samplePerLength = []
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSP4(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 200:
            x += 1
            negSamples += samplePerLength
            samplePerLength = []
    return negSamples

def generateSP8Negative(alphabet):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    while len(samplePerLength)<(20*8):
        word = rstr.rstr(alphabet,8)
        # check if word is forbidden
        forbidden = checkForbiddenSP8(word)
        if forbidden:
            samplePerLength.append(word)
    x = 9
    negSamples+=samplePerLength
    samplePerLength = []
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSP8(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 2000:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

##########################################################################
#########################CREATE TEST SETS#################################
#########################################################################

trainingPosSP2 = generateSP2Positive('abc')
print("done1")
trainingPosSP4 = generateSP4Positive('abc')
print("done2")
trainingPosSP8 = generateSP8Positive('abc')
print("done3")

trainingNegSP2 = generateSP2Negative('abc')
print("done4")
trainingNegSP4 = generateSP4Negative('abc')
print("done5")
trainingNegSP8 = generateSP8Negative('abc')
print("done6")

print(len(trainingPosSP2))
for x in trainingPosSP2:
    print(x,len(x))
