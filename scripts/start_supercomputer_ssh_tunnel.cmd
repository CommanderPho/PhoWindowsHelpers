@echo off
setlocal

if "%~1"=="" (
    echo Usage: %~nx0 "ssh -f -N -L port:host:port user@gateway"
    echo        %~nx0 --normal "ssh -f -N -L port:host:port user@gateway"
    exit /b 1
)

if /I "%~1"=="--normal" (
    if "%~2"=="" (
        echo Missing SSH command after --normal
        exit /b 1
    )
    start "GreatLakes VNC Tunnel" cmd /c "%~2"
    exit /b 0
)

start "GreatLakes VNC Tunnel" /min cmd /c "%~1"
