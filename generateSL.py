import rstr


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
    x=1
    while len(samplePerLength)<(20*8):
        x+=1
        word = rstr.rstr(alphabet,8)
        # check if word is forbidden
        forbidden = checkForbiddenSL8(word)
        if forbidden:
            samplePerLength.append(word)
    x = 9
    while x < 26:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbiddenSL8(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == 2000:
            x += 1
            print(x)
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples


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

##########################################################################
#########################CREATE TEST SETS#################################
#########################################################################

trainingPosSL2 = generateSL2Positive('abc')
trainingPosSL4 = generateSL4Positive('abc')
trainingPosSL8 = generateSL8Positive('abc')

trainingNegSL2 = generateSL2Negative('abc')
trainingNegSL4 = generateSL4Negative('abc')
#trainingNegSL8 = generateSL8Negative('abc')

print(len(trainingPosSL2))
for x in trainingPosSL2:
    print(x,len(x))
