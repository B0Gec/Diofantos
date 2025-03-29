#!/bin/bash
#SBATCH --job-name=VDPv1
#SBATCH --time=2-00:00:00
#SBATCH --mem-per-cpu=2GB
#SBATCH --array=0-9
#SBATCH --cpus-per-task=1

singularity exec proged_container.sif python3.7 slurm_run_batch.py ${SLURM_ARRAY_TASK_ID}