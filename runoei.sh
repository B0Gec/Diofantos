#!/bin/bash
#SBATCH --job-name=run_arrays
#SBATCH --time=14-00:00:00
#SBATCH --time=2-00:00:00
#SBATCH --mem-per-cpu=1GB
#SBATCH --cpus-per-task=1
#SBATCH --array=0-34
#SBATCH --array=0-2  #buglist
#SBATCH --output=./run_batch%A.out

date

sbatch oei.sh $SLURM_ARRAY_TASK_ID $SLURM_ARRAY_JOB_ID $1 $2 $3 $4 $5


echo "this is runoei.sh $1 $2 $3 $4 $5 $6 $7"
date
