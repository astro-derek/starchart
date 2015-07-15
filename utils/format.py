import os
import sys

filename = sys.argv[1]
input = open(filename)
print 'drop table %s;' % (filename)
print 'create table %s (' % (filename)

copies = list()
for line in input.readlines():
    format = line[10:16]
    
    fmt = 'numeric'
    if format.startswith('A'):
        fmt = 'char(' + format[1:] + ')'
    col_name = line[24:33]
    col_name = col_name.replace(':', '_')
    col_name = col_name.replace('-', '_')
    col_name = col_name.replace('(', '')
    col_name = col_name.replace(')', '')
    print col_name + ' ' + fmt + ','
print ');\n'
