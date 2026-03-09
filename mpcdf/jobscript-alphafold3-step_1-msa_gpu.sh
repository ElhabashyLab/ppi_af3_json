#!/bin/bash -l
#SBATCH --job-name=AF3_MSA_GPU
#SBATCH --ntasks=1
#SBATCH --constraint=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=18
#SBATCH --mem=60000
#SBATCH --time=03:00:00

module purge
module load apptainer/1.3.2
module load alphafold/3.0.0

source parameters.inc
mkdir -p $AF3_MSA_OUTPUT_DIR

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

export TMPDIR=/ptmp/$USER/tmp/${SLURM_JOBID}
mkdir -p $TMPDIR

srun apptainer --quiet exec --bind /u:/u,/ptmp:/ptmp,/raven:/raven \
    ${AF3_IMAGE_SIF} \
    python3 /app/alphafold/run_alphafold.py \
    --db_dir $AF3_DB_DIR \
    --model_dir $AF3_MODEL_DIR \
    --json_path $AF3_MSA_JSON_PATH \
    --output_dir $AF3_MSA_OUTPUT_DIR \
    --norun_inference
