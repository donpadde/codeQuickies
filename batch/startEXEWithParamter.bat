@echo off
rem batch script to start a .exe file and wait for it to finish
rem exe can be called with parameters
rem the .exe is started and the script waits for it to finish and checks the exit code of the .exe to see if it finished successfully or not
rem set path to .exe file and check if it exists
set exe="path\to\executable\test.exe"
if not exist %exe% (
    echo %exe% does not exist
    exit /b 1
)
rem ask the user for paramters
rem more parameters can be added
set /p parameter_one="Enter parameter 1: "
set /p parameter_two="Enter parameter 2: "
rem start the .exe stored in %exe% with the parameters
%exe% %parameter_one% %parameter_two%
if %errorlevel%==0 (
    rem set color to green
    color 0A
    echo Executable finished successfully
) else (
    rem set color to red
    color 0C
    echo Executable finished with error
)
