#!/bin/bash
#SBATCH --job-name=oeis_array_slurms
##SBATCH --time=14-00:00:00
##SBATCH --time=00:10:00
#SBATCH --time=2-00:00:00
##SBATCH --partition=long
#SBATCH --mem-per-cpu=5GB
##SBATCH --cpus-per-task=1
#SBATCH --array=0-35000
#SBATCH --array=0-5000
#SBATCH --array=0-1000
#SBATCH --array=0-999
##SBATCH --array=0-500
##SBATCH --array=0-50
##SBATCH --array=0-2
#SBATCH --array=0-0
#SBATCH --output=./joeis%A.out
####SBATCH --output=./MLJ23/results/slurm/parestim_sim/e0/slurm_output_%A_%a.out

echo "=============================================="

echo "Starting time (of array_subjob "$SLURM_ARRAY_JOB_ID"_"$SLURM_ARRAY_TASK_ID"):"
date
touch $SLURM_ARRAY_JOB_ID$0.txt

ingularity exec ../pg.sif python3 doones.py --job_id $SLURM_ARRAY_JOB_ID --task_id $(($1*1000 + $SLURM_ARRAY_TASK_ID))

date

echo "this is $0 $1 $2 $3 $4 $5 $6 $7"
