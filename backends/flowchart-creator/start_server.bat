@echo off
cd /d %~dp0

:: Clear any existing OPENAI_API_KEY environment variable
set OPENAI_API_KEY=

:: Set Python path explicitly
set PYTHON_PATH=C:\\Users\\VincentWashburn\\AppData\\Local\\Programs\\Python\\Python313\\python.exe

:: Check if Python exists at specified path
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at %PYTHON_PATH%
    pause
    exit /b 1
)

:: Only create venv if it doesn\'t exist
if not exist "venv\\" (
    echo Creating new virtual environment...
    "%PYTHON_PATH%" -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )

    call venv\\Scripts\\activate.bat
    if errorlevel 1 (
        echo Error: Failed to activate virtual environment
        pause
        exit /b 1
    )

    echo Upgrading pip...
    "%PYTHON_PATH%" -m pip install --upgrade pip

    echo Installing required packages...
    "%PYTHON_PATH%" -m pip install python-dotenv flask flask-cors python-docx openpyxl
    "%PYTHON_PATH%" -m pip install openai==0.28 --force-reinstall

    :: Show updated package list
    echo.
    echo Updated package list:
    "%PYTHON_PATH%" -m pip list
    echo.
    echo -------------------------------
    echo.
) else (
    echo Using existing virtual environment...
    call venv\\Scripts\\activate.bat
    if errorlevel 1 (
        echo Error: Failed to activate virtual environment
        pause
        exit /b 1
    )
)

:: Run Flask server using virtual environment Python
echo Starting Flowchart Creator Flask server...
"%PYTHON_PATH%" app.py
pause 