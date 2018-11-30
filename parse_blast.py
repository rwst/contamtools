from sys import *
from Bio import Seq, SeqIO, SeqRecord
from Bio.Blast import NCBIXML

def get_os(al):
    s = al.title
    os = s.find('OS=')
    sp = s.find('=', os+3)
    if s[sp-4] == ' ':
        sp = sp-4
    elif s[sp-3] == ' ':
        sp = sp-3
    else:
        sp = sp-2
    return s[os+3:sp]

def get_lab(s):
    lb = s.find('[')
    rb = s.find(']')
    rbs = s.rfind('-', lb, rb)
    ll = s.rfind('_', 0, lb)
    return (s[ll+1:lb-1], int(s[lb+1:rbs-1]), int(s[rbs+1:rb]))

sra = 'SRR001044'
favs = {}
hits = []
lfdnr = argv[1]
hdl = open('node_{}.orf'.format(lfdnr), 'r')
orfrecs = SeqIO.parse(hdl, format='fasta')
orfs = {}
for seq in orfrecs:
    orfs[seq.description] = seq.seq
hdl = open('node_{}.blast.xml'.format(lfdnr), 'r')
brecs = NCBIXML.parse(hdl)
for brec in brecs:
    if len(brec.alignments) == 0:
        continue
    if len(brec.alignments) == 1:
        favs[(get_os(brec.alignments[0]))] = 0
    (label, n1, n2) = get_lab(brec.query)
    hits.append((brec.query, label, n1, n2, brec.alignments))
for (q,_,_,_,a) in hits:
    print(q)
    for al in a:
        f = get_os(al)
        n = favs.get(f)
        if not n is None:
            favs[f] = n+1
mi = 0
top1 = None
top2 = None
for (f,n) in favs.items():
    if n > mi:
        top1 = f
        top2 = None
        mi = n
    elif n == mi:
        top2 = f
outrecs = []
print('Top: {}'.format(top1), file=stderr)
if top2:
    print('Top2: {} (both n={})'.format(top2, mi), file=stderr)
for (query, orf, n1, n2, a) in hits:
    seq = orfs.get(query)
    if not seq:
        print('query not found in orfs!', file=stderr)
        exit()
    seqr = SeqRecord.SeqRecord(seq,
            id='{}.CTG{}.ORF{}'.format(sra, lfdnr, orf))
    seqr.description = 'Hypothetical protein from {}'.format(sra)
    outrecs.append(seqr)
    #print('{} {}-{} {} {}'.format(label, n1, n2, al.hsps[0].expect, al.hit_def))
SeqIO.write(outrecs, 'node_{}_hits.fasta'.format(lfdnr), format='fasta')
