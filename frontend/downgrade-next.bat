@echo off
echo Downgrading Next.js to a compatible version...

REM Install a specific version of Next.js known to work well
call npm install next@13.4.19 react@18.2.0 react-dom@18.2.0 --save

REM Install required runtime dependencies
call npm install --save @babel/runtime

REM Set environment variables
set DISABLE_ESLINT_PLUGIN=true

REM Clean the next cache
if exist .next rmdir /s /q .next

echo Starting Next.js server...
call npx next dev

pause 