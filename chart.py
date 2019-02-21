from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
import re
import sys
import argparse
import math
from decimal import Decimal 

args = None

a4_width = 8.27
a4_height = 11.69

TYC = 0
HIP = 1
HD = 2
NAME = 3
RAH = 6
RAM = 7
RAS = 8
DE_ = 9
DED = 10
DEM = 11
DES = 12
VMAG = 13
PROX = 14

TYCHO_ROWS = 2557500
NGC_ROWS = 14002

alp = re.compile(r'.*Alp')
bet = re.compile(r'.*Bet')
gam = re.compile(r'.*Gam')
delt = re.compile(r'.*Del')
eps = re.compile(r'.*Eps')
zet = re.compile(r'.*Zet')
eta = re.compile(r'.*Eta')
iot = re.compile(r'.*Iot')
the = re.compile(r'.*The')
kap = re.compile(r'.*Kap')
lam = re.compile(r'.*Lam')
mu = re.compile(r'.*Mu')
nu = re.compile(r'.*Nu')
xi = re.compile(r'.*Xi')
omi = re.compile(r'.*Omi')
pi = re.compile(r'.*Pi')
rho = re.compile(r'.*Rho')
sig = re.compile(r'.*Sig')
tau = re.compile(r'.*Tau')
ups = re.compile(r'.*Ups')
phi = re.compile(r'.*Phi')
chi = re.compile(r'.*Chi')
psi = re.compile(r'.*Psi')
ome = re.compile(r'.*Ome')

c_prog = 0
fifteen = float(15)
scale = float('.75')
cmax = 0.0;

gainsboro = (220,220,220,255)
gray = (128,128,128,255)
white = 'white'
black = 'black'
red = (116,255,255,255)
lightblue = (190,150,30,255)
lightgreen = (221,116,221,255)
orange = (34, 108, 207, 255)
label = (139, 167, 214, 255) // invert this!

rads = float(math.pi / 180)


times = None
arial = None
arial_small = None
con_font = None

doubles = list()

