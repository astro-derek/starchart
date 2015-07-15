import sys

filename = sys.argv[1]
data = open(filename).readlines()
count = 0
for line in data:
    cols = line.split('|')
    newcols = list()
    for col in cols:
        newcol = col.strip()
        newcols.append(newcol)
    newline = '|'.join(newcols)
    print newline
    count += 1
    sys.stderr.write('%s\n' % (count))