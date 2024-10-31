#!/bin/bash
#SBATCH --job-name=JJ_Cellbender              # Job name
#SBATCH --partition=defq                      # Partition to run the job on
#SBATCH --nodelist=sabercore-a30-001          # Request A30 nodes specifically
#SBATCH --ntasks=1                            # Number of tasks
#SBATCH --cpus-per-task=24                    # CPU cores per task
#SBATCH --time=24:00:00                       # Max time limit
#SBATCH --output=JJ_cellbender_output.log     # Output log file


# Load Singularity module
module load singularity

# Define variables
SINGULARITY_IMAGE=/home/johnathanj/containers/singularity/cellbender_latest.sif
CELLBENDER_SCRIPT=/home/johnathanj/projects/sivan_nasa/bin/ambient_correction/run_cellbender.py
INPUT_DIR=/home/johnathanj/projects/sivan_nasa/results/align_count
SAMPLE_LIST=/home/johnathanj/projects/sivan_nasa/bin/ambient_correction/sample_list.txt # can separate by chunk if needed for speed
OUTPUT_DIR=/home/johnathanj/projects/sivan_nasa/results/cellbender

# Print system information
echo "Node: $(hostname)"
echo "Memory info:"
free -h
echo "Disk space:"
df -h

# Run the Singularity container with the STARsolo script and monitor resources
/usr/bin/time -v singularity exec --nv ${SINGULARITY_IMAGE} python ${CELLBENDER_SCRIPT} ${INPUT_DIR} --samples_file ${SAMPLE_LIST} ${OUTPUT_DIR}

# Check exit status
if [ $? -ne 0 ]; then
    echo "Job failed. Check JJ_cellbender.log for details."
    exit 1
fi
