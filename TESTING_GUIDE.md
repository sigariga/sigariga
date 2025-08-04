# 🧪 PDF Drawing Analysis Tool - Testing Guide

This guide provides comprehensive instructions for testing the PDF Drawing Analysis application.

## Prerequisites

Before testing, ensure you have:
- Python 3.7+ installed
- A PDF file with technical drawings (mechanical drawings with dimensions and GD&T symbols work best)

## 1. Quick Installation Test

### Option A: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv pdf_analysis_env

# Activate virtual environment
source pdf_analysis_env/bin/activate  # Linux/Mac
# OR
pdf_analysis_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-tk tesseract-ocr tesseract-ocr-eng libgl1-mesa-glx

# Test installation
python3 test_installation.py
```

### Option B: System Installation

```bash
# Use the automated installer
chmod +x install.sh
./install.sh

# Test installation
python3 test_installation.py
```

### Option C: Manual Testing (if dependencies are missing)

```bash
# Test individual components without dependencies
python3 -c "print('Python version check: OK')"
python3 -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}')"
```

## 2. Create Test PDF

If you don't have a technical drawing PDF, you can create a simple test:

```bash
# Create a simple test PDF with dimensions
python3 -c "
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas('test_drawing.pdf', pagesize=letter)
c.drawString(100, 750, 'TEST TECHNICAL DRAWING')
c.drawString(100, 700, '50mm ± 0.1')
c.drawString(100, 650, 'Ø25.4 +0.2/-0.1')
c.drawString(100, 600, 'R12.5')
c.rect(100, 400, 200, 100)
c.drawString(120, 430, '200mm')
c.save()
print('Created test_drawing.pdf')
"
```

## 3. GUI Application Testing

### Start the GUI Application
```bash
python3 main.py
```

### Testing Steps:

1. **Load PDF Test:**
   - Click "Select PDF File"
   - Choose your technical drawing PDF
   - Verify the file loads successfully

2. **Feature Detection Test:**
   - Click "Detect Features"
   - Check the "Detection Results" panel
   - Verify dimensions are found and displayed

3. **GD&T Detection Test:**
   - Click "Detect GD&T"
   - Look for GD&T symbols in results
   - Verify symbols are properly classified

4. **Auto Ballooning Test:**
   - Click "Auto Balloon"
   - Check that balloons appear on the drawing
   - Verify balloon positioning is reasonable

5. **Export Test:**
   - Click "Export Annotated PDF"
   - Choose output location
   - Verify annotated PDF is created

### Expected GUI Behavior:
- ✅ Clean interface with organized panels
- ✅ File browser opens when clicking "Select PDF File"
- ✅ Progress updates in status bar
- ✅ Results displayed in tree view
- ✅ Drawing displayed in main canvas
- ✅ Right-click context menus work
- ✅ Export creates annotated PDF

## 4. Command Line Testing

### Demo Script Test:
```bash
python3 demo.py test_drawing.pdf
```

### Expected Output:
```
PDF Drawing Analysis Tool - Demo
========================================
Analyzing PDF: test_drawing.pdf
==================================================
Step 1: Loading PDF and converting to images...
✓ Converted 1 pages to images
Step 2: Detecting dimensional features...
✓ Found X dimensional features
Step 3: Detecting GD&T symbols...
✓ Found X GD&T symbols
Step 4: Generating balloon annotations...
✓ Generated X balloons
Step 5: Exporting annotated PDF...
✓ Exported annotated PDF: test_drawing_annotated.pdf
```

## 5. Component Testing

### Test Individual Modules:

```bash
# Test PDF processing
python3 -c "
from pdf_processor import PDFProcessor
processor = PDFProcessor()
print('PDF Processor: OK')
"

# Test feature detection
python3 -c "
from feature_detector import FeatureDetector
detector = FeatureDetector()
print('Feature Detector: OK')
"

# Test GD&T detection
python3 -c "
from gdt_detector import GDTDetector
detector = GDTDetector()
print('GD&T Detector: OK')
"

# Test balloon manager
python3 -c "
from balloon_manager import BalloonManager
manager = BalloonManager()
print('Balloon Manager: OK')
"
```

## 6. Performance Testing

### Test with Different PDF Sizes:

```bash
# Time the analysis
time python3 demo.py large_drawing.pdf

