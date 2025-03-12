@echo off
echo Starting Next.js development server...

REM Install required dependencies
echo Installing required dependencies...
call npm install --save @babel/runtime

REM Set the environment variable to disable SWC
set DISABLE_ESLINT_PLUGIN=true

REM Run the Next.js development server in dev mode
echo Starting Next.js server...
call npx next dev

pause 