# PDF Drawing Analysis Tool

A comprehensive application for analyzing PDF technical drawings, identifying dimensional features and GD&T symbols, and automatically adding balloon annotations.

## Features

- **PDF Processing**: Convert PDF drawings to high-resolution images for analysis
- **Dimensional Feature Detection**: Automatically identify dimensions, tolerances, and measurements
- **GD&T Symbol Recognition**: Detect and classify geometric dimensioning and tolerancing symbols
- **Auto Ballooning**: Intelligently place balloon annotations with optimal positioning
- **Interactive Editing**: Edit and adjust annotations before export
- **Annotated PDF Export**: Export results as annotated PDF files

## Installation

### Quick Installation
Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

### Manual Installation

1. **System Dependencies** (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3-tk tesseract-ocr tesseract-ocr-eng libgl1-mesa-glx
```

2. **Python Dependencies**:
```bash
pip3 install -r requirements.txt
```

## Usage

1. **Start the Application**:
```bash
python3 main.py
```

2. **Load PDF Drawing**:
   - Click "Select PDF File"
   - Choose your technical drawing PDF

3. **Analyze Drawing**:
   - Click "Detect Features" to find dimensional features
   - Click "Detect GD&T" to find GD&T symbols
   - Review detected items in the results panel

4. **Add Balloons**:
   - Click "Auto Balloon" to automatically add balloon annotations
   - Use right-click context menu to manually add or edit balloons

5. **Export Results**:
   - Click "Export Annotated PDF"
   - Save the annotated drawing

## Supported Features

### Dimensional Features
- Linear dimensions with units (mm, in, inch)
- Diameter symbols (Ø)
- Radius indicators (R)
- Tolerances (±, +/-)
- Dimension lines and arrows

### GD&T Symbols
- Feature control frames
- Geometric symbols (straightness, flatness, circularity, etc.)
- Material condition modifiers (MMC, LMC, RFS)
- Datum references
- Position tolerances

### Balloon Features
- Automatic optimal positioning
- Leader line generation
- Collision avoidance
- Manual editing and adjustment
- Export to annotated PDF

## Requirements

- Python 3.7+
- OpenCV
- PyMuPDF
- Pillow
- Tesseract OCR
- NumPy
- Tkinter (usually included with Python)

## Architecture

The application consists of several key modules:

- `main.py`: Main GUI application
- `pdf_processor.py`: PDF loading and export functionality
- `feature_detector.py`: Computer vision for dimensional feature detection
- `gdt_detector.py`: GD&T symbol recognition and classification
- `balloon_manager.py`: Automatic balloon placement algorithms
- `annotation_editor.py`: Interactive editing interface

## Contributing

This project welcomes contributions in:
- Computer vision algorithms for better feature detection
- GD&T symbol templates and recognition patterns
- UI/UX improvements
- Performance optimizations
- Documentation and examples

## License

MIT License - see LICENSE file for details.

## Author

Ahmad78 - Interested in vision applications, machine learning, and industrial automation.
