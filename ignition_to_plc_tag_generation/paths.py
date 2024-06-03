import os
from typing import List

def Get_ALL_JSON_Paths(dir: str) -> List[str]:
    """
    Get all JSON file paths within a directory and its subdirectories.

    Args:
        dir (str): The directory path to search for JSON files.

    Returns:
        List[str]: A list of JSON file paths found within the directory and its subdirectories.
    """
    json_paths: List[str] = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), dir)):
        for file in files:
            if file.endswith('.json'):
                json_paths.append(os.path.join(root, file))
    return json_paths

def Get_ALL_CSV_Paths(dir: str) -> List[str]:
    """
    Get all the paths of CSV files within a directory and its subdirectories.

    Args:
        dir (str): The directory path to search for CSV files.

    Returns:
        List[str]: A list of paths to CSV files found within the directory and its subdirectories.
    """
    csv_paths: List[str] = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), dir)):
        for file in files:
            if file.endswith('.csv'):
                csv_paths.append(os.path.join(root, file))
    return csv_paths
