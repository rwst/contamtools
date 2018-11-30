from sys import *
import csv

arg = argv[1]
taxid = argv[2]
ccmap = set()
reader = open('ccont.txt', 'r')
for s in reader.readlines():
    ccmap.add(s.rstrip())
reader = csv.DictReader(stdin, delimiter='\t')
writer = csv.DictWriter(stdout, fieldnames=reader.fieldnames, delimiter='\t')
writer.writeheader()
for row in reader:
    saccver = row.get('saccver')
    if saccver is None or len(saccver) == 0:
        continue
    if saccver in ccmap:
        row['Comment'] = 'completely contaminated'
    row['Taxid'] = taxid
    writer.writerow(row)

