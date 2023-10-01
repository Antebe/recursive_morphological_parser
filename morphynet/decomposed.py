import json
import os

# Initialize empty lists for prefixes and suffixes
prefixes = []
suffixes = []

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
eng = os.path.join(THIS_DIR, 'eng.derivational.v1.tsv')
# Read the TSV file and process each line
with open(eng, 'r', encoding="UTF8") as tsvfile:
    for line in tsvfile:
        # Split the line into columns using tabs
        columns = line.strip().split('\t')
        if len(columns) == 6:
            word = columns[0]
            type_morph = columns[5]
            morph = columns[4]
            
            # Add the prefix to the prefixes list if it's not empty
            if type_morph == "prefix":
                prefixes.append(morph)
            
            # Add the suffix to the suffixes list if it's not empty
            if type_morph == "suffix":
                suffixes.append(morph)

# Save the prefixes and suffixes lists to JSON files
with open('morphynet/prefixes.json', 'w') as prefixfile:
    json.dump(list(set(prefixes)), prefixfile, indent=2)

with open('morphynet/suffixes.json', 'w') as suffixfile:
    json.dump(list(set(suffixes)), suffixfile, indent=2)