def main(params):
     
    global cmax
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', choices=['stereo', 'polar', 'gnomonic'], default='stereo', help='type of projection to use for the chart')
    parser.add_argument('-r', '--ra', type=float, default=6, help='center of the chart in right ascension')
    parser.add_argument('-d', '--dec', type=float, default=0, help='center of the chart in declination')
    parser.add_argument('-f', '--fov', type=float, default=5, help='fov for gnomonic projection')
    
    parser.add_argument('-m', '--mag', type=float, default=9, help='lowest magnitude stars to chart')
    parser.add_argument('-l', '--labelLimit', type=Decimal, default=6, help='only display labels on stars brighter than this')
    
    parser.add_argument('-c', '--catalogue', default='data/tycho2_abbr_new2.dat', help='catalogue to use for the query')
    parser.add_argument('-L', '--labels', action='store_false', default=True, help='draw labels on objects')
    parser.add_argument('-G', '--grid', action='store_false', default=True, help='draw coordinate grid')
    parser.add_argument('-B', '--borders', action='store_false', default=True, help='draw constellation border lines')
    parser.add_argument('--figures', action='store_false', default=True, help='draw constellation figures')
    parser.add_argument('-N', '--names', action='store_false', default= True, help='draw constellation names')
    
    parser.add_argument('-W', '--width', type=float, default=a4_width, help='width of the chart')
    parser.add_argument('-H', '--height', type=float, default=a4_height, help='height of the chart')
    parser.add_argument('-S', '--scaleR', type=float, default=1, help='scale factor for objects')
    parser.add_argument('-F', '--factor', type=float, default=3, help='size multiplier for drawing chart')
    
    parser.add_argument('-q', '--query', default=None, help='query the data files')
    parser.add_argument('-p', '--process', default=False, action='store_true', help='quit query on first result')
    parser.add_argument('-ff', '--filter', default=False, action='store_true', help='filter stars outside the bounds')
    parser.add_argument('-n', '--ngc', default=False, action='store_true', help='only query ngc catalogue')
    parser.add_argument('-o', '--queryonly', default=True, action='store_false', help='draw the chart aswell - centered on the first result')
    
    parser.add_argument('--ngc_max', type=float, default=9, help='limiting magnitude for ngc objects')
    parser.add_argument('--rmax', type=float, default=50, help='max distance of label from object')
    parser.add_argument('--dpi', type=float, default=300, help='dots per inch for image')
    
    parser.add_argument('--con_font', type=int, default=18, help='size of font used for constellation labels')
    parser.add_argument('--bayer_font', type=int, default=14, help='size of font used for stars identified by bayer / flamsteed')
    parser.add_argument('--hip_font', type=int, default=12, help='size of font used for hipparchos ids')
    parser.add_argument('--ngc_font', type=int, default=12, help='size of font used for ngc object labels')
    
    parser.add_argument('--out', type=argparse.FileType('wb'), default=None, help='filename for output')
	
    parser.add_argument('--figure_line_width', type=int, default=1, help='width for figure lines')
    parser.add_argument('--con_line_width', type=int, default=1, help='width for border lines')
    parser.add_argument('--ecliptic_line_width', type=int, default=1, help='width for ecliptic')
    parser.add_argument('--tick_width', type=int, default=1, help='width for tick lines')
    
    global args, times, arial, arial_small, con_font
    
    if params == None:
        params = sys.argv
        
    print params
    args = parser.parse_args(params)
    console('%s' % (args))
    
    times = ImageFont.truetype("C:/Windows/Fonts/times.ttf", args.bayer_font)
    arial = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", args.hip_font)
    arial_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", args.ngc_font)
    con_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", args.con_font)
    
    if args.query != None:
        result = run_query(args)
        if args.queryonly or not result:
            return
    
    args.width = args.width * args.dpi
    args.height = args.height * args.dpi
        
    if args.type == 'gnomonic':
        cmax = calc_cmax(args.ra, args.dec, args.fov / 2)
        console('cmax: %s' % (cmax))
    if args.type == 'polar':
        args.height = args.width
    if args.type == 'gnomonic':
        args.height = args.width
        
    image = create_chart(args)
    print 'image done'
    if args.out:
        image.save(args.out, 'PNG')
    else:
        return image
    
    
def run_query(args):
    results = query(args)
    got = False
    console('query found %s result(s):' % (len(results)))
    for line in results:
        if not args.queryonly and not got:
            if line[0] == 'N' or line[0] == 'I':
                args.ra = ngc_ra(line[8], line[9], line[10])
                args.dec = ngc_dec(line[11], line[12], line[13], line[14])
            else:
                args.ra = ngc_ra(line[RAH], line[RAM], line[RAS])
                args.dec = ngc_dec(line[DE_], line[DED], line[DEM], line[DES])
            got = True
        if line[0] == 'N' or line[0] == 'I':
            console('%s %scon:  %s\nra:   %sh %sm %ss\ndec:  %s%sd %sm %ss\nmag:  %s\ntype: %s\n' % (line[0] + line[1], ' '.join(line[24:]), line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[16], line[22]))
        else:
            console('%s' % (line))
    if len(results) > 0:
        return True
    else:
        return False
        
def calc_cmax(base_ra, base_dec, base_fov):
    lam = (base_ra + (base_fov/15.0)) * 15.0 * rads
    chi = (base_dec + base_fov) * rads
    lam0 = base_ra * 15 * rads
    chi1 = base_dec * rads
    return math.sin(chi) * math.sin(chi1) + math.cos(chi) * math.cos(chi1) * math.cos(lam - lam0)
    
