hip = open('hip_main_stripped.dat')
xref = open('hip_hd_xref.dat', 'w')

for line in hip:
    row = line.split('|')
    line = [row[1], row[71]]
    if row[71] != '':
        xref.write('|'.join(line) + '\n')