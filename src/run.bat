@echo off
setlocal

title Virtual Try-On

echo.
echo ==========================================
echo        VIRTUAL TRY-ON
echo ==========================================
echo.

REM ------------------------------------------
REM Move to project root
REM ------------------------------------------

cd /d "%~dp0"

echo [1/4] Project directory:
echo %CD%
echo.

REM ------------------------------------------
REM Check virtual environment
REM ------------------------------------------

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo [ERROR] Python virtual environment not found.
    echo.
    echo Expected:
    echo %CD%\.venv\Scripts\python.exe
    echo.
    pause
    exit /b 1
)

echo [2/4] Virtual environment found.
echo.

REM ------------------------------------------
REM Check Gradio app
REM ------------------------------------------

if not exist "src\app\gradio_app.py" (
    echo.
    echo [ERROR] gradio_app.py not found.
    echo.
    echo Expected:
    echo %CD%\src\app\gradio_app.py
    echo.
    pause
    exit /b 1
)

echo [3/4] Gradio application found.
echo.

REM ------------------------------------------
REM Start application
REM ------------------------------------------

echo [4/4] Starting Virtual Try-On...
echo.
echo ------------------------------------------
echo  Do not close this window while using
echo  the application.
echo ------------------------------------------
echo.

".venv\Scripts\python.exe" -m src.app.gradio_app

REM ------------------------------------------
REM Application stopped
REM ------------------------------------------

echo.
echo ==========================================
echo        APPLICATION STOPPED
echo ==========================================
echo.

pause
