import os
import json

# Folder containing the TXT files
folder_path = 'sample'

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Create a full path to the TXT file
        txt_file_path = os.path.join(folder_path, filename)

        # Read the TXT file
        with open(txt_file_path, 'r', encoding = "UTF8") as txt_file:
            lines = txt_file.readlines()

        # Create a dictionary to store the data
        data = []
        for line in lines:
            if line:
                data.append(line[:-1])

        # Convert the dictionary to JSON
        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        # Create a JSON filename by replacing the .txt extension with .json
        json_filename = filename.replace('.txt', '.json')

        # Create a full path to the JSON file
        json_file_path = os.path.join(folder_path, json_filename)

        # Save the JSON data to the JSON file
        with open(json_file_path, 'w', encoding="UTF8") as json_file:
            json_file.write(json_data)

print("Conversion completed for all TXT files in the folder.")