# Memory usage monitoring
python3 -c "
import psutil
import os
from pdf_processor import PDFProcessor

process = psutil.Process(os.getpid())
print(f'Memory before: {process.memory_info().rss / 1024 / 1024:.1f} MB')

processor = PDFProcessor()
# Load a PDF here...

print(f'Memory after: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

## 7. Error Testing

### Test Error Handling:

```bash
# Test with invalid PDF
python3 demo.py nonexistent.pdf

# Test with corrupted file
echo "not a pdf" > corrupt.pdf
python3 demo.py corrupt.pdf

# Test with empty PDF
python3 -c "
from reportlab.pdfgen import canvas
c = canvas.Canvas('empty.pdf')
c.save()
"
python3 demo.py empty.pdf
```

## 8. Validation Testing

### Check Output Quality:

1. **Annotated PDF Validation:**
   - Open the generated `*_annotated.pdf`
   - Verify balloons are properly positioned
   - Check that leader lines point to features
   - Ensure original drawing quality is preserved

2. **Feature Detection Accuracy:**
   - Compare detected dimensions with actual drawing
   - Verify units are correctly identified
   - Check tolerance values are accurate

3. **GD&T Symbol Recognition:**
   - Confirm geometric symbols are correctly classified
   - Verify material conditions are identified
   - Check datum references are proper

## 9. Troubleshooting Common Issues

### Installation Issues:
```bash
# If tkinter is missing (Ubuntu/Debian)
sudo apt-get install python3-tk

# If Tesseract is missing
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# If OpenCV issues
pip install opencv-python-headless

# If virtual environment issues
python3 -m pip install --user virtualenv
```

### Runtime Issues:
```bash
# Check Python path
echo $PYTHONPATH

# Check module locations
python3 -c "import sys; print('\n'.join(sys.path))"

# Verify file permissions
ls -la *.py
```

### GUI Issues:
```bash
# Test display connection (Linux)
echo $DISPLAY

# Test X11 forwarding (SSH)
ssh -X username@hostname

# Alternative: Use VNC or remote desktop
```

## 10. Test Results Interpretation

### Good Test Results:
- ✅ All installation tests pass
- ✅ PDF loads without errors
- ✅ Features detected (even if not perfect)
- ✅ Balloons generated and positioned
- ✅ Output PDF created successfully

### Acceptable Test Results:
- ⚠️ Some features missed (accuracy depends on drawing quality)
- ⚠️ Some false positives in detection
- ⚠️ Balloon positioning could be improved

### Problematic Test Results:
- ❌ Application crashes during analysis
- ❌ No features detected in clear drawings
- ❌ Export fails or corrupts PDF
- ❌ GUI doesn't respond or display properly

## 11. Sample Test Files

### Good Test PDFs:
- Mechanical parts with clear dimensions
- Engineering drawings with GD&T symbols
- CAD-generated PDFs (usually have clean text)

### Challenging Test PDFs:
- Hand-drawn sketches
- Scanned drawings (lower quality)
- Complex assemblies with many features
- Multi-page drawings

## 12. Automated Testing Script

Create a comprehensive test:

```bash
#!/bin/bash
# comprehensive_test.sh

echo "Starting comprehensive test..."

# Test 1: Installation
python3 test_installation.py
if [ $? -ne 0 ]; then
    echo "❌ Installation test failed"
    exit 1
fi

# Test 2: Create sample PDF
python3 -c "
from reportlab.pdfgen import canvas
c = canvas.Canvas('auto_test.pdf')
c.drawString(100, 750, 'AUTO TEST DRAWING')
c.drawString(100, 700, '50mm ± 0.1')
c.save()
"

# Test 3: Run demo
python3 demo.py auto_test.pdf
if [ $? -ne 0 ]; then
    echo "❌ Demo test failed"
    exit 1
fi

# Test 4: Check output
if [ -f "auto_test_annotated.pdf" ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Output file not created"
    exit 1
fi

# Cleanup
rm auto_test.pdf auto_test_annotated.pdf 2>/dev/null

echo "🎉 Testing complete!"
```

Run with:
```bash
chmod +x comprehensive_test.sh
./comprehensive_test.sh
```

This comprehensive testing guide covers all aspects of the application and should help you verify that everything is working correctly!