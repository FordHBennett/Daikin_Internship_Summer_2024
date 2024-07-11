try {
    python.exe -m venv .venv\
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    Write-Host "Ensure that Python is installed and added to the PATH environment variable." -ForegroundColor Red
    exit 1
}
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
python.exe -m pip install .
try {
    python.exe -m tag_generator -00 --enable-optimizations --with-lto=full --without-doc-strings 2>&1 | % { Write-Host $_ -NoNewline }
    Write-Host "`nIgnition tags generated successfully."
    Write-Host "Check the files/output folder for the generated tags."
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
}