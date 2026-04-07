**Running AlphaFold3 for Protein–Protein Interaction Modeling**

This repository provides a step-by-step guide for running AlphaFold3 to model protein–protein interactions using HPC resources.

**1. AlphaFold 3 Repository**

The original AlphaFold 3 implementation can be found here:
https://github.com/google-deepmind/alphafold3

This repository contains all the necessary code required for AlphaFold 3 inference.

Accessing Model Parameters

To use AlphaFold 3, you must request access to the official model parameters.
Follow the instructions in the section below:

https://github.com/google-deepmind/alphafold3?tab=readme-ov-file#obtaining-model-parameters

Access is granted at the sole discretion of Google DeepMind. Requests are typically reviewed within 2–3 business days.

Note: AlphaFold 3 model parameters may only be used if obtained directly from Google DeepMind and are subject to their terms of use.


**2. MPCDF Account Setup (if applicable)**

This step is only relevant for employees of the Max Planck Society (MPG).

If you already have an MPCDF account, you may skip this section.
If you are not a member of the MPG, you can also skip steps 2 and 3 and instead use any other HPC system you have access to.

If you do not already have an MPCDF account, please follow the instructions here:
https://docs.mpcdf.mpg.de/faq/account.html


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
The current input format supports a maximum of two distinct proteins per job, with the option to specify any number of copies for each protein. 
Scalable modeling of complexes with more than two unique protein types is not currently supported in this repo.



3. In case you have an MPCDF account 
AlphaFold3 is now available on Raven,
please follow the instrucution here to load alphafold modeule and to add the weight file to your  
https://docs.mpcdf.mpg.de/bnb/217.html

note some bash terminal command would be required in case you don't knoe please this this cheetcheet https://cheatography.com/davechild/cheat-sheets/linux-command-line/





This repo contains some scripts for the scalable usage of alphafold3 for protein protein interaction. 

# AF3_Submitter

This Python script automates the creation of AlphaFold3-compatible JSON configuration files for protein complex modeling.
It reads a list of protein pairs from a CSV file, retrieves their FASTA sequences from UniProt, saves them locally, and generates a JSON input file for each modeling job.

> ⚠️ **Warning:**  
> This script submits **only protein complexes** to AlphaFold3 (AF3).  
> It is **not** designed for modeling other molecule types.

# Overview

The script performs the following steps:
- Reads a CSV file containing the protein pairs to be modeled.
- Fetches FASTA sequences from UniProt for each UniProt ID.
- Saves FASTA files in corresponding job directories.
- FASTA sequences retrieved from UniProt are automatically saved to a CSV cache file to facilitate repeated use.
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
```csv
job_name,uid1,uid2,uid1_copies,uid2_copies
Job1,P69905,P68871,2,2
Job2,Q9Y6K9,O00327,1,1
```

**2. Script Parameters**
User must specify in the script:
- csv_file_path = "<path #to the list of proteins>.csv"
- cache_file_path = "<path #to the CSV file listing previously downloaded UniProt FASTA sequences>"
- working_dir = "<path #to where the files will be generated>"
- model_seeds = [3141592]  # You can define one or multiple random seeds

# Usage
Run the script from the command line or within a Python environment:
> python af3_submitter.py


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
