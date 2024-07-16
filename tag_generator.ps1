# Possible directories where Python might be installed
$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:PROGRAMFILES\Python",
    "$env:PROGRAMFILES(x86)\Python"
)

# Search for python.exe
$pythonPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path "$path\python.exe") {
        $pythonPath = "$path\python.exe"
        break
    }
}

if ($pythonPath -ne $null) {
    Write-Host "Python found at: $pythonPath"
} else {
    Write-Host "Python executable not found in common directories." -ForegroundColor Red
}


try {
    $pythonPath -m venv .venv\
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    Write-Host "Ensure that Python is installed and added to the PATH environment variable." -ForegroundColor Red
    exit 1
}
.venv\Scripts\activate
$pythonPath -m pip install --upgrade pip
$pythonPath -m pip install .
try {
    $pythonPath -m tag_generator -00 --enable-optimizations --with-lto=full --without-doc-strings 2>&1 | % { Write-Host $_ -NoNewline }
    Write-Host "`nIgnition tags generated successfully."
    Write-Host "Check the files/output folder for the generated tags."
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
}