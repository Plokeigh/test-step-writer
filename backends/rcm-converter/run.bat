@echo off
setlocal

:: Redirect output to a log file for debugging
echo %date% %time% - Starting RCM Converter... > "%~dp0conversion_log.txt"

:: Set Python path explicitly
set PYTHON_PATH=C:\Users\VincentWashburn\AppData\Local\Programs\Python\Python313\python.exe
echo %date% %time% - Using Python: %PYTHON_PATH% >> "%~dp0conversion_log.txt"

:: Check if Python exists at specified path
if not exist "%PYTHON_PATH%" (
    echo %date% %time% - Error: Python not found at %PYTHON_PATH% >> "%~dp0conversion_log.txt"
    echo {"status": "error", "message": "Python installation not found"}
    exit /b 1
)

:: Check if we have the required arguments
if "%~1"=="" (
    echo %date% %time% - Error: Missing input file argument >> "%~dp0conversion_log.txt"
    echo {"status": "error", "message": "Missing input file parameter"}
    exit /b 1
)

:: Set the input file path
set INPUT_FILE=%~1
echo %date% %time% - Input file: %INPUT_FILE% >> "%~dp0conversion_log.txt"

:: Check if input file exists
if not exist "%INPUT_FILE%" (
    echo %date% %time% - Error: Input file not found: %INPUT_FILE% >> "%~dp0conversion_log.txt"
    echo {"status": "error", "message": "Input file not found"}
    exit /b 1
)

:: Set the template file path - use default or provided
if "%~2"=="" (
    set TEMPLATE_FILE=%~dp0templates\rcm-control-view.xlsx
) else (
    set TEMPLATE_FILE=%~2
)
echo %date% %time% - Template file: %TEMPLATE_FILE% >> "%~dp0conversion_log.txt"

:: Check if the template file exists
if not exist "%TEMPLATE_FILE%" (
    echo %date% %time% - Error: Template file not found: %TEMPLATE_FILE% >> "%~dp0conversion_log.txt"
    echo {"status": "error", "message": "Template file not found"}
    exit /b 1
)

:: Create output directory if it doesn't exist
set OUTPUT_DIR=%~dp0output
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Install dependencies if needed - only do this first time
if not exist "%~dp0.dependencies_installed" (
    echo %date% %time% - Installing dependencies... >> "%~dp0conversion_log.txt"
    "%PYTHON_PATH%" -m pip install -r "%~dp0requirements.txt" >> "%~dp0conversion_log.txt" 2>&1
    if %ERRORLEVEL% neq 0 (
        echo %date% %time% - Error: Failed to install dependencies >> "%~dp0conversion_log.txt"
        echo {"status": "error", "message": "Failed to install Python dependencies"}
        exit /b 1
    )
    echo 1 > "%~dp0.dependencies_installed"
)

:: Run the Python script
echo %date% %time% - Running converter script... >> "%~dp0conversion_log.txt"
"%PYTHON_PATH%" "%~dp0app\main.py" "%INPUT_FILE%" "%TEMPLATE_FILE%" >> "%~dp0conversion_log.txt" 2>&1
if %ERRORLEVEL% neq 0 (
    echo %date% %time% - Error: Conversion script failed >> "%~dp0conversion_log.txt"
    echo {"status": "error", "message": "Conversion process failed"}
    exit /b 1
)

echo %date% %time% - Conversion completed successfully >> "%~dp0conversion_log.txt"
echo {"status": "success", "message": "Conversion completed successfully"}
endlocal 