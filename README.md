# Installation

## Prerequisites
- Python 3.x
- pip (Python package installer)

## Install the Package

1. Clone the Repository:
    ```sh
    git clone https://github.com/FordHBennett/Daikin_Internship_Summer_2024.git
    cd Daikin_Internship_Summer_2024
    ```
2. Install the Package:
    MacOS/Linux:
    ```sh
    python3 -m venv .venv/
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install .
    run-tag-generation
    ```

    Windows(PowerShell):
    ```pwsh
    python.exe -m venv .venv\
    .venv\Scripts\activate
    python.exe -m pip install --upgrade pip
    python.exe -m pip install .
    run-tag-generation.exe
    ```

## Development
1. Clone the Repository:
    ```sh
    git clone https://github.com/FordHBennett/Daikin_Internship_Summer_2024.git
    cd Daikin_Internship_Summer_2024
    ```

2. Install the Package in Editable Mode:
    MacOS/Linux:
    ```sh
    python3 -m venv .venv/
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e .
    python -c "import run-tag-generation"
    run-tag-generation
    ```

    Windows(PowerShell):
    ```pwsh
    python.exe -m venv .venv\
    .venv\Scripts\activate
    python.exe -m pip install --upgrade pip
    python.exe -m pip install -e .
    python.exe -c "import run-tag-generation"
    run-tag-generation.exe
    ```

## Uninstall the Package
1. Uninstall the Package:
    MacOS/Linux:
    ```sh
    python -m pip uninstall run-tag-generation
    deactivate 
    ```

    Windows(PowerShell):
    ```pwsh
    python.exe -m pip uninstall run-tag-generation
    deactivate
    ```



