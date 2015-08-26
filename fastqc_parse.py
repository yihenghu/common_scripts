#!/usr/bin/env python3
# by James Ashmore 
# https://www.biostars.org/u/13632/
# Biostar post: https://www.biostars.org/p/152138/#152151
# 08/26/2015

# Import necessary libraries:
import csv
import os
import subprocess
import zipfile

# List modules used by FastQC:
modules = ['Basic_Statistics',
           'Per_base_sequence_quality',
           'Per_tile_sequence_quality',
           'Per_sequence_quality_scores',
           'Per_base_sequence_content',
           'Per_sequence_GC_content',
           'Per_base_N_content',
           'Sequence_Length_Distribution',
           'Sequence_Duplication_Levels',
           'Overrepresented_sequences',
           'Adapter_Content',
           'Kmer_Content']

# Set dict to convert module results to integer scores:
scores = {'pass': 1,
          'warn': 0,
          'fail': -1}

# Get current working directory:
cwd = os.getcwd()

# Get list of '_fastqc.zip' files generated by FastQC:
files = [file for file in os.listdir(cwd) if file.endswith('_fastqc.zip')]

# List to collect module scores for each '_fastqc.zip' file:
all_mod_scores = []

# Read fastqc_data.txt file in each archive:
for file in files:
    archive = zipfile.ZipFile(file, 'r') # open '_fastqc.zip' file
    members = archive.namelist() # return list of archive members
    fname = [member for member in members if 'fastqc_data.txt' in member][0] # find 'fastqc_data.txt' in members
    data = archive.open(fname) # open 'fastqc_data.txt'
  
    # Get module scores for this file:
    mod_scores = [file]
    for line in data:
        text = line.decode('utf-8') 
        if '>>' in text and '>>END' not in text:
            text = text.lstrip('>>').split()
            module = '_'.join(text[:-1])
            result = text[-1]
            mod_scores.append(scores[result])
    
    # Append to all module scores list:
    all_mod_scores.append(mod_scores)
    
    # close all opened files:
    data.close()
    archive.close()

# Write scores out to a CSV file:
with open('all_mod_scores.csv', 'w') as f:
    writer = csv.writer(f)
    for mod_scores in all_mod_scores:
        writer.writerow(mod_scores)
    f.close()

