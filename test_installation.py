#!/usr/bin/env python3
"""
Test script to verify PDF Drawing Analysis Tool installation
"""

import sys
import importlib
import traceback

def test_import(module_name, description=""):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} - {description}")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - {description} - Error: {e}")
        return False

def test_opencv():
    """Test OpenCV functionality"""
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
        return True
    except Exception as e:
        print(f"✗ OpenCV test failed: {e}")
        return False

def test_tesseract():
    """Test Tesseract OCR"""
    try:
        import pytesseract
        # Try to get tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract version: {version}")
        return True
    except Exception as e:
        print(f"✗ Tesseract test failed: {e}")
        return False

def test_pdf_processing():
    """Test PDF processing capabilities"""
    try:
        import fitz  # PyMuPDF
        print(f"✓ PyMuPDF version: {fitz.version}")
        return True
    except Exception as e:
        print(f"✗ PDF processing test failed: {e}")
        return False

def test_gui():
    """Test GUI capabilities"""
    try:
        import tkinter as tk
        # Try to create a root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✓ Tkinter GUI framework")
        return True
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        return False

def test_application_modules():
    """Test application-specific modules"""
    modules_to_test = [
        ('pdf_processor', 'PDF Processing Module'),
        ('feature_detector', 'Feature Detection Module'), 
        ('gdt_detector', 'GD&T Detection Module'),
        ('balloon_manager', 'Balloon Management Module'),
        ('annotation_editor', 'Annotation Editor Module')
    ]
    
    results = []
    for module, description in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"✓ {module} - {description}")
            results.append(True)
        except ImportError as e:
            print(f"✗ {module} - {description} - Error: {e}")
            results.append(False)
    
    return all(results)

def main():
    """Run all installation tests"""
    print("PDF Drawing Analysis Tool - Installation Test")
    print("=" * 50)
    
    # Test Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("✗ Python 3.7+ required")
        return False
    else:
        print("✓ Python version OK")
    
    print("\nTesting Core Dependencies:")
    print("-" * 30)
    
    # Test core dependencies
    core_deps = [
        ('numpy', 'NumPy for numerical operations'),
        ('cv2', 'OpenCV for computer vision'),
        ('PIL', 'Pillow for image processing'),
        ('fitz', 'PyMuPDF for PDF processing'),
        ('pytesseract', 'Tesseract OCR for text recognition'),
        ('scipy', 'SciPy for scientific computing'),
        ('shapely', 'Shapely for geometric operations'),
        ('matplotlib', 'Matplotlib for plotting'),
        ('reportlab', 'ReportLab for PDF generation'),
        ('tkinter', 'Tkinter for GUI'),
        ('skimage', 'Scikit-image for image processing')
    ]
    
    core_results = []
    for module, desc in core_deps:
        core_results.append(test_import(module, desc))
    
    print("\nTesting Specific Functionality:")
    print("-" * 30)
    
    # Test specific functionality
    func_results = [
        test_opencv(),
        test_tesseract(),
        test_pdf_processing(),
        test_gui()
    ]
    
    print("\nTesting Application Modules:")
    print("-" * 30)
    
    app_result = test_application_modules()
    
    print("\nTest Summary:")
    print("-" * 30)
    
    all_passed = all(core_results) and all(func_results) and app_result
    
    if all_passed:
        print("✓ All tests passed! Installation is successful.")
        print("\nYou can now run the application with:")
        print("  python3 main.py")
    else:
        print("✗ Some tests failed. Please check the installation.")
        print("\nTroubleshooting:")
        print("1. Run: pip3 install -r requirements.txt")
        print("2. Install system dependencies: sudo apt-get install python3-tk tesseract-ocr")
        print("3. Check that all application modules are in the same directory")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)