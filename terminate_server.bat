@echo off
setlocal enabledelayedexpansion

REM Specify the port number you want to find and terminate
set "target_port=5000"

REM Use PowerShell to find the process using the specified port
for /f "tokens=5" %%a in ('netstat -aon ^| find ":%target_port%"') do set "pid=%%a"

REM Debugging: Log the PID and current time
echo PID=%pid% >> "terminatelog.txt"
echo %date% %time% >> "terminatelog.txt"

REM Check if a PID was found
if not defined pid (
    echo No process found on port %target_port%.
) else if not "!pid!" == "" (
    echo Found process with PID %pid% on port %target_port%.
    REM Terminate the process
    powershell Stop-Process -Id %pid% -Force
)

REM Pause at the end to keep the console window open
pause

endlocal
