import sys
import os

def sl(sl,alphabet, minWordLength, maxWordLength, fPath, slDirectory, fomaWriteFile):
    dpath = './foma_scripts'
    if not os.path.exists(dpath):
        os.makedirs(dpath)

    if not os.path.exists(slDirectory):
        os.makedirs(slDirectory)

    filePath = dpath+'/'+fPath
        
    scriptAlphabet = ''

    for l in alphabet:
        scriptAlphabet+=l+' | '
    scriptAlphabet = scriptAlphabet[:-2]
    scriptAlphabet = '[ ' + scriptAlphabet + ' ]^{}'
   
    if sl == 'sl2p' or  sl == 'sl2n':
        f=open(filePath, 'w')
        for length in range(minWordLength, maxWordLength+1):
            scriptCommand = "regex " + scriptAlphabet.replace('{}', str(length) )
            if sl == 'sl2n':
                scriptCommand += ' & [ b ?* | ?* a | ?* a a ?* | ?* b b  ?* ] ;'
            else:
                scriptCommand += ' - [ b ?* | ?* a | ?* a a ?* | ?* b b  ?* ] ;'
            f.write(scriptCommand)
            f.write('\n')
            f.write('print words > '+fomaWriteFile+'_'+str(length)+'.txt')
            f.write('\n')
        f.close()    

    if sl =='sl4p' or sl == 'sl4n':
        f=open(filePath, 'w')
        for length in range(minWordLength, maxWordLength+1):
            scriptCommand = "regex " + scriptAlphabet.replace('{}', str(length) )
            if sl =='sl4n':
                scriptCommand += ' & [ b b b ?* | ?* a a a | ?* a a a a ?* | ?* b b b b ?* ] ;'
            else:
                scriptCommand += ' - [ b b b ?* | ?* a a a | ?* a a a a ?* | ?* b b b b ?* ] ;'
            f.write(scriptCommand)
            f.write('\n')
            f.write('print words > '+fomaWriteFile+'_'+str(length)+'.txt')
            f.write('\n')
        f.close()

    if sl=='sl8p' or sl == 'sl8n':
        f=open(filePath, 'w')
        for length in range(minWordLength, maxWordLength+1):
            scriptCommand = "regex " + scriptAlphabet.replace('{}', str(length) )
            if sl=='sl8n':
                scriptCommand += ' & [ b b b b b b b ?* | ?* a a a a a a a | ?* a a a a a a a a ?* | ?* b b b b b b b b ?* ] ;'
            else:
                scriptCommand += ' - [ b b b b b b b ?* | ?* a a a a a a a | ?* a a a a a a a a ?* | ?* b b b b b b b b ?* ] ;'
            f.write(scriptCommand)
            f.write('\n')
            f.write('print words > '+fomaWriteFile+'_'+str(length)+'.txt')
            f.write('\n')
        f.close()

#construct foma scripts for 3 letter alphabet

alphabet = 'abc'

sl('sl2n', alphabet, 1, 12, 'sl2negative_3', './foma_outputs/sl2negative_3/', '../foma_outputs/sl2negative_3/sl2negative_3')
#sl('sl2p', alphabet, 1, 12, 'sl2positive_3', '../foma_outputs/sl2positive_3')
sl('sl4n', alphabet, 1, 12, 'sl4negative_3', './foma_outputs/sl4negative_3/', '../foma_outputs/sl4negative_3/sl4negative_3')
#sl('sl4p', alphabet, 1, 12, 'sl4positive_3', '../foma_outputs/sl4positive_3')
sl('sl8n', alphabet, 1, 12, 'sl8negative_3', './foma_outputs/sl8negative_3/', '../foma_outputs/sl8negative_3/sl8negative_3')
#sl('sl8p', alphabet, 1, 12, 'sl8postivie_3', '../foma_outputs/sl8positive_3')

"""

sl('sl2n', alphabet, 26, 50, 'sl2negative_3_test2')
sl('sl2p', alphabet, 26, 50, 'sl2positive_3_test2')
sl('sl4n', alphabet, 26, 50, 'sl4negative_3_test2')
sl('sl4p', alphabet, 26, 50, 'sl4positive_3_test2')
sl('sl8n', alphabet, 26, 50, 'sl8negative_3_test2')
sl('sl8p', alphabet, 26, 50, 'sl8positive_3_test2')

"""

#construct foma scripts for 10 letter alphabet

alphabet = 'abcdefghij'

sl('sl2n', alphabet, 1, 8, 'sl2negative_10', './foma_outputs/sl2negative_10/', '../foma_outputs/sl2negative_10/sl2negative_10')
#sl('sl2p', alphabet, 1, 8, 'sl2positive_10', '../foma_outputs/sl2positive_10')
sl('sl4n', alphabet, 1, 8, 'sl4negative_10', './foma_outputs/sl4negative_10/', '../foma_outputs/sl4negative_10/sl4negative_10')
#sl('sl4p', alphabet, 1, 8, 'sl4positive_10', '../foma_outputs/sl4positive_10')
sl('sl8n', alphabet, 1, 8, 'sl8negative_10', './foma_outputs/sl8negative_10/', '../foma_outputs/sl8negative_10/sl8negative_10')
#sl('sl8p', alphabet, 1, 8, 'sl8postivie_10', '../foma_outputs/sl8positive_10')

"""
sl('sl2n', alphabet, 26, 50, 'sl2negative_10_test2')
sl('sl2p', alphabet, 26, 50, 'sl2positive_10_test2')
sl('sl4n', alphabet, 26, 50, 'sl4negative_10_test2')
sl('sl4p', alphabet, 26, 50, 'sl4positive_10_test2')
sl('sl8n', alphabet, 26, 50, 'sl8negative_10_test2')
sl('sl8p', alphabet, 26, 50, 'sl8positive_10_test2')
"""
#construct foma scripts for 56 letter alphabet

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234'

sl('sl2n', alphabet, 1, 5, 'sl2negative_56', './foma_outputs/sl2negative_56/', '../foma_outputs/sl2negative_56/sl2negative_56')
#sl('sl2p', alphabet, 1, 5, 'sl2positive_56', '../foma_outputs/sl2positive_56')
sl('sl4n', alphabet, 1, 7, 'sl4negative_56', './foma_outputs/sl4negative_56/', '../foma_outputs/sl4negative_56/sl4negative_56')
#sl('sl4p', alphabet, 1, 7, 'sl4positive_56', '../foma_outputs/sl4positive_56')
sl('sl8n', alphabet, 1, 10, 'sl8negative_56', './foma_outputs/sl8negative_56/', '../foma_outputs/sl8negative_56/sl8negative_56')
#sl('sl8p', alphabet, 1, 10, 'sl8postivie_56', '../foma_outputs/sl8positive_56')

"""
sl('sl2n', alphabet, 26, 50, 'sl2negative_56_test2')
sl('sl2p', alphabet, 26, 50, 'sl2positive_56_test2')
sl('sl4n', alphabet, 26, 50, 'sl4negative_56_test2')
sl('sl4p', alphabet, 26, 50, 'sl4positive_56_test2')
sl('sl8n', alphabet, 26, 50, 'sl8negative_56_test2')
sl('sl8p', alphabet, 26, 50, 'sl8positive_56_test2')
"""

