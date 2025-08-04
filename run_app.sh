#!/bin/bash

# SPC Analysis Application Startup Script

echo "🚀 Starting SPC Analysis - Cp & Cpk Calculator..."
echo "==============================================="

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed!"
fi

# Add local bin to PATH if not present
export PATH=$PATH:/home/ubuntu/.local/bin

echo "📊 Launching application..."
echo "🌐 The app will be available at: http://localhost:8501"
echo "💡 Press Ctrl+C to stop the application"
echo ""

# Start the Streamlit application
streamlit run spc_app.py --server.headless false --server.port 8501

echo ""
echo "👋 Thanks for using SPC Analysis!"