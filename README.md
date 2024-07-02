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
    run-mitsubishi-tag-generator
    ```

    **Windows (PowerShell):**
    ```pwsh
    python.exe -m venv .venv\
    .venv\Scripts\activate
    python.exe -m pip install --upgrade pip
    python.exe -m pip install -e .
    run-mitsubishi-tag-generator.exe
    ```

## Testing

- **OSX/Linux:**
    To run all tests:
    ```sh
         python -m unittest src.tests -v
    ```
    To run profiler:
    ```sh
        python -m cProfile -m src.mitsubishi_tag_generator.main > tmp/tmp.prof
    ```
- **Windows(PowerShell):**
    To run all tests:
    ```pwsh
        python.exe -m unittest src.tests -v
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


Profiling: 
python -m cProfile -o files/profiles/mitsubishi.prof -m tag_generator 
snakeviz files/profiles/mitsubishi.prof
 
mprof run --backend psutil python -m tag_generator


Note: If your tags are not appearing as expected for a large tag import, the Designer's memory allocation may need to be increased. Access your Gateway and navigate to the Config > Gateway Settings > Designer Memory to adjust memory limitations. The default size is 1.0 GB, with available dropdown options from MB128 to 4.0 GB.