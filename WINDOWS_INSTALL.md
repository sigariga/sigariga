# 🪟 Windows Installation Guide - PDF Drawing Analysis Tool

Complete step-by-step guide for installing and running the PDF Drawing Analysis Tool on Windows.

## Prerequisites

- Windows 10 or Windows 11
- Administrator access (for some installations)
- Internet connection

## 🚀 Quick Installation (Recommended)

### Option 1: Using Anaconda/Miniconda (Easiest)

1. **Install Anaconda or Miniconda:**
   - Download from: https://www.anaconda.com/download
   - Or Miniconda: https://docs.conda.io/en/latest/miniconda.html
   - Install with default settings

2. **Open Anaconda Prompt:**
   - Press `Win + R`, type `cmd`, press Enter
   - Or search "Anaconda Prompt" in Start Menu

3. **Create Virtual Environment:**
   ```cmd
   conda create -n pdf_analysis python=3.9
   conda activate pdf_analysis
   ```

4. **Install Dependencies:**
   ```cmd
   pip install opencv-python PyMuPDF Pillow numpy matplotlib reportlab pytesseract scikit-image scipy shapely pdfplumber
   ```

5. **Install Tesseract OCR:**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install with default settings
   - Add to PATH: `C:\Program Files\Tesseract-OCR`

6. **Test Installation:**
   ```cmd
   python quick_test.py
   ```

### Option 2: Using Python from Microsoft Store

1. **Install Python:**
   - Open Microsoft Store
   - Search "Python 3.11" or "Python 3.12"
   - Click "Get" and install

2. **Open Command Prompt:**
   - Press `Win + R`, type `cmd`, press Enter

3. **Create Virtual Environment:**
   ```cmd
   python -m venv pdf_analysis_env
   pdf_analysis_env\Scripts\activate
   ```

4. **Install Dependencies:**
   ```cmd
   python -m pip install --upgrade pip
   pip install opencv-python PyMuPDF Pillow numpy matplotlib reportlab pytesseract scikit-image scipy shapely pdfplumber
   ```

5. **Install Tesseract OCR** (see detailed steps below)

## 📋 Detailed Installation Steps

### Step 1: Install Python

#### Method A: Python.org (Official)
1. Go to https://www.python.org/downloads/
2. Download Python 3.9, 3.10, 3.11, or 3.12
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Choose "Install for all users" if you have admin rights

#### Method B: Microsoft Store
1. Open Microsoft Store
2. Search "Python"
3. Install Python 3.11 or newer

#### Method C: Anaconda (Data Science Platform)
1. Download from https://www.anaconda.com/download
2. Install with default settings
3. Use Anaconda Prompt for all commands

### Step 2: Verify Python Installation

Open Command Prompt (`Win + R`, type `cmd`) and test:

```cmd
python --version
pip --version
```

Should show Python 3.7+ and pip version.

### Step 3: Install Tesseract OCR

Tesseract is required for text recognition in drawings.

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest Windows installer
   - File will be named like: `tesseract-ocr-w64-setup-5.x.x.exe`

2. **Install Tesseract:**
   - Run the installer as Administrator
   - Install to default location: `C:\Program Files\Tesseract-OCR`
   - **IMPORTANT:** During installation, select "Add to PATH"

3. **Verify Tesseract:**
   ```cmd
   tesseract --version
   ```

4. **If PATH not working:**
   - Add manually: Control Panel → System → Advanced → Environment Variables
   - Add `C:\Program Files\Tesseract-OCR` to PATH

### Step 4: Download the Application

#### Option A: Git Clone (if you have Git)
```cmd
git clone [repository-url]
cd pdf-drawing-analysis
```

#### Option B: Download ZIP
1. Download the application files as ZIP
2. Extract to a folder like `C:\pdf-drawing-analysis`
3. Open Command Prompt in that folder

### Step 5: Set Up Virtual Environment

**Using venv (Built-in):**
```cmd
python -m venv pdf_analysis_env
pdf_analysis_env\Scripts\activate
```

**Using Anaconda:**
```cmd
conda create -n pdf_analysis python=3.9
conda activate pdf_analysis
```

You should see `(pdf_analysis)` or similar at the beginning of your command prompt.

### Step 6: Install Python Dependencies

**All at once:**
```cmd
pip install opencv-python PyMuPDF Pillow numpy matplotlib reportlab pytesseract scikit-image scipy shapely pdfplumber
```

**Or from requirements.txt:**
```cmd
pip install -r requirements.txt
```

**If you get errors, try one by one:**
```cmd
pip install opencv-python
pip install PyMuPDF
pip install Pillow
pip install numpy
pip install matplotlib
pip install reportlab
pip install pytesseract
pip install scikit-image
pip install scipy
pip install shapely
pip install pdfplumber
```

