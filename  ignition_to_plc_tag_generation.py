import pandas as pd
import json
from typing import Dict, Any

from zmq import NULL

'''
TODO:
Create a generic opcItemPath generation function that generates the path for the ignition tag based off of the kepware parameters
Communitcate with the drivers to so I can send to and from ignition
'''

'''
Considerations:
-If the template has nested key I will need to check if the each tag in the ignition json is nested or not
-If it is not nested then when I use the template I need to make sure that the keys in the ignition json are not nested
'''

def Get_All_Keys(json_structure: Any) -> Dict[str, Any]:
    def recursive_extract_keys(obj: Any, parent_key: str = '') -> Dict[str, Any]:
        keys = {}
        # Dumbass python3.9 doesn't have switch statements
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                keys[key] = recursive_extract_keys(value, full_key)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                keys.update(recursive_extract_keys(item, full_key))
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
