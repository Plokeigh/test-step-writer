@echo off
cd /d %~dp0

:: Set Python path explicitly
set PYTHON_PATH=C:\Users\VincentWashburn\AppData\Local\Programs\Python\Python313\python.exe

:: Check if Python exists at specified path
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at %PYTHON_PATH%
    echo Trying system Python instead...
    set PYTHON_PATH=python
)

:: Activate venv if it exists
if exist "venv\" (
    echo Using existing virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python...
)

:: Run the test script
echo Running OpenAI API connection test...
"%PYTHON_PATH%" test_openai.py
if errorlevel 1 (
    echo Test FAILED. Please check your .env file configuration.
) else (
    echo Test PASSED. Your OpenAI API configuration is working correctly.
)

pause 