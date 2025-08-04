#!/usr/bin/env python3
"""
Demo script for PDF Drawing Analysis Tool
Shows how to use the application programmatically
"""

import os
import sys
from pdf_processor import PDFProcessor
from feature_detector import FeatureDetector
from gdt_detector import GDTDetector
from balloon_manager import BalloonManager

def demo_analysis(pdf_path):
    """Demonstrate the analysis workflow"""
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    print(f"Analyzing PDF: {pdf_path}")
    print("=" * 50)
    
    try:
        # Initialize processors
        pdf_processor = PDFProcessor()
        feature_detector = FeatureDetector()
        gdt_detector = GDTDetector()
        balloon_manager = BalloonManager()
        
        # Step 1: Load and convert PDF
        print("Step 1: Loading PDF and converting to images...")
        images = pdf_processor.pdf_to_images(pdf_path)
        print(f"✓ Converted {len(images)} pages to images")
        
        # Step 2: Detect dimensional features
        print("\nStep 2: Detecting dimensional features...")
        all_features = []
        for i, image_data in enumerate(images):
            features = feature_detector.detect_dimensions(image_data)
            for feature in features:
                feature['page'] = i
            all_features.extend(features)
        print(f"✓ Found {len(all_features)} dimensional features")
        
        # Display some feature details
        if all_features:
            print("Sample features:")
            for i, feature in enumerate(all_features[:5]):  # Show first 5
                print(f"  {i+1}. Type: {feature.get('type', 'Unknown')}, "
                      f"Value: {feature.get('value', 'N/A')}")
        
        # Step 3: Detect GD&T symbols
        print("\nStep 3: Detecting GD&T symbols...")
        all_gdt_symbols = []
        for i, image_data in enumerate(images):
            symbols = gdt_detector.detect_gdt_symbols(image_data)
            for symbol in symbols:
                symbol['page'] = i
            all_gdt_symbols.extend(symbols)
        print(f"✓ Found {len(all_gdt_symbols)} GD&T symbols")
        
        # Display some GD&T details
        if all_gdt_symbols:
            print("Sample GD&T symbols:")
            for i, symbol in enumerate(all_gdt_symbols[:3]):  # Show first 3
                print(f"  {i+1}. Type: {symbol.get('symbol_type', 'Unknown')}, "
                      f"Tolerance: {symbol.get('tolerance', 'N/A')}")
        
        # Step 4: Generate balloons
        print("\nStep 4: Generating balloon annotations...")
        all_items = all_features + all_gdt_symbols
        balloons = balloon_manager.create_balloons(all_items)
        print(f"✓ Generated {len(balloons)} balloons")
        
        # Display balloon table
        if balloons:
            print("\nBalloon summary:")
            table_data = balloon_manager.create_balloon_table(balloons)
            for row in table_data[:10]:  # Show first 10
                print(f"  Balloon {row['balloon_number']}: {row['description']} - {row['value']}")
        
        # Step 5: Export annotated PDF
        print("\nStep 5: Exporting annotated PDF...")
        output_path = pdf_path.replace('.pdf', '_annotated.pdf')
        pdf_processor.export_annotated_pdf(
            pdf_path, output_path, balloons, all_features, all_gdt_symbols
        )
        print(f"✓ Exported annotated PDF: {output_path}")
        
        # Summary
        print("\nAnalysis Summary:")
        print("-" * 30)
        print(f"Input PDF: {pdf_path}")
        print(f"Pages processed: {len(images)}")
        print(f"Dimensional features: {len(all_features)}")
        print(f"GD&T symbols: {len(all_gdt_symbols)}")
        print(f"Balloons generated: {len(balloons)}")
        print(f"Output PDF: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_report(balloons, features, gdt_symbols, output_file="analysis_report.txt"):
    """Create a text report of the analysis"""
    
    with open(output_file, 'w') as f:
        f.write("PDF Drawing Analysis Report\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Total Features Detected: {len(features) + len(gdt_symbols)}\n")
        f.write(f"Dimensional Features: {len(features)}\n")
        f.write(f"GD&T Symbols: {len(gdt_symbols)}\n")
        f.write(f"Balloons Generated: {len(balloons)}\n\n")
        
        if features:
            f.write("Dimensional Features:\n")
            f.write("-" * 20 + "\n")
            for i, feature in enumerate(features, 1):
                f.write(f"{i}. Type: {feature.get('type', 'Unknown')}\n")
                f.write(f"   Value: {feature.get('value', 'N/A')}\n")
                f.write(f"   Page: {feature.get('page', 0) + 1}\n\n")
        
        if gdt_symbols:
            f.write("GD&T Symbols:\n")
            f.write("-" * 13 + "\n")
            for i, symbol in enumerate(gdt_symbols, 1):
                f.write(f"{i}. Type: {symbol.get('symbol_type', 'Unknown')}\n")
                f.write(f"   Tolerance: {symbol.get('tolerance', 'N/A')}\n")
                f.write(f"   Page: {symbol.get('page', 0) + 1}\n\n")
        
        if balloons:
            f.write("Balloon Annotations:\n")
            f.write("-" * 19 + "\n")
            for balloon in balloons:
                f.write(f"Balloon {balloon['label']}: {balloon.get('item_type', 'Unknown')}\n")
    
    print(f"✓ Analysis report saved: {output_file}")

def main():
    """Main demo function"""
    print("PDF Drawing Analysis Tool - Demo")
    print("=" * 40)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Look for sample PDF files in current directory
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        
        if pdf_files:
            pdf_path = pdf_files[0]
            print(f"Using sample PDF: {pdf_path}")
        else:
            print("Usage: python3 demo.py <pdf_file>")
            print("\nNo PDF file specified and no sample PDFs found.")
            print("Please provide a PDF file containing technical drawings.")
            return False
    
    # Run the demo analysis
    success = demo_analysis(pdf_path)
    
    if success:
        print("\nDemo completed successfully!")
        print("You can now:")
        print("1. Check the generated annotated PDF")
        print("2. Run the GUI application: python3 main.py")
        print("3. View the analysis report: analysis_report.txt")
    else:
        print("\nDemo failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()