@echo off
echo ============================================================
echo  PDF Drawing Analysis Tool - Quick Test
echo ============================================================
echo.

:: Change to the directory where this batch file is located
cd /d "%~dp0"

:: Check if virtual environment exists
if exist pdf_analysis_env (
    echo Found virtual environment, activating...
    call pdf_analysis_env\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python...
)

:: Run the quick test
echo Running quick test...
echo.
python quick_test.py

echo.
echo ============================================================
echo  Test Results Above
echo ============================================================
echo.

if %errorlevel% equ 0 (
    echo ✅ Tests completed successfully!
    echo.
    echo You can now run the application with:
    echo   run_app.bat
    echo.
) else (
    echo ❌ Some tests failed.
    echo.
    echo To fix issues:
    echo 1. Run install.bat if you haven't already
    echo 2. Check WINDOWS_INSTALL.md for troubleshooting
    echo 3. Ensure all application files are present
    echo.
)

pause