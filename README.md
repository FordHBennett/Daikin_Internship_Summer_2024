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

2. Input folder structure:
    ```
    input/
        plc_brand/
            csv/
            json/
    ```

    Place your Ignition tags into the corresponding `json` folder.\
    Place your Kepware CSV file into the corresponding `csv` folder.

3. Install the Package:

    **MacOS/Linux:**
    ```sh
    python -m venv .venv/
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install .
    python -m tag_generator
    ```

    **Windows (PowerShell in Administrator Mode):**
    ```pwsh
    .\tag_generator.exe
    ```
    or
    ```pwsh
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    python -m pip install .
    python -m tag_generator
    ```

    **Windows (Command Prompt):**
    ```cmd  
    powershell -noexit "& tag_generator.exe"
    ```

4. Retrieve the Output:
    ```
    output/
        plc_brand/
            csv/
            json/
    ```
    Your new Ignition tags will be in the corresponding `json` folder.\
    Your new device addressing CSV will be in the corresponding `csv` folder.\
    View the `tag_generation.log` file to see the changes made to the names of the tags.

## Development

1. Clone the Repository:
    ```sh
    git clone https://github.com/FordHBennett/Daikin_Internship_Summer_2024.git
    cd Daikin_Internship_Summer_2024
    ```

2. Install the Package in Editable Mode:

    **MacOS/Linux:**
    ```sh
    python -m venv .venv/
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e .
    python -m tag_generator
    ```

    **Windows (PowerShell):**
    ```pwsh
    python -m venv .venv\
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    python -m pip install -e .
    python -m tag_generator
    ```

## Testing

- **OSX/Linux:**
    To run all tests:
    ```sh
         python -m unittest src.tests -v
    ```
    To run profiler:
    ```sh
        python -m cProfile -o files/profiles/mitsubishi.prof -m tag_generator
        mprof run --backend psutil python -m tag_generator
    ```
- **Windows(PowerShell):**
    To run all tests:
    ```pwsh
        python -m unittest src.tests -v
    ```


## Uninstall the Package
1. Uninstall the Package:
    **MacOS/Linux:**
    ```sh
    rm -rf .venv/
    python -m pip uninstall run-tag-generator
    source deactivate or deactivate
    ```