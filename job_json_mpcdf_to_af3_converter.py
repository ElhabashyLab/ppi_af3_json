import json
import os

def convert_MPCDF_json_to_alphafold_json(input_file: str, output_file: str) -> None:
    """
    Convert an MPCDF AlphaFold 3 job JSON file to AlphaFold server JSON format.

    This function transforms MPCDF-specific job definitions into the format expected
    by the AlphaFold server. The key transformation is converting 'protein' entries
    to 'proteinChain' entries while preserving all optional fields.

    The function handles both single job dictionaries and lists of job dictionaries,
    normalizing them into a consistent list format for processing.

    Parameters
    ----------
    input_file : str
        Path to the input MPCDF AlphaFold 3 job JSON file. Can contain either a
        single job dictionary or a list of job dictionaries.
    output_file : str
        Path where the converted AlphaFold-server-compatible JSON file will be
        written. Parent directories are created automatically if they don't exist.

    Returns
    -------
    None
        The function writes output to disk and prints a confirmation message.

    Notes
    -----
    Conversion details:
    - 'protein' entries are converted to 'proteinChain' with a default count of 1
    - Optional fields preserved: glycans, modifications, maxTemplateDate, useStructureTemplate
    - Non-protein sequence types (e.g., RNA, DNA, ligands) are passed through unchanged
    - Default modelSeeds value is [3141592] if not specified in input json file
    - Output format includes dialect="alphafold3" and version=1

    Examples
    --------
    >>> convert_MPCDF_json_to_alphafold_json(
    ...     "mpcdf_jobs/job1.json",
    ...     "af3_jobs/job1.json"
    ... )
    AF3-ready JSON saved to af3_jobs/job1.json
    """
    with open(input_file, "r") as f:
        data = json.load(f)

    # If the input is a single job dict, wrap it in a list
    if isinstance(data, dict):
        data = [data]

    af3_jobs = []

    for job in data:
        new_sequences = []
        for seq_entry in job.get("sequences", []):
            # Convert protein entries
            if "protein" in seq_entry:
                protein = seq_entry["protein"]
                protein_chain = {"sequence": protein["sequence"], "count": 1}

                # Preserve optional fields if present
                for optional_field in ["glycans", "modifications", "maxTemplateDate", "useStructureTemplate"]:
                    if optional_field in protein:
                        protein_chain[optional_field] = protein[optional_field]

                new_sequences.append({"proteinChain": protein_chain})
            else:
                # Keep other sequence types as-is
                new_sequences.append(seq_entry)

        af3_job = {
            "name": job.get("name", "job"),
            "modelSeeds": job.get("modelSeeds", [3141592]),
            "sequences": new_sequences,
            "dialect": "alphafold3",
            "version": 1
        }

        af3_jobs.append(af3_job)

    # Write AF3-ready JSON
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    with open(output_file, "w") as f:
        json.dump(af3_jobs, f, indent=2)

    print(f"AF3-ready JSON saved to {output_file}")


def convert_json_folder(input_folder: str, output_folder: str) -> None:
    """
    Batch convert all MPCDF AlphaFold 3 job files in a directory to AlphaFold server format.

    This function processes all JSON and TXT files in the input directory, converting
    each one using the MPCDF-to-AlphaFold transformation. Files with other extensions
    are skipped. The output directory is created automatically if it doesn't exist.

    Parameters
    ----------
    input_folder : str
        Path to the directory containing MPCDF AlphaFold 3 job files. Only files
        with .json or .txt extensions will be processed.
    output_folder : str
        Path to the directory where converted AlphaFold-compatible JSON files will
        be saved. This directory will be created if it doesn't exist.

    Returns
    -------
    None
        The function writes converted files to disk and prints confirmation messages
        for each file processed. These can then be added to the AlphaFold Web Server via the 
        "Upload JSON" option.

    Notes
    -----
    - All output files have a .json extension regardless of input extension
    - Original filenames are preserved (only extension may change)
    - Empty directories or directories with no .json/.txt files will complete silently

    Examples
    --------
    >>> convert_json_folder("mpcdf_jobs/", "af3_jobs/")
    AF3-ready JSON saved to af3_jobs/job1.json
    AF3-ready JSON saved to af3_jobs/job2.json
    AF3-ready JSON saved to af3_jobs/experiment_a.json

    See Also
    --------
    convert_MPCDF_json_to_alphafold_json : Converts a single file
    """
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".txt") and not file_name.endswith(".json"):
            continue
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".json")
        convert_MPCDF_json_to_alphafold_json(input_path, output_path)


# Usage:
input_folder = "Path_to_MPCDF_jobs_to_convert"
output_folder = "Path_to_save_converted_AF3_jobs"
convert_json_folder(input_folder, output_folder)
