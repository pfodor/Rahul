import sys
import os

def sp(sp,alphabet, minWordLength, maxWordLength, fPath):
    dpath = './fs'
    if not os.path.exists(dpath):
        os.makedirs(dpath)

    #if not os.path.exists(spDirectory):
    #    os.makedirs(spDirectory)
    
    filePath = dpath+'/'+fPath
        
    scriptAlphabet = ''

    for l in alphabet:
        scriptAlphabet+=l+' | '
    scriptAlphabet = scriptAlphabet[:-2]
    scriptAlphabet = '[ ' + scriptAlphabet + ' ]^{}'
    
    if sp == 'sp2p' or  sp == 'sp2n':
        f=open(filePath, 'w')
        for length in range(minWordLength, maxWordLength+1):
            scriptCommand = "regex " + scriptAlphabet.replace('{}', str(length) )
            if sp == 'sp2n':
                scriptCommand += ' & [ ?* a ?* b ?* ] ;'
            else:
                scriptCommand += ' - [ ?* a ?* b ?* ] ;'
            f.write(scriptCommand)
            f.write('\n')
            for x in range(20000):
                f.write('print random-words')
                f.write('\n')
        f.close()    

    if sp =='sp4p' or sp == 'sp4n':
        f=open(filePath, 'w')
        for length in range(minWordLength, maxWordLength+1):
            scriptCommand = "regex " + scriptAlphabet.replace('{}', str(length) )
            if sp =='sp4n':
                scriptCommand += ' & [ ?* a ?* b ?* b ?* a ?* ] ;'
            else:
                scriptCommand += ' - [ ?* a ?* b ?* b ?* a ?* ] ;'
            f.write(scriptCommand)
            f.write('\n')
            for x in range(20000):
                f.write('print random-words')
                f.write('\n')
        f.close()

    if sp=='sp8p' or sp == 'sp8n':
        f=open(filePath, 'w')
        for length in range(minWordLength, maxWordLength+1):
            scriptCommand = "regex " + scriptAlphabet.replace('{}', str(length) )
            if sp=='sp8n':
                scriptCommand += ' & [ ?* a ?* b ?* b ?* a ?* a ?* b ?* b ?* a ?* ] ;'
            else:
                scriptCommand += ' - [ ?* a ?* b ?* b ?* a ?* a ?* b ?* b ?* a ?* ] ;'
            f.write(scriptCommand)
            f.write('\n')
            for x in range(20000):
                f.write('print random-words')
                f.write('\n')
        f.close()

#construct foma scripts for 3 letter alphabet

alphabet = 'abc'

sp('sp2n', alphabet, 1, 50, 'sp2negative_3')
sp('sp2p', alphabet, 1, 50, 'sp2positive_3')
sp('sp4n', alphabet, 1, 50, 'sp4negative_3')
sp('sp4p', alphabet, 1, 50, 'sp4positive_3')
sp('sp8n', alphabet, 1, 50, 'sp8negative_3')
#sp('sp8p', alphabet, 1, 12, 'sp8postivie_3', '../foma_outputs/sp8positive_3')


"""

sp('sp2n', alphabet, 26, 50, 'sp2negative_3_test2')
sp('sp2p', alphabet, 26, 50, 'sp2positive_3_test2')
sp('sp4n', alphabet, 26, 50, 'sp4negative_3_test2')
sp('sp4p', alphabet, 26, 50, 'sp4positive_3_test2')
sp('sp8n', alphabet, 26, 50, 'sp8negative_3_test2')
sp('sp8p', alphabet, 26, 50, 'sp8positive_3_test2')

"""

#construct foma scripts for 10 letter alphabet

alphabet = 'abcdefghij'

sp('sp2n', alphabet, 1, 50, 'sp2negative_10')
sp('sp2p', alphabet, 1, 50, 'sp2positive_10')
sp('sp4n', alphabet, 1, 50, 'sp4negative_10')
sp('sp4p', alphabet, 1, 50, 'sp4positive_10')
sp('sp8n', alphabet, 1, 50, 'sp8negative_10')
#sp('sp8p', alphabet, 1, 8, 'sp8postivie_10', '../foma_outputs/sp8positive_10')

"""
sp('sp2n', alphabet, 26, 50, 'sp2negative_10_test2')
sp('sp2p', alphabet, 26, 50, 'sp2positive_10_test2')
sp('sp4n', alphabet, 26, 50, 'sp4negative_10_test2')
sp('sp4p', alphabet, 26, 50, 'sp4positive_10_test2')
sp('sp8n', alphabet, 26, 50, 'sp8negative_10_test2')
sp('sp8p', alphabet, 26, 50, 'sp8positive_10_test2')
"""
#construct foma scripts for 56 letter alphabet

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234'

sp('sp2n', alphabet, 1, 50, 'sp2negative_56')
sp('sp2p', alphabet, 1, 50, 'sp2positive_56')
sp('sp4n', alphabet, 1, 50, 'sp4negative_56')
sp('sp4p', alphabet, 1, 50, 'sp4positive_56')
sp('sp8n', alphabet, 1, 50, 'sp8negative_56')
#sp('sp8p', alphabet, 1, 10, 'sp8postivie_56', '../foma_outputs/sp8positive_56')

"""
sp('sp2n', alphabet, 26, 50, 'sp2negative_56_test2')
sp('sp2p', alphabet, 26, 50, 'sp2positive_56_test2')
sp('sp4n', alphabet, 26, 50, 'sp4negative_56_test2')
sp('sp4p', alphabet, 26, 50, 'sp4positive_56_test2')
sp('sp8n', alphabet, 26, 50, 'sp8negative_56_test2')
sp('sp8p', alphabet, 26, 50, 'sp8positive_56_test2')
"""
