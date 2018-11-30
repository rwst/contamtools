from sys import *
import csv
import operator

reader = csv.DictReader(stdin, delimiter='\t')
sortedlist = sorted(reader, key=lambda d: d['saccver'])
sortedlist = sorted(sortedlist, key=lambda d: d['qaccver'])
writer = csv.DictWriter(stdout, fieldnames=reader.fieldnames, delimiter='\t')
writer.writeheader()
writer.writerows(sortedlist)
