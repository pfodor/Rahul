import subprocess


outputDir = '../foma2_outputs/'
listOfScripts = []

p = subprocess.Popen('ls ./fs', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line.decode('utf-8')[:-1])
    listOfScripts.append(line.decode('utf-8')[:-1])
#listOfScripts=['sp8negative_56']
print('\n')
for script in listOfScripts:    
    p = subprocess.Popen('foma -f ./fs/'+script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    debug = []
    t = {}
    for line in p.stdout.readlines():
        l = line.decode('utf-8')
        if l[0] == '[':
            debug.append(l)
            x = l.split(' ')
            if '\n' in x[1]:
                x[1] = x[1].replace('\n','')
            if len(x[1]) in t:
                t[len(x[1])].append(x[1])
            else:
                t[len(x[1])]=[x[1]]
    retval = p.wait()

    f = open(outputDir+script+'.txt', 'w')
    for o in t:
        for x in t[o]:
            f.write(x)
            f.write('\n')
    f.close()
    print(script,":  ", debug[0])
    
