#!/bin/bash -l
#SBATCH --job-name=AF3_modeling
#SBATCH --ntasks=1
#SBATCH --constraint=gpu
#SBATCH --time=10:00:00

# 1/4 node, for small setups (comment '##' and move to more resources if necessary, see below)
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=18
#SBATCH --mem=125000

# 1/2 node, for medium setups:
##SBATCH --gres=gpu:a100:2
##SBATCH --cpus-per-task=36
##SBATCH --mem=250000

# 1 node, for larger setups:
####SBATCH --gres=gpu:a100:4
####SBATCH --cpus-per-task=72
####SBATCH --mem=500000

module purge
module load apptainer/1.3.2
module load alphafold/3.0.0

source parameters.inc
mkdir -p $AF3_JAX_CACHE_DIR $AF3_INFERENCE_OUTPUT_DIR

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export TMPDIR=${JOB_TMPDIR}
export XLA_FLAGS="--xla_gpu_enable_triton_gemm=false"
export XLA_PYTHON_CLIENT_PREALLOCATE=false
export TF_FORCE_UNIFIED_MEMORY=true
export XLA_CLIENT_MEM_FRACTION="3.0"
# 1/2 node
##export XLA_CLIENT_MEM_FRACTION="6.0"
# 1 node
####export XLA_CLIENT_MEM_FRACTION="12.0"

srun apptainer --quiet exec --bind /u:/u,/ptmp:/ptmp,/raven:/raven --nv \
    ${AF3_IMAGE_SIF} \
    python3 /app/alphafold/run_alphafold.py \
    --db_dir $AF3_DB_DIR \
    --model_dir $AF3_MODEL_DIR \
    --json_path $AF3_INFERENCE_JSON_PATH \
    --output_dir $AF3_INFERENCE_OUTPUT_DIR \
    --jax_compilation_cache_dir $AF3_JAX_CACHE_DIR \
    --norun_data_pipeline \
