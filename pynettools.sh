#!/bin/sh
#
# pynettools.sh
# 2023-06-17 | CR
#
cd "`dirname "$0"`" ;
SCRIPTS_DIR="`pwd`" ;
python3 -m src.pynettools_main --input hostname_mac.txt $1 $2 $3 $4 $5 $6 $7 $8 $9
