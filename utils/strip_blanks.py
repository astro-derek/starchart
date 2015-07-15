import sys

def strip_blanks(filename):
    file = open(filename)
    count = 0
    line = file.readline()
    while line != '':
        cols = line.split('|')
        newcols = list()
        for col in cols:
            newcols.append(col.strip())
        print '|'.join(newcols)
        count+=1
        if count % 1000 == 0:
            sys.stderr.write('%s\n' % (count))
        line = file.readline()
strip_blanks(sys.argv[1])