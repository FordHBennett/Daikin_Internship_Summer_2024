import pandas as pd
import json
from typing import Dict, Any

from zmq import NULL


def Get_All_Keys(json_structure: Any) -> Dict[str, Any]:
    """
    This function takes a JSON structure as input and returns a dictionary containing all the keys
    present in the structure.

    @param json_structure JSON structure from which keys need to be extracted.
    """
    def recursive_extract_keys(obj: Any, parent_key: str = '') -> Dict[str, Any]:
        """
        The `recursive_extract_keys` function recursively extracts keys from a nested dictionary or list
        structure along with their full paths.

        @param obj The `obj` parameter in the `recursive_extract_keys` function is the input object for
        which you want to extract keys. It can be a dictionary, list, or any other object that contains keys
        or nested keys.
        @param parent_key The `parent_key` parameter in the `recursive_extract_keys` function is used to
        keep track of the current key in the recursive traversal of the input object. It represents the key
        of the parent object in the hierarchy of keys. It helps in constructing the full path of keys as the
        function traverses

        @return The `recursive_extract_keys` function returns a dictionary where the keys are the nested
        keys of the input object `obj` along with their full paths, and the values are the corresponding
        values or nested keys.
        """
        keys = {}
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                keys[key] = recursive_extract_keys(value, full_key)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                keys.update(recursive_extract_keys(item, full_key))
        else:
            keys = None
        return keys

    return recursive_extract_keys(json_structure)

#If the template has nested key I will need to check if the each tag in the ignition json is nested or not
#If it is not nested then when I use the template I need to make sure that the keys in the ignition json are not nested

def main() -> None:
    # File paths
    csv_file: str = 'MA_EV1.csv'
    json_file: str = 'MA_Ev1_Ignition.json'

    # Read the CSV file into a DataFrame
    df: pd.DataFrame = pd.read_csv(csv_file)

    # Read the existing JSON structure file
    with open(json_file, 'r') as f:
        json_structure = json.load(f)

    # Get all keys from the JSON structure
    keys = Get_All_Keys(json_structure)

    #dump the keys to a file
    key_json = json.dumps(keys, indent=4)
    with open('keys.json', 'w') as f:
        f.write(key_json)if __name__ == "__main__":
    main()