def query(args):
    results = list()
    
    if not args.ngc:
        console('searching tycho for %s' % (args.query))
        tycho = open(args.catalogue)
        count = 0
        for row in tycho:
            line = row.split('|')
            count += 1
            
            if line[TYC] == args.query or line[HIP] == args.query or line[HD] == args.query or line[NAME].upper().find(args.query.upper()) != -1:
                if line[VMAG] and float(line[VMAG]) <= args.mag:
                    results.append(line)
                    if args.process:
                        return results
            progress(count, TYCHO_ROWS)
    
    console('searching ngc for %s' % (args.query))
    ngc = open('data/ngc.csv')
    count = 0
    for row in ngc:
        line = row.split(',')
        count += 1
        
        if str(line[0] + line[1]).upper() == args.query.upper():# or str('|'.join(line[24:])).upper().find(args.query.upper()) != -1 or str(line[7]).upper() == args.query.upper():
            print '%s %s ' % (line[16], args.ngc_max)
            if line[16] and float(line[16]) <= args.ngc_max:
                results.append(line)
                if args.process:
                    return results
        progress(count, NGC_ROWS)
            
    return results
    
def console(text):
    sys.stdout.write('\n%s     ' % (text))


def progress(value, max):
    global c_prog
    prog = int(value * 100 / max)
    if c_prog != prog:
        sys.stdout.write("\b\b\b\b\b%4s%%" % (prog))
        c_prog = prog
        
def create_chart(args):
    console('getting ngc...')
    ngc = get_ngc(args)
    
    console('executing query...')
    stars = get_stars(args)
    
    console('drawing chart...')
    image = draw(stars, ngc, args)
    
    return image

def get_stars(args):
    stars = list()
    
    data = open(args.catalogue)
    line_no = 1
    
    for row in data:
        raw = row.strip().split('|')
        star = parse_star(raw, args)
        if star:
            stars.append(star)
        
        line_no += 1
        progress(line_no, TYCHO_ROWS)
        
    return stars
    
def parse_star(row, args):
    #try:
    if not float(row[VMAG]) <= args.mag:
        return None
    #except:
    #    console('error on line: %s' % (row))
    #    return None
        
    point = get_point(row, args)
    if point:
        id = row[NAME]
        name = ''
        mag = float(row[VMAG])
        font = times
        con = ''
        if args.labels:
            if id != None:
                id = id.strip()
                con = id[-3:]
                name = fix(id[:-3]).strip()
            if name == '' and args.labelLimit != None and mag <= args.labelLimit:
                if row[HIP] != '':
                    name = str(row[HIP]).strip()
                else:
                    name = str(row[TYC]).strip()
                    
                font = arial
            
        hip = row[HIP]
        prox = row[PROX].strip()
        
        return {'name': name, 'con': con, 'point': point, 'mag': mag, 'font': font, 'prox': prox, 'hip': hip}

    return None


def get_point(row, args):    
    r = float(row[RAH]) + float(row[RAM]) / 60 + float(row[RAS]) / 3600
    sign = -1 if row[DE_] == '-' else 1
    
    d = sign * float(row[DED]) + (sign * float(row[DEM]) / 60) + (sign * float(row[DES]) / 3600)
    
    point = get_coords(r, d, args)
    return point

        
def get_boundaries():
    data = open('data/boundaries.dat').readlines()
    boundaries = list()
    for line in data:
        cols = line.lstrip().split()
        row = {'ra': float(cols[0]), 'dec': float(cols[1]), 'con': cols[2], 'flag': cols[3]}
        boundaries.append(row)
    return boundaries

def get_figures():
    data = open('data/conlines.csv').readlines()
    lines = list()
    for line in data:
        cols = line.lstrip().split(',')
        row = {'con': cols[0], 'startRa': float(cols[1])/1000, 'startDec': float(cols[2])/100, 'endRa': float(cols[3])/1000, 'endDec': float(cols[4])/100}
        lines.append(row)
    return lines
    
def get_names():
    data = open('data/names.csv').readlines()
    names = list()
    for line in data:
        cols = line.split(',')
        row = {'name': cols[0], 'abbr': cols[1], 'ra': float(cols[2]), 'dec': float(cols[3])}
        names.append(row)
    return names
    
