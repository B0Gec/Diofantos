#!/bin/bash -i
# This is script for login node.
source ~/login.sh
ars $ord0dir &&
ars $ord2dir &&
ars $ord4dir &&
ars $ord2nodir &&
ars $ord4nodir
# for i in $general$order[024]-*$direct".xrsl"; do echo ars $i; done
