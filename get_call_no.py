import re

set = ['MD650.D12 2022', 'F1111 .G14 .E100 2010', 'F700 .T16 1999', 'GP1992 .A45 .F1201 1970']

# Discriminate by LC series number
for s in set:
    if s[:1] == 'F':
        print(s)

# Isolate the class number
for s in set:
    s = s.split('.')[0]
    s = s.strip()
    s = re.sub('\D', '', s)
    print(s)