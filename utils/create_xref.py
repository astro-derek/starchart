xref = open('xref.dat', 'w')
hip_hd_xref = open('hip_hd_xref.dat')
bs = open('bs_catalogue_stripped.csv')

hh_xref = list()
for line in hip_hd_xref:
    row = line.strip().split('|')
    hh_xref.append([row[0], row[1]])
    
hd_bs = dict()
for line in bs:
    data = line.strip().split('|')
    hd_bs[data[3]] = data[1]
    
for row in hh_xref:
    name = ''
    try:
        name = hd_bs[row[1]]
    except:
        name = ''
    row.append(name)
    xref.write('|'.join(row) + '\n')
