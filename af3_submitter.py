import os
import json
import pandas as pd
import requests



# Example usage
csv_file_path = " <path to the list of the proteins to be modelled>.csv"  
working_dir = "<path to where the files will be generated>" 
model_seeds = [3141592]  # Set your desired seeds



# Function to fetch FASTA sequence for a given UniProt ID
def fetch_fasta(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    response = requests.get(url)
    
    if response.status_code == 200:
        return ''.join(response.text.split('\n')[1:])  # Return sequence only, removing FASTA header
    else:
        print(f"Failed to fetch FASTA for UniProt ID {uniprot_id}")
        return None

# Function to save FASTA file to the specified directory
def save_fasta(fasta_content, output_dir, uniprot_id):
    filename = f"{uniprot_id}.fasta"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as fasta_file:
        fasta_file.write(fasta_content)
    
    print(f"Saved FASTA for {uniprot_id} at {filepath}")

# Function to process CSV and generate JSON files in each job directory
def process_csv_and_generate_json(csv_file_path, working_dir, model_seeds):
    df = pd.read_csv(csv_file_path)
    
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
        fasta1 = fetch_fasta(uid1)
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
        fasta2 = fetch_fasta(uid2)
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


process_csv_and_generate_json(csv_file_path, working_dir, model_seeds)
