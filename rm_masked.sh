#!/bin/sh
sed -n '
/^>N/ {
    N
        /\n.*[AGCT]/ p
    }'
