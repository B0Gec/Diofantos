#!/bin/bash
#jobid="37683622"
jobid="37117747"  # 23k succ
jobid="32117747"
output="succs_$jobid.txt"
#echo $jobid output
ls oeis/results/$jobid >> $output
for i in {0..4}; do cat $output | grep 0$i..._ | head -n1 ; done
echo - - -
for i in {5..9}; do cat $output | grep 0$i..._ | head -n1 ; done
echo - - -
for i in {10..14}; do cat $output | grep $i..._ | head -n1 ; done
echo - - -
for i in {15..19}; do cat $output | grep $i..._ | head -n1 ; done
echo - - -
for i in {20..24}; do cat $output | grep $i..._ | head -n1 ; done
echo - - -
for i in {25..29}; do cat $output | grep $i..._ | head -n1 ; done
echo - - -
for i in {30..34}; do cat $output | grep $i..._ | head -n1 ; done
