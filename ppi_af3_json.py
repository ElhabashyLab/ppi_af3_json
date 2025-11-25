import os
import json
import pandas as pd
import requests



# Example usage
csv_file_path = " <path to the list of the proteins to be modelled>.csv" 
cache_file_path = " <path to the list of the proteins allready pulled>.csv" 
working_dir = "<path to where the files will be generated>" 
model_seeds = [3141592]  # Set your desired seeds



# Function to fetch FASTA sequence for a given UniProt ID
def fetch_fasta(uniprot_id, session = None, cache = {}):
    
    if uniprot_id in cache:
        return cache[uniprot_id], cache
    
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    response = session.get(url)
    
    if response.status_code == 200:
        cache[uniprot_id] = ''.join(response.text.split('\n')[1:])   # Return sequence only, removing FASTA header
        return cache[uniprot_id], cache
    else:
        print(f"Failed to fetch FASTA for UniProt ID {uniprot_id}")
        return None, cache

# Function to save FASTA file to the specified directory
def save_fasta(fasta_content, output_dir, uniprot_id):
    filename = f"{uniprot_id}.fasta"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as fasta_file:
        fasta_file.write(fasta_content)
    
    print(f"Saved FASTA for {uniprot_id} at {filepath}")

# Function to process CSV and generate JSON files in each job directory
def process_csv_and_generate_json(csv_file_path, working_dir, model_seeds, cache={}):
    df = pd.read_csv(csv_file_path)
    session = requests.Session() 
    
    for index, row in df.iterrows():
        job_name = row['job_name']
        uid1 = row['uid1']
        uid2 = row['uid2']
        uid1_copies = row['uid1_copies']
        uid2_copies = row['uid2_copies']
        
        job_dir = os.path.join(working_dir, job_name)
        os.makedirs(job_dir, exist_ok=True)
        print(f"Created directory: {job_dir}")
        
        sequences_list = []
        letter_counter = 0  # Start from 'A'
        
        # uid1 sequences
        fasta1, cache = fetch_fasta(uid1, session=session, cache=cache)
        if fasta1:
            save_fasta(fasta1, job_dir, uid1)
            for _ in range(uid1_copies):
                sequences_list.append({
                    "protein": {
                        "id": [chr(65 + letter_counter)],
                        "sequence": fasta1
                    }
                })
                letter_counter += 1
        
        # uid2 sequences
        fasta2, cache = fetch_fasta(uid2, session=session, cache=cache)
        if fasta2:
            save_fasta(fasta2, job_dir, uid2)
            for _ in range(uid2_copies):
                sequences_list.append({
                    "protein": {
                        "id": [chr(65 + letter_counter)],
                        "sequence": fasta2
                    }
                })
                letter_counter += 1


        json_data = {
            "name": job_name,
            "modelSeeds": model_seeds,
            "sequences": sequences_list,
            "dialect": "alphafold3",
            "version": 1
        }
        json_output_path = os.path.join(job_dir, f"{job_name}.json")
        
        with open(json_output_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        
        print(f"JSON file saved at {json_output_path}")
    
    # Return the cache for further use
    return cache


if os.path.exists(cache_file_path):
    cache_df = pd.read_csv(cache_file_path)
    fasta_cache = dict(zip(cache_df['uid'], cache_df['fasta']))
    print(f"Loaded FASTA cache from {cache_file_path}")
else:
    fasta_cache = {}

cache = process_csv_and_generate_json(csv_file_path, working_dir, model_seeds, cache=fasta_cache)

pd.DataFrame(list(cache.items()), columns=['uid', 'fasta']).to_csv(cache_file_path, index=False)
print(f"FASTA cache saved at {cache_file_path}")