def draw(data, ngc, args):
    image = Image.new('RGBA', (math.trunc(args.width), math.trunc(args.height)), white)
    
    chart = ImageDraw.Draw(image)
    w,h = image.size
    rectangle = (0,0,w-1,h-1)
    chart.rectangle(rectangle, outline="gray")
    
    if args.grid:
        console('plotting dec lines...')
        drawDeclinationLines(chart, args)
        
        console('plotting ra lines...')
        drawRaLines(chart, args)
    
    if args.borders:
        console('plotting constellation borders...')
        drawBorders(chart, args)
    
    if args.figures:
        console('plotting constellation figures...')
        if args.type == 'polar':
            drawPolarFigures(chart, args)
        elif args.type == 'stereo':
		    drawRAFigures(chart, args)
    
    drawEcliptic(chart, args)
    
    if args.names:
        console('plotting constellation names...')
        drawNames(chart, args)
        
    console('plotting ngc objects...')
    drawNgc(chart, ngc, args)
        
    console('plotting star positions...')
    drawStars(chart, data, args)
        
    if args.type == 'polar':
        point = get_coords(args.ra - 12, args.dec - 1, args)
        point2 = get_coords(args.ra, args.dec -1, args)
        chart.line([(point['x'], point['y']), (point['x'], point2['y'])], fill=gray, width=args.tick_width)
        point = get_coords(args.ra - 6, args.dec - 1, args)
        point2 = get_coords(args.ra + 6, args.dec -1, args)
        chart.line([(point['x'], point['y']), (point2['x'], point['y'])], fill=gray, width=args.tick_width)
    
    if args.labels:
        drawLabels(chart, image, ngc, data, args)
        
    console('finished drawing.')
    return image

def drawNgc(chart, ngc, args):
    ngccount = 0
    counter = 0
    for row in ngc:
        if row['mag'] <= args.ngc_max:
            ngccount += 1
            point = row['point']
            x = point['x'] - 10 * args.scaleR
            y = point['y'] - 5 * args.scaleR
            x1 = point['x'] + 10 * args.scaleR 
            y1 = point['y'] + 5 * args.scaleR
            
            chart.ellipse((x, y, x1, y1), outline=black)
        counter += 1
        progress(counter, len(ngc))
    console('drew %s ngc objects' % (ngccount))
    
def drawStars(chart, data, args):
    counter = 0
    for row in data:
        point = row['point']
        m = calc_rad(row['mag'])
        
        x = point['x'] - m * args.scaleR
        y = point['y'] - m * args.scaleR
        x1 = point['x'] + m * args.scaleR 
        y1 = point['y'] + m * args.scaleR
        
        chart.ellipse((x, y, x1, y1), fill=black)
        chart.ellipse((x, y, x1, y1), outline=white)
        prox = row['prox']
        if prox != '999' and m > 1:
            cy = y + ((y1 - y) / 2)
            chart.line((x - 1, cy, x1 + 1, cy), fill=black)
        counter += 1
        progress(counter, len(data))
        
def drawLabels(chart, image, ngc, data, args):
    counter = 0
    console('writing star labels...')
    for row in data:
        point = row['point']
        name = row['name']
        font_family = row['font']
        
        if name != '' and args.labels and row['mag'] <= args.labelLimit:
            r = float(calc_rad(row['mag'])) * args.scaleR
            point = find_free(point, name, font_family, image, r, row['hip'])
            if point:
                chart.text((point['x'], point['y']), name, font=font_family, fill=label)
        counter += 1
        progress(counter, len(data))
    
    console('writing ngc labels...')
    counter = 0
    for row in ngc:
        if row['mag'] <= args.ngc_max:
            point = row['point']
            name = row['name']
            font_family = row['font']
            if name != '':
                # point = find_free(point, name, font_family, image, 10 * args.scaleR, '')
                if point:
                    chart.text((point['x'], point['y']+9), name, font=font_family, fill=black)
        counter += 1
        progress(counter, len(ngc))
        
