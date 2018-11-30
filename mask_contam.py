from sys import *
from Bio import Seq, SeqRecord, SeqIO
import csv

# Idea by Ben Voigt in https://stackoverflow.com/questions/32869247/a-container-for-integer-intervals-such-as-rangeset-for-c
def sort_condense(ivs):
    if len(ivs) == 0:
        return []
    if len(ivs) == 1:
        if ivs[0][0] > ivs[0][1]:
            return [(ivs[0][1], ivs[0][0])]
        else:
            return ivs
    eps = []
    for iv in ivs:
        ivl = min(iv)
        ivr = max(iv)
        eps.append((ivl, False))
        eps.append((ivr, True))
    eps.sort()
    ret = []
    level = 0
    i = 0
    while i < len(eps)-1:
        if not eps[i][1]:
            level = level+1
            if level == 1:
                left = eps[i][0]
        else:
            if level == 1:
                if (not eps[i+1][1]
                   and eps[i+1][0] == eps[i][0]+1):
                    i = i+2
                    continue
                right = eps[i][0]
                ret.append((left, right))
            level = level-1
        i = i+1
    ret.append((left, eps[len(eps)-1][0]))
    return ret

arg = argv[1]
contams = {}
reader = csv.DictReader(open(arg), delimiter='\t')
for row in reader:
    sacc = row.get('saccver')
    if sacc is None or len(sacc) == 0:
        continue
    sstart = row['sstart']
    send = row['send']
    if len(sstart) == 0:
        print("interval start missing, row: {}".format(row),
                file=stderr, flush=True)
        exit(-1)
    if len(send) == 0:
        print("interval end missing, row: {}".format(row),
                file=stderr, flush=True)
        exit(-1)
    if contams.get(sacc) is None:
        l = []
        l.append((int(sstart), int(send)))
        contams[sacc] = l
    else:
        contams[sacc].append((int(sstart), int(send)))

recs = SeqIO.parse(stdin, 'fasta')
seqs = []
for s in recs:
    i = s.name.find(' ')
    intervals = contams.get(s.name)
    if intervals is None or len(intervals) == 0:
        seqs.append(s)
        continue
    intervals = sort_condense(intervals)
    do_write = False
    if (intervals[0][0] >= 100
       or len(s.seq) - intervals[len(intervals)-1][1] >= 100):
        do_write = True
    else:
        for i in range(len(intervals)-1):
            size = intervals[i+1][0] - intervals[i][1]
            if size >= 100:
                seq = str(s.seq)[intervals[i][1] : intervals[i+1][0]]
                maxok = 0
                ok = 0
                for c in seq:
                    if c in 'ACGT':
                        ok = ok+1
                    else:
                        if ok > maxok:
                            maxok = ok
                        ok = 0
                if ok > maxok:
                    maxok = ok
                if maxok >= 100:
                    do_write = True
                    break
    if do_write:
        seq = str(s.seq)
        for iv in intervals:
            seq = seq[:iv[0]] + 'N'*(iv[1]-iv[0]+1) + seq[iv[1]+1:]
        s.seq = Seq.Seq(seq)
        seqs.append(s)
    else:
        print(s.name, file=stderr, flush=True)

SeqIO.write(seqs, stdout, 'fasta')
