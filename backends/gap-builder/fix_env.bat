@echo off
cd /d %~dp0

echo Fixing .env file configuration...

if exist ".env.fixed" (
    echo Found .env.fixed file. Replacing .env with fixed version.
    if exist ".env" (
        echo Backing up original .env to .env.backup
        copy .env .env.backup
        del .env
    )
    copy .env.fixed .env
    echo Fixed .env file copied successfully.
) else (
    echo ERROR: Fixed .env file (.env.fixed) not found!
    exit /b 1
)

echo.
echo Testing OpenAI configuration...
call test_openai.bat

echo.
echo Environment configuration fixed.
pause 