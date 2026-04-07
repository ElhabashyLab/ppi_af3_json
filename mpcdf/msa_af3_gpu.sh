#!/bin/bash

#one need to run this first
#ls -d $PWD/* > msa.list

#this is how to run in the backgroung 
#nohup bash msa_af3.sh  > msa_af3.log 2>&1 &

# Max number of jobs allowed
MAX_JOBS=300

# Sleep interval (15 minutes)
SLEEP_INTERVAL=$((10*60))

# User running the jobs
USER_NAME="hadel"

# File containing subdirectory list
LIST_FILE="msa.list"

# Loop over list
while IFS= read -r dir; do
    # Skip if not a directory (safety)
    [ -d "$dir" ] || continue

    while true; do
        # Count current jobs
        current_jobs=$(squeue -u "$USER_NAME" -p gpu1 | tail -n +2 | wc -l)

        if [ "$current_jobs" -lt "$MAX_JOBS" ]; then
            echo "[$(date)] Submitting job in $dir (current jobs: $current_jobs)"
            (
                cd "$dir" || exit
                #jobid=$(sbatch jobscript-alphafold3-step_1-msa_gpu.sh | awk '{print $4}')
                sbatch jobscript-alphafold3-step_1-msa_gpu.sh
            )
            # Pause a bit between submissions
            sleep 2
            break
        else
            echo "[$(date)] Job limit reached ($current_jobs). Waiting $SLEEP_INTERVAL seconds..."
            sleep "$SLEEP_INTERVAL"
        fi
    done
done < "$LIST_FILE"

echo "[$(date)] All jobs submitted."
