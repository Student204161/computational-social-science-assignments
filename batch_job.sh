#!/bin/sh
#BSUB -J pls_work
#BSUB -W 5:00
#BSUB -n 1
#BSUB -R "select[model == XeonE5_2660v3]"
#BSUB -R "rusage[mem=100GB]"
#BSUB -B
#BSUB -N
#BSUB -u s204161@student.dtu.dk
#BSUB -o out_test_ssh.out
#BSUB -e err_test_ssh.err

module load cuda/11.6

source /work3/s204161/miniconda/bin/activate base

cd /zhome/a7/0/155527/Desktop/s204161/Computational-Social-Science-Exercises/week2/

python extract_scientist_data.py