def drawEcliptic(chart, args):
    coseps = math.cos(rads*23.439)
    sineps = math.sin(rads*23.439)
    prev = None
    for d in range(0, 361):
        i = float(d) / 15
        delta = math.asin(sineps * math.sin(i*rads*15))*(180/math.pi)
        point = get_coords(i, delta, args)
        if point:
            m = 3
            x = point['x'] - m * args.scaleR
            y = point['y'] - m * args.scaleR
            x1 = point['x'] + m * args.scaleR 
            y1 = point['y'] + m * args.scaleR
            
            chart.ellipse((x, y, x1, y1), fill=red)
            
            if prev:
                chart.line([(point['x'], point['y']), (prev['x'], prev['y'])], fill=red, width=args.ecliptic_line_width)
            
            prev = point
        
            
    
def drawBorders(draw, args):
    boundaries = get_boundaries()
    current = ''
    prev = None
    count = len(boundaries)
    cur = 0
    for row in boundaries:
        coords = get_coords(row['ra'], row['dec'], args)
        
        if coords and prev:
            if row['con'] == current:
                draw.line([(prev['x'], prev['y']), (coords['x'], coords['y'])], fill=lightblue, width=args.con_line_width)
            
        current = row['con']
        prev = coords
        cur += 1
        progress(cur, count)

def drawPolarFigures(draw, args):
    current = ''
    lines = get_figures()
    count = 0
    for row in lines:
        start = get_coords(row['startRa'], row['startDec'], args)
        if row['startDec'] > -60 and row['endDec'] > -60:
            if start != None:
                end = get_coords(row['endRa'], row['endDec'], args)
                if end != None:
                    draw.line([(start['x'], start['y']), (end['x'], end['y'])], fill=lightgreen, width=args.figure_line_width)
            count += 1
            progress(count, len(lines))

def drawRAFigures(draw, args):
    current = ''
    lines = get_figures()
    count = 0
    for row in lines:
        start = get_coords(row['startRa'], row['startDec'], args)
        if row['startRa'] > args.ra-3 and row['endRa'] < args.ra+3:
            if start != None:
                end = get_coords(row['endRa'], row['endDec'], args)
                if end != None:
                    draw.line([(start['x'], start['y']), (end['x'], end['y'])], fill=lightgreen, width=args.figure_line_width)
            count += 1
            progress(count, len(lines))

#def drawFigures2(draw, args):
#    current = ''
#    lines = get_figures()
#    count = 0
#    for row in lines:
#        start = get_coords(row['startRa'], row['startDec'], args)
#        end = get_coords(row['endRa'], row['endDec'], args)
#        line = line_eq(start, end)
#        for 
#            draw.line([(start['x'], start['y']), (end['x'], end['y'])], fill=lightgreen)
#        count += 1
#        progress(count, len(lines))

def line_eq(start, end):
    # y = mx + b
    m = (end['y'] - start['y']) / (end['x'] - start['x'])
    # b = y - mx
    b = start['y'] - (m * start['x'])
    return (m, b)
    
def drawNames(draw, args):
    names = get_names()
    count = 0
    for name in names:
        coords = get_coords(name['ra'], name['dec'], args)
        if coords:
            draw.text((coords['x'], coords['y']), name['name'], font=con_font, fill=orange)
        count += 1
        progress(count, len(names))

