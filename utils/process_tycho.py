import math

ref = dict()
def main():
    tycho = open('tycho2_stripped.dat')
    suppl = open('suppl_1.dat')

    xref = open('xref.dat')

    for line in xref:
        data = line.strip().split('|')
        #print '"%s" %s' % (data[0], str(data))
        ref[str(data[0])] = data
    
    print 'references: %s' % (str(len(ref)))
    
    RA = 2
    DEC = 3
    RA_ = 24
    DEC_ = 25
    BTMAG = 17
    VTMAG = 19
    PROX = 21
    HIP = 23

    sRA = 2
    sDEC = 3
    sBTMAG = 11
    sVTMAG = 13
    sPROX = 15
    sHIP = 17
    abbr = open('tycho2_abbr_new.dat', 'w')
    for line in tycho:
        line = line.split('|')
        
        try:
            ra = float(line[RA])
            dec = float(line[DEC])
        except:
            ra = float(line[RA_])
            dec = float(line[DEC_])
        
        pos = convert(ra, dec)
        name = get_xref(line[HIP])    
        mag = line[VTMAG]
        if mag == '':
            mag = line[BTMAG]
            
        row = '|'.join([line[0], line[HIP].strip(), name[0], name[1], str(ra), str(dec), str(pos[0]), str(pos[1]), str(pos[2]), pos[3], str(pos[4]), str(pos[5]), str(pos[6]), str(mag).strip(), line[PROX].strip()])
        
        abbr.write(row + '\n')
    count = 1  
    print 'processing suppl:'     
    for line in suppl:
        line = line.strip().split('|')
        try:
            ra = float(line[sRA])
            dec = float(line[sDEC])
        except:
            print 'error!: %s' % (line)
            #continue
        
        pos = convert(ra, dec)
        
        name = get_xref(line[sHIP])
        mag = line[sVTMAG]
        if mag == '':
            mag = line[sBTMAG]
        row = '|'.join([line[0], line[sHIP].strip(), name[0], name[1], line[sRA], line[sDEC], str(pos[0]), str(pos[1]), str(pos[2]), pos[3], str(pos[4]), str(pos[5]), str(pos[6]), str(mag).strip(), line[sPROX].strip()])
        
        abbr.write(row + '\n')
        count += 1
    print count
    
    tycho.close()
    suppl.close()
    abbr.close()

def convert(ra, dec):
    rah = ra / 15.0
    ram = 60 * (rah - math.trunc(rah))
    ras = 60 * (ram - math.trunc(ram))

    rah = math.trunc(rah)
    ram = math.trunc(ram)
    
    ded = dec
    if dec < 0:
        de_ = '-'
    else:
        de_ = '+'
    dem = 60 * (ded - math.trunc(ded))
    des = 60 * (dem - math.trunc(dem))
    
    ded = math.fabs(math.trunc(ded))
    dem = math.fabs(math.trunc(dem))
    des = math.fabs(des)

    return (rah, ram, ras, de_, ded, dem, des)
    
def get_xref(hip):
    hd = ''
    name = ''
    
    try:
        x = ref[str(hip).strip()]
        hd = x[1].strip()
        name = x[2].strip()
    except KeyError:
        try:
            x = ref[str(hip).strip()[:-1]]
            hd = x[1].strip()
            name = x[2].strip()
        except:
            return ('','')
        
    return (hd, name)
    
main()