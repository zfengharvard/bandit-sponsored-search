#!/bin/bash
#SBATCH -n 30 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 7-00:00 # Runtime in D-HH:MM
#SBATCH -p shared # Partition to submit to
#SBATCH --mem=100000# Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o winexp_%j.out # File to which STDOUT will be written
#SBATCH -e winexp_%j.err # File to which STDERR will be written

#module load python
module load python/2.7.11-fasrc01
source activate charapod
python runner-dp.py
