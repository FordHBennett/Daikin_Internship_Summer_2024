
# Possible directories where Python might be installed
$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:PROGRAMFILES\Python",
    "$env:PROGRAMFILES(x86)\Python"
)



# Search for python.exe
$pythonPath = $null
foreach ($path in $possiblePaths) {
    #recursive search for python.exe in the directory
    $pythonPath = Get-ChildItem -Path $path -Recurse -Filter "python.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
    if ($pythonPath -ne $null) {
        break
    }
}

if ($pythonPath -ne $null) {
    Write-Host "Python found at: $pythonPath"
} else {
    Write-Host "Python executable not found in common directories." -ForegroundColor Red
}

try {
    & $pythonPath "-m" "venv" ".venv"
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    Write-Host "Ensure that Python is installed and added to the PATH environment variable." -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully."

try{
    .venv\Scripts\activate
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    exit 1

}
Write-Host "Virtual environment activated."

$env_python_path = ".venv\Scripts\python.exe"

& $env_python_path "-m" "pip" "install" "--upgrade" "pip"

try {
    & $env_python_path "-m" "pip" "install" "."
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    exit 1
}


try {
    & $env_python_path "-m" "tag_generator" "-00" "--enable-optimizations" "--with-lto=full" "--without-doc-strings" 2>&1 | % { Write-Host $_ -NoNewline }
    Write-Host "`nIgnition tags generated successfully."
    Write-Host "Check the files/output folder for the generated tags."
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
}