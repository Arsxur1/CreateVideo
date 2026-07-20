@echo off
setlocal EnableDelayedExpansion
set "forward="

:next
if "%~1"=="" goto run
if /I "%~1"=="--color" (
  shift
  shift
  goto next
)
set "forward=!forward! "%~1""
shift
goto next

:run
"C:\nvm4w\nodejs\codex.cmd" %forward%
exit /b %ERRORLEVEL%