### Step 7: Test Installation

```cmd
python quick_test.py
```

Expected output:
```
🚀 PDF Drawing Analysis Tool - Quick Test
==================================================
✅ PASS - Python Version
✅ PASS - File Structure  
✅ PASS - Module Syntax
✅ PASS - Basic Imports
✅ PASS - GUI Availability
✅ PASS - Requirements File
✅ PASS - Test PDF Creation
--------------------------------------------------
Tests Passed: 7/7

🎉 All quick tests passed!
```

## 🎮 Running the Application

### GUI Application
```cmd
python main.py
```

### Command Line Demo
```cmd
python demo.py your_drawing.pdf
```

### Full Installation Test
```cmd
python test_installation.py
```

## 🛠️ Troubleshooting Common Windows Issues

### Issue 1: "python is not recognized"

**Solution:**
```cmd
# Try python3 instead
python3 --version

# Or use full path
C:\Users\[username]\AppData\Local\Programs\Python\Python311\python.exe --version

# Add to PATH manually:
# Control Panel → System → Advanced → Environment Variables
# Add Python installation directory to PATH
```

### Issue 2: "pip is not recognized"

**Solution:**
```cmd
# Try full path
python -m pip --version

# Or reinstall Python with "Add to PATH" checked
```

### Issue 3: Tesseract not found

**Error:** `TesseractNotFoundError`

**Solution:**
```cmd
# Check if installed
tesseract --version

# If not working, set environment variable
set TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata

# Or install via conda
conda install -c conda-forge tesseract
```

### Issue 4: OpenCV/GUI Issues

**Error:** Display or OpenCV errors

**Solution:**
```cmd
# Try headless version
pip uninstall opencv-python
pip install opencv-python-headless

# For GUI issues, ensure you're not using SSH/Remote Desktop
# Run locally on the Windows machine
```

### Issue 5: Permission Errors

**Error:** `PermissionError` or `Access denied`

**Solution:**
```cmd
# Run Command Prompt as Administrator
# Right-click Command Prompt → "Run as Administrator"

# Or install for user only
pip install --user [package_name]
```

### Issue 6: Virtual Environment Issues

**Problem:** Cannot activate virtual environment

**Solution:**
```cmd
# Enable execution policy (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
pdf_analysis_env\Scripts\activate
```

### Issue 7: Antivirus Blocking

Some antivirus software may block Python or downloaded files.

**Solution:**
- Add Python installation folder to antivirus exceptions
- Add your project folder to exceptions
- Temporarily disable real-time protection during installation

## 📁 Recommended Folder Structure

```
C:\pdf-drawing-analysis\
├── main.py
├── pdf_processor.py
├── feature_detector.py
├── gdt_detector.py
├── balloon_manager.py
├── annotation_editor.py
├── requirements.txt
├── README.md
├── quick_test.py
├── test_installation.py
├── demo.py
└── pdf_analysis_env\
    └── Scripts\
        ├── activate.bat
        ├── python.exe
        └── pip.exe
```

## 🎯 Quick Start Script for Windows

Create a batch file `install.bat`:

```batch
@echo off
echo Installing PDF Drawing Analysis Tool for Windows...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv pdf_analysis_env

:: Activate virtual environment
echo Activating virtual environment...
call pdf_analysis_env\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing dependencies...
pip install opencv-python PyMuPDF Pillow numpy matplotlib reportlab pytesseract scikit-image scipy shapely pdfplumber

:: Test installation
echo Testing installation...
python quick_test.py

echo.
echo Installation complete!
echo.
echo To run the application:
echo 1. Open Command Prompt in this folder
echo 2. Run: pdf_analysis_env\Scripts\activate
echo 3. Run: python main.py
echo.
pause
```

Save as `install.bat` and double-click to run.

## 🚀 One-Click Startup Script

Create `run_app.bat`:

```batch
@echo off
cd /d "%~dp0"
call pdf_analysis_env\Scripts\activate.bat
python main.py
pause
```

Double-click to start the application.

## 📞 Support

If you encounter issues:

1. **Check Python version:** Must be 3.7+
2. **Verify virtual environment:** Should see `(pdf_analysis)` in prompt
3. **Test components individually:** Run `quick_test.py`
4. **Check antivirus:** May block Python execution
5. **Try administrator mode:** Some installations require admin rights

## 🎉 Success Indicators

You'll know installation succeeded when:

- ✅ `python quick_test.py` shows 7/7 tests passed
- ✅ `python main.py` opens the GUI application
- ✅ You can load and analyze a PDF drawing
- ✅ Annotations and balloons are generated
- ✅ Annotated PDF exports successfully

Happy analyzing! 🎯