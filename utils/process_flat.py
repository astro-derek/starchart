import sys


input = open(sys.argv[1])

format_data = open(sys.argv[2]).readlines()
format = list()
for row in format_data:
    start = row[0:4]
    end = row[5:8]
    if start.strip() == '':
        start = end
    start = int(start) - 1
    end = int(end) - 1
    format.append({'start': start, 'end': end})

line = input.readline().rstrip()
while line != '':
    columns = list()
    for column in format:
        columns.append(line[column['start'] : column['end'] + 1])
    print '|'.join(columns)
    line = input.readline().rstrip()
    