#!/bin/bash
#SBATCH --job-name=ghz_cpu_timing
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=03:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=rf5447@princeton.edu
#SBATCH --output=ghzcputiming_%j.out
#SBATCH --error=ghzcputiming_%j.out

module purge
module load anaconda3/2024.10

/usr/bin/time -v ./.venv/bin/python3 -u ghzcputiming_includingwarmup.py