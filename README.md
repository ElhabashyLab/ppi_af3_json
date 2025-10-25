# AF3_Submitter

This Python script automates the creation of AlphaFold3-compatible JSON configuration files for protein complex modeling.
It reads a list of protein pairs from a CSV file, retrieves their FASTA sequences from UniProt, saves them locally, and generates a JSON input file for each modeling job.

# Overview

The script performs the following steps:
- Reads a CSV file containing the protein pairs to be modeled.
- Fetches FASTA sequences from UniProt for each UniProt ID.
- Saves FASTA files in corresponding job directories.
- Generates AlphaFold3 JSON input files that define the modeling parameters and protein sequences.
Each modeling job is created as a separate directory within the specified working directory, containing:
Two FASTA files (uid1.fasta, uid2.fasta) and a JSON file (job_name.json) formatted for AlphaFold3

# Dependencies

Install the required packages using pip:
> pip install pandas requests


# Input
**1. CSV File**
The input CSV must contain the following columns:
- **Column**, **Name**,	**Description**
- **job_name**	Unique name for the modeling job (used to create directory and output files).
- **uid1**	UniProt ID of the first protein.
- **uid2**	UniProt ID of the second protein.
- **uid1_copies**	Number of copies of the first protein to include in the model.
- **uid2_copies**	Number of copies of the second protein to include in the model.

Example:
> job_name,uid1,uid2,uid1_copies,uid2_copies
> Job1,P69905,P68871,2,2
> Job2,Q9Y6K9,O00327,1,1


**2. Script Parameters**
User must specify inthe script:
- csv_file_path = "<path to the list of proteins>.csv"
- working_dir = "<path to where the files will be generated>"
- model_seeds = [3141592]  # You can define one or multiple random seeds

# Usage
Run the script from the command line or within a Python environment:
> python af3_submitter.py


# Output Structure
The script will generate one directory per job in the specified working directory.
Each job directory will contain:
<JobName>/
│
├── <uid1>.fasta
├── <uid2>.fasta
└── <JobName>.json


# example data

# License
This project is released under the MIT License.
Feel free to use and modify it with attribution.

- 
