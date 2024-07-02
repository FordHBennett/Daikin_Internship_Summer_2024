python.exe -m venv .venv\
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
python.exe -m pip install .
run-mitsubishi-tag-generator.exe
#write to the terminal once the script is done