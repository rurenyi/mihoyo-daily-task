rem fetch process on port 16384
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :16384') do (
    rem killing the process
    taskkill /PID %%a /F
    echo process %%a killed
)

rem no process found
if errorlevel 1 (
    echo no process on port 16384
)
