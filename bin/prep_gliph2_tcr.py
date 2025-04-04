#!/usr/bin/env python3

"""
prep_gliph2_tcr.py
Input: adaptive TSV files
Output: ${project_name}_tcr.txt
"""

# Import modules
import argparse
import glob
import os
import pandas as pd

# Initialize the parser
parser = argparse.ArgumentParser(description="Take positional args")

# Add positional arguments
parser.add_argument("data_dir")
parser.add_argument("project_name")
parser.add_argument("samplesheet")

# Parse the arguments
args = parser.parse_args()

# Print the arguments
print("data_dir: ", args.data_dir)
print("project_name: ", args.project_name)
print("samplesheet: ", args.samplesheet)

samplesheet = pd.read_csv(args.samplesheet, header=0)
data_dir = args.data_dir + "/"
tsv_files = glob.glob(os.path.join(data_dir, "*.tsv"))
tsv_files = [os.path.abspath(file) for file in tsv_files]

dfs = []
for index, row in samplesheet.iterrows():
    file_path = row['file']
    print(f"Loading {file_path}")
    
    # Read the TSV file into a dataframe
    df = pd.read_csv(file_path, sep="\t", header=0)
    
    # Get metadata
    subject_id = row['subject_id']
    timepoint = row['timepoint']
    origin = row['origin']
    
    # Add patient column
    df['patient'] = f"{subject_id}:{timepoint}_{origin}"
    
    # Select relevant columns
    df = df[['aminoAcid', 'vGeneName', 'jGeneName', 'patient', 'count (templates/reads)']]
    dfs.append(df)


# Concatenate all the dataframes into one
df_combined = pd.concat(dfs)

# Rename columns as required
df_combined = df_combined.rename(columns={
    'aminoAcid': 'CDR3b',
    'vGeneName': 'TRBV',
    'jGeneName': 'TRBJ',
    'count (templates/reads)': 'counts'
})
df_combined = df_combined[df_combined['CDR3b'].notna()]

df_combined.to_csv(f"{args.project_name}_tcr.txt", sep="\t", index=False, header=True)
