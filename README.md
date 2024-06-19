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
    run-mitsubishi-tag-generator
    ```

    **Windows (PowerShell in Administrator Mode):**
    ```pwsh
    ./tag_generator.exe
    ```
    or
    ```pwsh
    python.exe -m venv .venv\
    .venv\Scripts\activate
    python.exe -m pip install --upgrade pip
    python.exe -m pip install .
    run-mitsubishi-tag-generator.exe
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
    python -c "import mitsubishi_tag_generator"
    python -c "import base"
    run mitsubishi-tag-generator
    ```

    **Windows (PowerShell):**
    ```pwsh
    python.exe -m venv .venv\
    .venv\Scripts\activate
    python.exe -m pip install --upgrade pip
    python.exe -m pip install -e .
    python.exe -c "import mitsubishi_tag_generator"
    python.exe -c "import base"
    run-mitsubishi-tag-generator.exe
    ```

## Testing

- **OSX/Linux:**
    To run all base tests:
    ```sh
        python -m unittest discover src/tests/base_tests "*_tests.py" -v 
    ```
    To run all mitsubishi_tag_generator tests:
    ```sh
        python -m unittest discover src/tests/mitsubishi_tag_generator_tests "*_tests.py" -v 
    ```
    To run profiler:
    ```sh
        python -m cProfile -m src.mitsubishi_tag_generator.main > tmp/tmp.prof
    ```
- **Windows(PowerShell):**
    To run all base tests:
    ```pwsh
        python.exe -m unittest discover src\tests\base_tests "*_tests.py" -v 
    ```
    To run all mitsubishi_tag_generator tests:
    ```pwsh
        python.exe -m unittest discover src\tests\mitsubishi_tag_generator_tests "*_tests.py" -v 
    ```

## Uninstall the Package
1. Uninstall the Package:
    **MacOS/Linux:**
    ```sh
    rm -rf .venv/
    python -m pip uninstall run-mitsubishi-tag-generator
    source deactivate or deactivate
    ```

    **Windows(PowerShell):**
    ```pwsh
    python.exe -m pip uninstall run-mitsubishi-tag-generator
    deactivate
    ```


Profiling: python -m cProfile -o profiles/mitsubishi.prof -m src.mitsubishi_tag_generator.main