ONE_TWELFTH = Decimal(1)/Decimal(12)
def drawDeclinationLines(draw, args):
    prev = None
    decs = 0
    label_step = 12
    dec = Decimal(-90)
    end = Decimal(90)
    step = Decimal(10)
    if args.type == 'stereo':
        dec = Decimal(-60)
        end = Decimal(61)
        ra = args.ra - 3
        endra = args.ra + 3
    elif args.type == 'gnomonic':
        console('%s' % (args.dec))
        dec = math.trunc(args.dec - 20)
        end = math.trunc(args.dec + 20)
        ra = args.ra - 1
        endra = args.ra + 1
        label_step = 12
    elif args.type == 'polar':
        if args.dec == 90:
            dec = -60
            end = 81
        elif args.dec == -90:
            dec = -80
            end = -49
        ra = 0
        endra = 24
    count = end - dec
    
    #console('%s %s %s %s' % (dec, end, ra, endra))
    
    # draw lines every 10 degrees
    for de in range(dec, end, step):
        r = ra
        #console("ra: %s de: %s " % (ra,de))
        prev = None
        ctr = 0
        while r <= endra:
            
            #console("ra: %s dec: %s                      %s" % (ra, de, ONE_TWELFTH))
            point = get_coords(r, de, args)
            if point and prev:
                draw.line([(prev['x'], prev['y']), (point['x'], point['y'])], fill=gray, width=args.tick_width)
                
            
            if ctr % label_step == 0:
                rh = round(r, 0)
                #rm = round(60 * (r - math.trunc(r)))
                draw.text((point['x'] - 20, point['y'] - 15), u'%sh' % (rh), font=arial, fill=gray, width=args.tick_width)
            r += float(ONE_TWELFTH)
            ctr += 1
            prev = point
    
    # draw ticks every degree
    for de in range(dec, end):
        rac = 0
        r = ra
        prev = None
        while r <= endra:
            point = get_coords(r - .025, de, args)
            point2 = get_coords(r + .025, de, args)
            if point and point2 and prev:
                draw.line([(point['x'], point['y']), (point2['x'], point2['y'])], fill=gray, width=args.tick_width)
                
            prev = point2
            r += 1
            rac += 1
            
        decs += 1
        progress(decs, count)
           
def drawRaLines(draw, args):
    prev = None
    counter = 0
    ra = 0
    end = Decimal(23)
    step = Decimal('0.2')
    label_step = 10
    
    if args.type == 'stereo':
        ra = Decimal(args.ra - 3)
        end = Decimal(args.ra + 3)
        sdec = Decimal(-60)
        edec = Decimal(61)
    elif args.type == 'gnomonic':
        ra = Decimal(args.ra - 1)
        end = Decimal(args.ra + 1)
        sdec = Decimal(args.dec - 20)
        edec = Decimal(args.dec + 20)
        label_step = 1
    elif args.type == 'polar':
        if args.dec == 90:
            sdec = Decimal(-60)
            edec = Decimal(81)
        elif args.dec == -90:
            sdec = Decimal(-80)
            edec = Decimal(-49)
    
    count = end - ra
    r = ra
    # draw lines every hour
    while r <= end:
        prev = None
        for de in range(sdec, edec, 1):
            point = get_coords(float(r), float(de), args)
            if point and prev:
                draw.line([(prev['x'], prev['y']), (point['x'], point['y'])], fill=gray, width=args.tick_width)
                if de % label_step == 0:
                    rh = math.trunc(r)
                    rm = math.trunc(60 * (r - math.trunc(r)))
                    draw.text((point['x'] + 10, point['y'] + 10), u'%s\u00b0' % (de), font=arial, fill=gray, width=args.tick_width)
            prev = point
        counter += 1
        r += Decimal(1)
    
    counter = 0
    r = ra
    # draw ticks every 5 minutes
    while r <= end:
        #prev = None
        for de in range(sdec, edec, 10):
            point = get_coords(float(r), float(de - step), args)
            point2 = get_coords(float(r), float(de + step), args)
            if point and point2:
                draw.line([(point['x'], point['y']), (point2['x'], point2['y'])], fill=gray, width=args.tick_width)
            #prev = point2
        counter += 1
        r += ONE_TWELFTH
        progress(counter, Decimal(count * 12))
        
    return

    
