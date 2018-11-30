for i in UniVec plasmid viral bacteria archaea fungi mouse human; do echo $i; kraken2 --db $i --threads 4 --use-names --classified-out $i.fa --confidence 0.5 tt.fa |grep ^C >$i.txt; done
