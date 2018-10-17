from sys import *
from Bio import Seq, SeqRecord, SeqIO
import csv

accmap = {}
reader = csv.DictReader(stdin, delimiter='\t')
for row in reader:
    saccver = row.get('saccver')
    if saccver is None or len(saccver) == 0:
        continue
    print(saccver, file=stderr, flush=True)
    if accmap.get(saccver) is None:
        accmap[saccver] = []
    accmap[saccver].append(row)

writer = csv.DictWriter(stdout, fieldnames=reader.fieldnames, delimiter='\t')
writer.writeheader()

def outside_of(row, mrow):
    if row is mrow:
        return False
    rowl = min(int(row['sstart']), int(row['send']))
    rowr = max(int(row['sstart']), int(row['send']))
    mrowl = min(int(mrow['sstart']), int(mrow['send']))
    mrowr = max(int(mrow['sstart']), int(mrow['send']))
    return (rowr-100 < mrowl
        or rowl+100 > mrowr
        or (row['qaccver'] == mrow['qaccver']
            and (rowl < mrowl or rowr > mrowr)))

for sacc, lst in accmap.items():
    while len(lst) > 0:
        mrow = max(lst, key=lambda row: int(row['bitscore']))
        lst = [row for row in lst if outside_of(row, mrow)]
        writer.writerow(mrow)
