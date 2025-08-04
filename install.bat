@echo off
echo ============================================================
echo  PDF Drawing Analysis Tool - Windows Installer
echo ============================================================
echo.

:: Check if Python is installed
echo [1/8] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python first:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download Python 3.9 or newer
    echo 3. During installation, check "Add Python to PATH"
    echo 4. Restart this installer
    echo.
    pause
    exit /b 1
)

python --version
echo Python found successfully!
echo.

:: Check if pip is available
echo [2/8] Checking pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip not found!
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)
echo pip is available!
echo.

:: Create virtual environment
echo [3/8] Creating virtual environment...
if exist pdf_analysis_env (
    echo Virtual environment already exists, removing old one...
    rmdir /s /q pdf_analysis_env
)

python -m venv pdf_analysis_env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment!
    echo Try running as Administrator.
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

:: Activate virtual environment
echo [4/8] Activating virtual environment...
call pdf_analysis_env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

:: Upgrade pip
echo [5/8] Upgrading pip...
python -m pip install --upgrade pip
echo.

:: Install dependencies
echo [6/8] Installing Python dependencies...
echo This may take a few minutes...
echo.

:: Install packages one by one for better error handling
echo Installing OpenCV...
pip install opencv-python
if %errorlevel% neq 0 (
    echo WARNING: OpenCV installation failed, trying headless version...
    pip install opencv-python-headless
)

echo Installing PyMuPDF...
pip install PyMuPDF

echo Installing Pillow...
pip install Pillow

echo Installing NumPy...
pip install numpy

echo Installing Matplotlib...
pip install matplotlib

echo Installing ReportLab...
pip install reportlab

echo Installing PyTesseract...
pip install pytesseract

echo Installing Scikit-Image...
pip install scikit-image

echo Installing SciPy...
pip install scipy

echo Installing Shapely...
pip install shapely

echo Installing PDFPlumber...
pip install pdfplumber

echo.
echo All Python packages installed!
echo.

:: Check for Tesseract
echo [7/8] Checking Tesseract OCR...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Tesseract OCR not found!
    echo.
    echo Tesseract is required for text recognition in drawings.
    echo Please install it manually:
    echo.
    echo 1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. Download the Windows installer
    echo 3. Install to default location
    echo 4. Make sure "Add to PATH" is selected
    echo.
    echo The application will work with limited functionality without Tesseract.
    echo.
) else (
    tesseract --version
    echo Tesseract OCR found!
    echo.
)

:: Test installation
echo [8/8] Testing installation...
python quick_test.py
if %errorlevel% neq 0 (
    echo.
    echo Installation test had some issues, but you can still try running the app.
) else (
    echo.
    echo Installation test completed successfully!
)

echo.
echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. To run the GUI application:
echo    - Double-click "run_app.bat"
echo    - OR open Command Prompt here and run:
echo      pdf_analysis_env\Scripts\activate
echo      python main.py
echo.
echo 2. To test with a sample PDF:
echo    - Put your PDF file in this folder
echo    - Run: python demo.py your_file.pdf
echo.
echo 3. For help and troubleshooting:
echo    - Read WINDOWS_INSTALL.md
echo    - Read TESTING_GUIDE.md
echo.
echo Happy analyzing!
echo.
pause