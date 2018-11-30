blastn -query /home/ralf/krakendir/UniVec/library/UniVec/library.fna -db genome -evalue 1e-80 -outfmt 6 std slen |sed 's+kraken:taxid|28384|gnl|uv|++g' >t.tsv
