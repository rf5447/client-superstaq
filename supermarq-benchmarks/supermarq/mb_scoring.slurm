#!/bin/bash
#SBATCH --job-name=mb_scoring      # Name in the queue
#SBATCH --nodes=1                  # Run on a single node
#SBATCH --ntasks=1                 # Run a single task
#SBATCH --cpus-per-task=1          # Use 1 CPU core
#SBATCH --mem=16G                  # Request 16GB of RAM
#SBATCH --time=00:15:00            # Max runtime (15 mins)
#SBATCH --output=mb_out_%j.log     # Standard output and error log

# 1. Clean the environment (best practice on Della)
module purge

# 2. Move to the directory where your script and venv live
cd /home/rf5447/client-superstaq/supermarq-benchmarks/supermarq/

# 3. Activate your specific venv
source .venv/bin/activate

# 4. Run your python script
# We use 'python' instead of 'python3' usually once venv is active
python mb_scoring.py