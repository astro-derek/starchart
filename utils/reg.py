import re

alp = re.compile(r'.*Alp')

print alp.sub('33 Alp', '\u03b1')