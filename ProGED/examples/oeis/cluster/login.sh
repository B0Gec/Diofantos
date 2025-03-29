#!/bin/bash
# This is script for login node.

# git clone --branch ode https://github.com/brencej/ProGED

# cp ProGED/ProGED/examples/oeis/cluster/login.sh .

# cp ProGED/ProGED/examples/oeis/fibonacci_oneby1.py .
# cp ProGED/ProGED/examples/oeis/oeis_selection.csv .
# cp ProGED/ProGED/examples/oeis/cluster/play.sh .
# # cp ProGED/ProGED/examples/oeis/cluster/arcsuball.sh .
# cp ProGED/tests/test_core.py .

# cp ProGED/ProGED/examples/oeis/cluster/submit.xrsl . &&

cp ~/ProGED/ProGED/examples/oeis/fibonacci_oneby1.py ~/remoteserv/
cp ~/ProGED/ProGED/examples/oeis/oeis_selection.csv ~/remoteserv/
cp ~/ProGED/ProGED/examples/oeis/cluster/play.sh ~/remoteserv/
cp ~/ProGED/tests/test_core.py ~/remoteserv/
cp ~/ProGED/ProGED/examples/oeis/cluster/submit.xrsl ~/remoteserv/


#old:
# general=soeis-
# direct=direct
# order=ord
# function sedply () {
# name=$general$3'-'$order$1$direct$2
# cat submit.xrsl \
# 	| sed 's/play.sh/'$name'.sh/' \
# 	| sed 's/generic jobname/'$name'/' \
# 	> $name.xrsl
# cat play.sh  \
# 	| sed 's/--order=\w/--order='$1'/' \
# 	| sed 's/--is_direct=\w\+/--is_direct='$2'/' \
#        	| sed 's/--sample_size=\w\+/--sample_size='$3'/' \
# 	> $name.sh
# }
# sedply 4 False 100 
# sedply 2 False 100 
# sedply 4 True 100 
# sedply 2 True 100 
# sedply 0 True 100 

# for i in $general*.xrsl; do echo arcsub -c nsc.ijs.si -d info $i; done
# for i in $general*'-'$order*$direct*.xrsl; do echo arcsub -c nsc.ijs.si -d info $i; done

# cat play.sh | sed 's/--sample_size=\w\+/--sample_size=100/' | sed 's/--order=\w/--order=2/' | sed 's/--is_direct=\w\+/--is_direct=True/' >> $ord4nodir.sh


submitfile=submit.xrsl
scriptfile=play.sh
echo "inside "$submitfile" :"
cat $submitfile | grep $submitfile
echo "inside "$scriptfile" :"
cat $scriptfile | grep $submitfile

echo " "
echo "Next steps: "
# echo "edit "$ord4nodir
# echo "edit "$scriptfile
# echo "arcsub -c cluster.net soeis100-ord4directFalse.sh"
echo "arcsub -c cluster.net play.sh"
# or
# ars submit.xrsl  # ars is in myarcrunner/

