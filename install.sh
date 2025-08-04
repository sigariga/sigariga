#!/bin/bash

# PDF Drawing Analysis Tool Installation Script

echo "Installing PDF Drawing Analysis Tool..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Install system dependencies (Ubuntu/Debian)
if command -v apt-get &> /dev/null; then
    echo "Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        python3-tk \
        tesseract-ocr \
        tesseract-ocr-eng \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create data directories
mkdir -p data/templates
mkdir -p data/models
mkdir -p output

# Make the main script executable
chmod +x main.py

echo "Installation complete!"
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
echo "Requirements:"
echo "  - PDF files with technical drawings"
echo "  - Tesseract OCR installed for text recognition"
echo "  - At least 4GB RAM for processing large drawings"
echo ""
echo "Usage:"
echo "  1. Open the application: python3 main.py"
echo "  2. Load a PDF drawing using 'Select PDF File'"
echo "  3. Click 'Detect Features' to find dimensional features"
echo "  4. Click 'Detect GD&T' to find GD&T symbols"
echo "  5. Click 'Auto Balloon' to add balloon annotations"
echo "  6. Export the annotated PDF using 'Export Annotated PDF'"