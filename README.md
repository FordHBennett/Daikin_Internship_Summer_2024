# Installation

## Prerequisites
- Python 3.x
- pip (Python package installer)

## Install the Package
1. Clone the Repository:
    ```
    git clone https://github.com/FordHBennett/Daikin_Internship_Summer_2024.git
    cd Daikin_Internship_Summer_2024
    ```

MacOS/Linux:
python3 -m venv .venv/ 
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install . 
run-tag-generation

Windows(PowerShell):
python.exe -m venv .venv\
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
python.exe -m pip install .
run-tag-generation.exe

## Development
1. Clone the Repository:
    ```
    git clone
    cd Daikin_Internship_Summer_2024
    ```
MacOS/Linux:
python3 -m venv .venv/
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . 
python -c "import run-tag-generation"
run-tag-generation

Windows(PowerShell):
python.exe -m venv .venv\
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
python.exe -m pip install -e .
python.exe -c "import run-tag-generation"
run-tag-generation.exe

## Uninstall the Package
Windows(PowerShell):
python.exe -m pip uninstall run-tag-generation

MacOS/Linux:
python -m pip uninstall run-tag-generation
```

