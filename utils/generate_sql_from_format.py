import sys

def generate_sql_from_format(filename):
    data = open(filename).readlines()
    print 'create table %s (\n' % (filename)
    for line in data:
        name = line[22:33]
        name = name.replace('-', '_')
        name = name.replace(':', '_')
        name = name.replace('(', '')
        name = name.replace(')', '')
        format = 'numeric,'
        fmt = line[10:16]
        if fmt.strip().startswith('A'):
            format = 'char(%s),' % (fmt[1:])
        print '%s %s' % (name, format)
    print ')'
filename = sys.argv[1]
generate_sql_from_format(filename)