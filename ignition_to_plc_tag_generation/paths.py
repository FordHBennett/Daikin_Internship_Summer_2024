import os
from typing import List

def Get_ALL_JSON_Paths(dir: str) -> List[str]:
    json_paths: List[str] = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), dir)):
        for file in files:
            if file.endswith('.json'):
                json_paths.append(os.path.join(root, file))
    return json_paths

def Get_ALL_CSV_Paths(dir: str) -> List[str]:
    csv_paths: List[str] = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), dir)):
        for file in files:
            if file.endswith('.csv'):
                csv_paths.append(os.path.join(root, file))
    return csv_paths
