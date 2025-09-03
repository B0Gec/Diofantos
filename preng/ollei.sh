#!/bin/bash
#SBATCH --job-name=test
##SBATCH --partition=long
##SBATCH --time=14-00:00:00
##SBATCH --time=00:10:00
#SBATCH --time=2-00:00:00
#SBATCH --mem-per-cpu=5GB
#SBATCH --time=01:10:00
##SBATCH --mem-per-cpu=100MB
##SBATCH --cpus-per-task=1
#SBATCH --array=0-1000  # 1001 is upper limit
#SBATCH --array=0-1
##SBATCH --array=0-1000
#SBATCH --output=./joeis%A_%a.out 
#SBATCH --output=./oeis/preng/results/%x/%A/%5a.out

echo "=============================================="

echo "Starting time (of array_subjob "$SLURM_JOB_NAME"_"$SLURM_ARRAY_JOB_ID"_"$SLURM_ARRAY_TASK_ID"):"
date

# $1=batch (0-34); $2=dir_id
# pip install pysindy sympy numpy diophantine pandas

#cd oeis/
cd oeis/preng/
#singularity exec ../pg.sif python3 doones.py --job_id $SLURM_ARRAY_JOB_ID \
#singularity exec ../oeis.sif python3 doones.py \
#singularity exec ../../oeis.sif python3 hpc_testset.py \
# singularity exec ../../oeis.sif python3 oll_extract.py \
#         --task_id $(($1*1000 + $SLURM_ARRAY_TASK_ID)) --exper_id $2 >> results/$2/0$1$SLURM_ARRAY_TASK_ID.txt

task_id=$(($1*1000 + $SLURM_ARRAY_TASK_ID))
fill=00000$task_id
prefix=${fill: -5}

singularity exec ../../oeis.sif python3 oll_extract.py \
        --task_id $(($1*1000 + $SLURM_ARRAY_TASK_ID)) > results/$SLURM_JOB_NAME/$prefix.txt 2>&1


date

#echo mv results/$SLURM_JOB_NAME/$SLURM_ARRAY_JOB_ID/$filename results/$SLURM_JOB_NAME/$filename


echo "this is oei.sh $1 $2 $3 $4 $5 $6 $7 doing \
  doones job_id $SLURM_ARRAY_JOB_ID task_id $1 * 1000 + $SLURM_ARRAY_TASK_ID --exper_id $2"

# usage, e.g.:  #sbatch --job-name=obat-dasco25-10k_eval4 --array=0-0%1 runlloei.sh 1 10

