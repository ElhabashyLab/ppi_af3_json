**Running AlphaFold3 for Protein–Protein Interaction Modeling**
This repository provides a step-by-step guide for running AlphaFold3 to model protein–protein interactions using HPC resources.


  
**1. AlphaFold 3 Repository**

The original AlphaFold 3 implementation can be found here:
(https://github.com/google-deepmind/alphafold3)
This repository contains all the necessary code required for AlphaFold 3 inference.
Accessing Model Parameters
  
To use AlphaFold 3, you must request access to the official model parameters.
Follow the instructions in the section below:
(https://github.com/google-deepmind/alphafold3?tab=readme-ov-file#obtaining-model-parameters)
Access is granted at the sole discretion of Google DeepMind. Requests are typically reviewed within 2–3 business days.
**Note**: AlphaFold 3 model parameters may only be used if obtained directly from Google DeepMind and are subject to their terms of use.
   
   
**2. MPCDF Account Setup (if applicable)**

This step is only relevant for employees of the Max Planck Society (MPG).
If you already have an MPCDF account, you may skip this section.
If you are not a member of the MPG, you can also skip steps 2 and 3 and instead use any other HPC system you have access to.
If you do not already have an MPCDF account, please follow the instructions here:
(https://docs.mpcdf.mpg.de/faq/account.html)
   
   
**3. Running AlphaFold 3 on MPCDF (Raven Cluster)**

AlphaFold 3 is available on the Raven cluster at MPCDF.
To load the AlphaFold module and configure the required environment (including model weights), follow the official documentation:
https://docs.mpcdf.mpg.de/bnb/217.html
   
   
**4. Prepare Input List of Protein–Protein Interactions**

Before running AlphaFold 3, you need to prepare an input file specifying the protein–protein interactions to be modeled.

a. The input file in CSV formate CSV must contain the following columns:
- **Column**, **Name**,	**Description**
- **job_name**	Unique name for the modeling job (used to create output directory and files).
- **uid1**	UniProt ID of the first protein.
- **uid2**	UniProt ID of the second protein.
- **uid1_copies**	Number of copies of the first protein to include to be modeled.
- **uid2_copies**	Number of copies of the second protein to include to be modeled.

Example:
```csv
job_name,uid1,uid2,uid1_copies,uid2_copies
Job1,P69905,P68871,2,2
Job2,Q9Y6K9,O00327,1,1
```

> ⚠️ **Warning:**  
> The current input format supports a maximum of two distinct proteins per job, with the option to specify any number of copies for each protein. 
> Scalable modeling of complexes with more than two unique protein types is not currently supported in this repo.


**5. Create AlphaFold3 JSON Input File**

This repository includes two helper scripts for generating AlphaFold 3-compatible input files:

> AF3_json_1seed.py
> AF3_json_20seeds.py

These scripts automate the preparation of input data for protein–protein complex modeling.
The scripts take a CSV file containing protein pairs as input, retrieve corresponding FASTA sequences from UniProt, and generate properly formatted AlphaFold 3 JSON configuration files for each modeling job.
Each job is created in its own directory within the specified working directory.

The two scripts differ only in the number of diffusion seeds used:

> AF3_json_1seed.py uses 1 seed abd produces 5 models per job
> AF3_json_20seeds.py uses 20 seeds and produces 100 models per job

Both scripts perform the following steps:

- Read the input .csv file containing protein pairs to be modeled
- Fetch FASTA sequences from UniProt using the provided UniProt IDs
- Save FASTA files locally in each job directory
- Cache retrieved sequences in a CSV file to avoid redundant downloads
- Generate AlphaFold 3 JSON input files defining model parameters and sequences


Here the repo contains two scripts that can help you
AF3_json_1seed.py and AF3_json_20seeds.py 
  
This Python script automates the creation of AlphaFold3-compatible JSON configuration files for protein complex modeling.
It reads a list of protein pairs from a CSV file, retrieves their FASTA sequences from UniProt, saves them locally, and generates a JSON input file for each modeling job.

the only difference betwweb the two files is the number of seeds
the first add one seed which results in 5 models and the second sample using 20 seeds which results in a 100 models

both take the described input file. 
 The script performs the following steps:
- Reads a CSV file containing the protein pairs to be modeled.
- Fetches FASTA sequences from UniProt for each UniProt ID.
- Saves FASTA files in corresponding job directories.
- FASTA sequences retrieved from UniProt are automatically saved to a CSV cache file to facilitate repeated use.
- Generates AlphaFold3 JSON input files that define the modeling parameters and protein sequences.
Each modeling job is created as a separate directory within the specified working directory, containing:
Two FASTA files (uid1.fasta, uid2.fasta) and a JSON file (job_name.json) formatted for AlphaFold3

> ⚠️ **Warning:**  
> This script submits **only protein complexes** to AlphaFold3 (AF3).  
> It is **not** designed for modeling other molecule types.

# Dependencies

Install the required packages using pip:
> pip install pandas requests


**2. Script Parameters**
User must specify in the script:
- csv_file_path = "<path #to the list of proteins>.csv"
- cache_file_path = "<path #to the CSV file listing previously downloaded UniProt FASTA sequences>"
- working_dir = "<path #to where the files will be generated>"
- model_seeds = [3141592]  # You can define one or multiple random seeds

# Usage
Run the script from the command line or within a Python environment:
> python3 AF3_json_1seed.py
> python3 AF3_json_20seeds.py 


# Output Structure
The script will generate one directory per job in the specified working directory.
Each job directory will contain:
```
<JobName>/
│
├── <uid1>.fasta
├── <uid2>.fasta
└── <JobName>.json
```
(The cache CSV file will be updated in place)


# Example data
The example CSV file **example_dataset.csv** is provided in the repository to illustrate the expected data format and facilitate testing of the script.

# License
This script is released under the MIT License.
