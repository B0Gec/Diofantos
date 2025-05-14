#!/bin/bash
#SBATCH --job-name=test
##SBATCH --partition=long
##SBATCH --time=14-00:00:00
#SBATCH --time=2-00:00:00
#SBATCH --time=00:30:00
#SBATCH --time=00:10:00
##SBATCH --mem-per-cpu=100MB
#SBATCH --mem-per-cpu=2500MB
#SBATCH --mem-per-cpu=4500MB
#SBATCH --mem-per-cpu=5GB
##SBATCH --cpus-per-task=1
#SBATCH --array=0-1
#SBATCH --array=9-9  # fibo in Linrec
#SBATCH --array=200-1000 
#SBATCH --array=100-200  
#SBATCH --array=0-1000  # 1001 is upper limit
#SBATCH --array=0-1
#SBATCH --output=./joeis%A.out

echo "=============================================="

echo "Starting time (of array_subjob "$SLURM_ARRAY_JOB_ID"_"$SLURM_ARRAY_TASK_ID"):"
date

# $1=batch (0-34); $2=dir_id
# pip install pysindy sympy numpy diophantine pandas

cd oeis/
#singularity exec ../pg.sif python3 doones.py --job_id $SLURM_ARRAY_JOB_ID \
# singularity exec ../oeis.sif python3 doones.py \
singularity exec ../oeis.sif python3 bug_dasco_zeroterms.py \
        --task_id $(($1*1000 + $SLURM_ARRAY_TASK_ID)) --exper_id $2

date

echo "this is oei.sh $1 $2 $3 $4 $5 $6 $7 doing \
  doones job_id $SLURM_ARRAY_JOB_ID task_id $1 * 1000 + $SLURM_ARRAY_TASK_ID --exper_id $2"
