import pandas as pd
import json
from typing import Dict, Any

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

def get_all_keys(json_structure: Any) -> Dict[str, Any]:
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
    def recursive_extract_keys(obj: Any, parent_key: str = '', keys_set: set = None) -> Dict[str, Any]:
        if keys_set is None:
            keys_set = set()

        keys = {}
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    keys[key] = recursive_extract_keys(value, full_key, keys_set)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    keys.update(recursive_extract_keys(item, full_key, keys_set))
        else:
            return None
        return keys

    return recursive_extract_keys(json_structure)


if __name__ == '__main__':
    # File paths
    csv_file: str = 'MA_EV1.csv'
    json_file: str = 'MA_Ev1_Ignition.json'

    # Read the CSV file into a DataFrame
    df: pd.DataFrame = pd.read_csv(csv_file)

    # Read the existing JSON structure file
    with open(json_file, 'r') as f:
        json_structure = json.load(f)

    # Get all keys from the JSON structure
    keys: Dict[str, Any] = Get_All_Keys(json_structure)

    #dump the keys to a file
    key_json: str = json.dumps(keys, indent=4)
    with open('keys.json', 'w') as f:
        f.write(key_json)
