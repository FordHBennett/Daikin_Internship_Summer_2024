python.exe -m venv .venv\
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
python.exe -m pip install .
python.exe -m tag_generator
Write-Host "Ignition tags generated successfully."
Write-Host "Check the files/output folder for the generated tags."