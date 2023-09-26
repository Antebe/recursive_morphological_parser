import os
import json

def read_morphemes(folder_path):
    # Create an empty list to store loaded JSON data
    loaded_json_data = {}

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Create a full path to the JSON file
            json_file_path = os.path.join(folder_path, filename)

            # Load the JSON data from the JSON file
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)

            loaded_json_data[filename.split(".")[0]] = (json_data)      
    return loaded_json_data

# Now, 'loaded_json_data' contains the loaded JSON objects from all JSON files in the folder
# You can access each JSON object by iterating through the list