def get_coords(ra, dec, args):
    #point = globals()[args.type](ra, dec, args.ra, args.dec, filter)
    point = None
    if (args.type == 'stereo'):
        point = stereo(ra, dec, args.ra, args.dec, args.filter)
    elif (args.type == 'gnomonic'):
        point = gnomonic(ra, dec, args.ra, args.dec, args.filter)
    elif (args.type == 'polar'):
        point = polar(ra, dec, args.ra, args.dec, args.filter)
    if point != None:
        transform(point, args)
    return point
    
def stereo(r, d, ra, dec, filter):
    if filter and (r > ra + 3 or r < ra - 3 or d > 60 or d < -60):
        return None
        
    r = r - ra
    
    r_rads = r * rads * fifteen
    d_rads = d * rads
    
    x = float(math.cos(d_rads) * math.sin(r_rads))
    y = float(math.sin(d_rads))
    z = float(math.cos(r_rads) * math.cos(d_rads))
    
    X1 = float(-1 * x / (1 + z))
    Y1 = float(-1 * y / (1 + z))
        
    return {'x': X1, 'y': Y1}
    
def polar(ra, dec, base_ra, base_dec, filter):
    if filter:
        if (base_dec == 90 and dec < -60) or (base_dec == -90 and dec > -50):
            return None
        
    r = float(ra) * rads * 15
    d = (base_dec - float(dec)) * rads
    
    x1 = d * float(math.cos(r))
    y1 = d * float(math.sin(r))
    
    return {'x': x1, 'y': y1}

def gnomonic(ra, dec, base_ra, base_dec, filter):
    #inside = ra < base_ra + cmax and ra > base_ra - cmax and dec > base_dec - args.fov and dec < base_dec + args.fov
    #if filter and not inside:
    #    return None
        
    lam = ra * 15 * rads
    chi = dec * rads
    lam0 = base_ra * 15 * rads
    
    chi1 = base_dec * rads
    c = float(math.sin(chi) * math.sin(chi1) + math.cos(chi) * math.cos(chi1) * math.cos(lam - lam0))
    
    if filter and c < cmax:
        return None
        
    x1 = math.cos(chi) * math.sin(lam - lam0) / math.cos(c * rads)
    y1 = ((math.cos(chi1) * math.sin(chi)) - (math.sin(chi1) * math.cos(chi) * math.cos(lam - lam0))) / math.cos(c * rads)
    
    return {'x': -1 * x1, 'y': -1 * y1}
    
def transform(point, args):
    globals()['transform_' + args.type](point, args)
    
def transform_stereo(point, args):
    x = point['x']
    y = point['y']
    
    point['x'] = (x * args.width * args.factor) + (args.width * args.factor / 2)
    point['y'] = (y * args.width * args.factor) + (args.height * args.factor / 2)
    
def transform_polar(point, args):
    x = point['x']
    y = point['y']
    
    point['x'] = (x * args.width * args.factor) + (args.width  / 2)
    point['y'] = (y * args.width * args.factor) + (args.height / 2)
    
def transform_gnomonic(point, args):
    x = point['x']
    y = point['y']
    
    #scale = .75 * args.width * args.factor / (args.fov * rads / 2)
    scale =  cmax * args.factor * args.width / (args.fov * rads)
    
    point['x'] = (x * scale) + (args.width * args.factor / 2)
    point['y'] = (y * scale) + (args.width * args.factor / 2)
    
    
def find_free(point, text, font, image, r, hip):
    free = False
    a = point['x']
    b = point['y']
    metrics = font.getsize(text)
    width, height = image.size
    
    #if a + metrics[0] >= width or b + metrics[1] >= height:
    #    return point
    
    while not free:
        r += 1
        if r > args.rmax:
            return None
        for j in range(0, 360, 5):
            a = math.trunc(point['x'] + r * float(math.cos(j * rads)))
            b = math.trunc(point['y'] + r * float(math.sin(j * rads)))
            if a < point['x']:
                a = a - metrics[0]
            
            for x1 in range(a, a + metrics[0]):
                for y1 in range(b, b + metrics[1] ):
                    if x1 >= width or y1 >= height or x1 <= 0 or y1 <= 0:
                        break#return point
                    
                    pixel = image.getpixel((x1, y1))
                    
                    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0 and pixel[3] == 0:
                        free = True
                    elif (pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0) and pixel[3] != 0:
                        free = True
                    else:
                        free = False
                        break
                if not free:
                    break
            if free:
                break 
        
    coords = {}
    coords['x'] = a
    coords['y'] = b
    return coords
    
    

