@echo off
echo ============================================================
echo  PDF Drawing Analysis Tool - Starting Application
echo ============================================================
echo.

:: Change to the directory where this batch file is located
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist pdf_analysis_env (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run install.bat first to set up the application.
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call pdf_analysis_env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment!
    echo Please try running install.bat again.
    pause
    exit /b 1
)

:: Check if main.py exists
if not exist main.py (
    echo ERROR: main.py not found!
    echo Please ensure all application files are in this directory.
    pause
    exit /b 1
)

echo Starting PDF Drawing Analysis Tool...
echo.
echo The GUI application window should open shortly.
echo If it doesn't appear, check for error messages below.
echo.
echo To close the application, close the GUI window or press Ctrl+C here.
echo.

:: Run the main application
python main.py

:: Check if there was an error
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo  Application exited with an error
    echo ============================================================
    echo.
    echo If you see import errors, try running install.bat again.
    echo.
    echo For help, check:
    echo - WINDOWS_INSTALL.md
    echo - TESTING_GUIDE.md
    echo.
    echo Or run quick_test.py to diagnose issues:
    echo   python quick_test.py
    echo.
) else (
    echo.
    echo Application closed normally.
)

echo.
pause