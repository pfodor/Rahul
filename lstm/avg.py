from statistics import mean, stdev
f = open('results.txt', 'r')
w = open('results_w_average.txt' ,'w+')

for l in f:
    if 'Test' in l:
        t = l[:-2].split(' ')
        nums=[float(x) for x in t[-10:]]
        m = mean(nums)
        s = stdev(nums)
        w.write(l[:-1] + ' AVERAGE: ' + '{0:.4f}'.format(m) + ' STDEV: ' + '{0:.4f}'.format(s) + '\n')
    else:
        w.write(l)
        