def fix(name):    
    name = alp.sub(u'\u03b1', name, 1)
    name = bet.sub(u'\u03B2', name, 1)
    name = gam.sub(u'\u03B3', name, 1)
    name = delt.sub(u'\u03B4', name, 1)
    name = eps.sub(u'\u03B5', name, 1)
    name = zet.sub(u'\u03B6', name, 1)
    name = eta.sub(u'\u03B7', name, 1)
    name = iot.sub(u'\u03B9', name, 1)
    name = the.sub(u'\u03B8', name, 1)
    name = kap.sub(u'\u03BA', name, 1)
    name = lam.sub(u'\u03BB', name, 1)
    name = mu.sub(u'\u03BC', name, 1)
    name = nu.sub(u'\u03BD', name, 1)
    name = xi.sub(u'\u03BE', name, 1)
    name = omi.sub(u'\u03BF', name, 1)
    name = pi.sub(u'\u03C0', name, 1)
    name = rho.sub(u'\u03C1', name, 1)
    name = sig.sub(u'\u03C3', name, 1)
    name = tau.sub(u'\u03C4', name, 1)
    name = ups.sub(u'\u03C5', name, 1)
    name = phi.sub(u'\u03C6', name, 1)
    name = chi.sub(u'\u03C7', name, 1)
    name = psi.sub(u'\u03C8', name, 1)
    name = ome.sub(u'\u03C9', name, 1)
    
    return name
    
def calc_rad(mag):
    if mag >= 12:
        return .5
    if mag >= 10:
        return .5
    if mag >= 9:
        return .5
    if mag >= 8:
        return 1
    if mag >= 7:
        return 1
    if mag >= 6:
        return 2
    if mag >= 5:
        return 2
    if mag >= 4:
        return 3
    if mag >= 3:
        return 3
    if mag >= 2:
        return 3
    if mag >= 1:
        return 5
    if mag >= 0:
        return 6
    if mag >= -1:
        return 8
    if mag >= -2:
        return 10

def get_ngc(args):
    rows = list()
    
    ngc = open('data/ngc.csv')
    
    ngccount = 0
    for line in ngc:
        cols = line.split(',')
        type = cols[22]
        
        name = ''
        if cols[24].find('"M ') != -1:
            name = cols[24].replace('"', '')
        else:
            name = cols[0] + cols[1]
        ra = ngc_ra(cols[8], cols[9], cols[10])
        dec = ngc_dec(cols[11], cols[12], cols[13], cols[14])
        if cols[16] == '':
            cols[16] = 99
            
        mag = float(cols[16])
        
        coords = get_coords(ra, dec, args)
        font = arial_small
        prox = '999'
        if coords:
            row = {'name': name, 'con': '', 'point': coords, 'mag': mag, 'font': font, 'prox': prox, 'hip': ''}
            rows.append(row)
            ngccount+=1
                
    console("returning %s ngc objects" % (ngccount))
        
    return rows

def ngc_ra(h, m, s):
    ra = float(h)
    min = float(m) / 60
    sec = float(s) / 60 / 60
    return ra + min + sec
    
def ngc_dec(hem, d, m, s):
    dec = 0
    deg = float(hem + d)
    min = float(m) / 60
    sec = float(s) / 60 / 60
    if deg < 0:
        return deg - min - sec
    else:
        return deg + min + sec


        

if __name__ == '__main__':
    if sys.platform == "win32":
        import os, msvcrt
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    main(sys.argv[1:])