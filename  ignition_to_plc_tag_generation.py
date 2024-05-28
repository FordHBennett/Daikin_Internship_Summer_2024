import pandas as pd
import json
from typing import Dict, Any, List
import os

'''
TODO:
    -Create a generic opcItemPath generation function that generates the path for the ignition tag based off of the kepware parameters
    -Communitcate with the drivers to so I can send to and from ignition
'''

'''
CONSIDERATIONS:
    -If the template has nested key I will need to check if the each tag in the ignition json is nested or not
    -If it is not nested then when I use the template I need to make sure that the keys in the ignition json are not nested
    POSSIBLE SOLUTION:
        -I check each ignition key to see if it is nested or not recursively
            -If it is nested then pass
            -If it is not then set the key to null
'''

'''
MITSUBISHI DRIVER DOCUMENTATION:
    -https://forum.inductiveautomation.com/t/mitsubishi-driver/73741
    -https://www.docs.inductiveautomation.com/docs/8.1/ignition-modules/opc-ua/opc-ua-drivers/mitsubishi-tcp-driver
'''

'''
DON'T MAKE SENSE: Why do the documentation use csv files for importing/exporting tags but they keep on telling me it using json files
'''

def Get_All_Keys(json_structure: Any) -> Dict[str, Any]:
    """
    The function `get_all_keys` recursively extracts all keys from a JSON-like structure and returns
    them in a dictionary.

    @param json_structure The `json_structure` parameter in the `get_all_keys` function is expected to
    be a JSON-like data structure of type `Any`, which can be a dictionary, list, or a combination of
    both. The function recursively extracts all keys present in the JSON structure along with their
    hierarchical paths.

    @return The function `get_all_keys` returns a dictionary containing all the keys found in the JSON
    structure provided as input.
    """
    def Recursive_Extract_Keys(obj: Any, parent_key: str = '', keys_set: set = None) -> Dict[str, Any]:
        if keys_set is None:
            keys_set = set()

        keys = {}
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    keys[key] = Recursive_Extract_Keys(value, full_key, keys_set)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    keys.update(Recursive_Extract_Keys(item, full_key, keys_set))
        else:
            return None
        return keys

    return Recursive_Extract_Keys(json_structure)


def Get_ALL_MA_JSON_Paths() -> List[str]:
    """
    The function `Get_ALL_MA_JSON_Paths` retrieves a list of file paths for JSON files containing "MA"
    in their names within the current working directory.

    @return A list of file paths for all JSON files with 'MA' in their name within the current working
    directory and its subdirectories.
    """
    ma_json_paths = []
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if 'MA' in file and file.endswith('.json'):
                ma_json_paths.append(os.path.join(root, file))
    return ma_json_paths


if __name__ == '__main__':
    # File paths
    csv_file: str = 'MA_EV1.csv'
    json_files: List[str] = Get_ALL_MA_JSON_Paths()
    # Read the CSV file into a DataFrame
    df: pd.DataFrame = pd.read_csv(csv_file)

    # Dictionary to hold all keys from all JSON files
    all_keys: Dict[str, Any] = {}

    # Read each JSON file and extract keys
    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_structure = json.load(f)
            keys = Get_All_Keys(json_structure)
            all_keys.update(keys)

    # Dump the keys dictionary to a file
    key_json: str = json.dumps(all_keys, indent=4)
    with open('keys.json', 'w') as f:
        f.write(key_json)
