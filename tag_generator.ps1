
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
    if ($null -ne $pythonPath) {
        break
    }
}

if ($null -ne $pythonPath) {
    Write-Host "Python found at: $pythonPath"
} else {
    Write-Host "Make sure you have python installed." -ForegroundColor Red
}

try {
    & $pythonPath "-m" "venv" ".venv" 2>&1 | ForEach-Object { Write-Host $_ }
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    Write-Host "Ensure that Python is installed and added to the PATH environment variable." -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully."

try{
    .venv\Scripts\activate 2>&1 | ForEach-Object { Write-Host $_ }
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    exit 1

}
Write-Host "Virtual environment activated."

$env_python_path = ".venv\Scripts\python.exe"

& $env_python_path "-m" "pip" "install" "--upgrade" "pip" 2>&1 | Out-Null

try {
     & $env_python_path "-m" "pip" "install" "." 2>&1 | ForEach-Object { Write-Host $_ }
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
    exit 1
}


try {
    & $env_python_path "-m" "tag_generator" "-00" "--enable-optimizations" "--with-lto=full" "--without-doc-strings" 2>&1 | ForEach-Object { Write-Host $_ }
    Write-Host "`nIgnition tags generated successfully." -ForegroundColor Green
    $local_path = Get-Location
    Write-Host "Check the $local_path/files/output directory for the generated tags." -ForegroundColor Green
} catch {
    Write-Host "An error occurred: $($_)" -ForegroundColor Red
}