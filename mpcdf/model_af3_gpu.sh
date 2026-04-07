#!/bin/bash 

#this is how to run in the background 
#nohup bash model_af3.sh  > model_af3.log 2>&1 &


file1="msa.test"
file2="af3.list"

ls -d $PWD/*_*/*data* > "$file1"
sed -i 's|/[^/]*$||' "$file1"

ls -d $PWD/*_*/*confidence* > "$file2"
sed -i 's|/[^/]*$||' "$file2"

# Step 2: Remove duplicates from file1 that exist in file2
grep -vxFf "$file2" "$file1" > tmp_file && mv tmp_file "$file2"


#this is how to run in the backgroung 
#nohup bash model_af3.sh  > model_af3.log 2>&1 &


#####WARNING####

#DO NOT FORGET TO TERMINATE THE SCRIPT 
#AFTER ALL YOUR CALCULATIONS ARE DONE

#AND THIS IS HOW
#ps -ef | grep model_af3.sh
#FIND THE JOB ID 
#example
#hadel    118091  49302  0 12:43 pts/534  00:00:00 grep --color=auto model_af3.sh

#AND RUN 
# KILL <JOB ID>
################
# Max number of jobs allowed
MAX_JOBS=300

# Sleep interval (30 minutes)
SLEEP_INTERVAL=$((10*60))

# User running the jobs
USER_NAME="hadel"

# File containing subdirectory list
LIST_FILE="af3.list"

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
                sbatch jobscript-alphafold3-step_2-prediction.sh
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
