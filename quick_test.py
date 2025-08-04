#!/usr/bin/env python3
"""
Quick Test Script for PDF Drawing Analysis Tool
Tests basic functionality without requiring full dependency installation
"""

import sys
import os

def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python version...")
    if sys.version_info >= (3, 7):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Requires 3.7+")
        return False

def test_file_structure():
    """Test that all required files are present"""
    print("\nTesting file structure...")
    
    required_files = [
        'main.py',
        'pdf_processor.py', 
        'feature_detector.py',
        'gdt_detector.py',
        'balloon_manager.py',
        'annotation_editor.py',
        'requirements.txt',
        'README.md',
        'install.sh'
    ]
    
    missing_files = []
    present_files = []
    
    for file in required_files:
        if os.path.exists(file):
            present_files.append(file)
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file} - Missing")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files: {', '.join(missing_files)}")
        return False
    else:
        print(f"\n✅ All {len(present_files)} required files present")
        return True

def test_module_syntax():
    """Test that Python modules have valid syntax"""
    print("\nTesting module syntax...")
    
    modules = [
        'main.py',
        'pdf_processor.py', 
        'feature_detector.py',
        'gdt_detector.py',
        'balloon_manager.py',
        'annotation_editor.py'
    ]
    
    syntax_errors = []
    
    for module in modules:
        try:
            with open(module, 'r') as f:
                content = f.read()
            
            # Basic syntax check
            compile(content, module, 'exec')
            print(f"✅ {module} - Syntax OK")
            
        except SyntaxError as e:
            syntax_errors.append(f"{module}: {e}")
            print(f"❌ {module} - Syntax Error: {e}")
        except FileNotFoundError:
            syntax_errors.append(f"{module}: File not found")
            print(f"❌ {module} - File not found")
        except Exception as e:
            syntax_errors.append(f"{module}: {e}")
            print(f"❌ {module} - Error: {e}")
    
    if syntax_errors:
        print(f"\n⚠️  {len(syntax_errors)} syntax errors found")
        return False
    else:
        print(f"\n✅ All modules have valid syntax")
        return True

def test_basic_imports():
    """Test basic Python standard library imports"""
    print("\nTesting basic imports...")
    
    basic_imports = [
        ('os', 'Operating system interface'),
        ('sys', 'System-specific parameters'),
        ('math', 'Mathematical functions'),
        ('re', 'Regular expressions'),
        ('json', 'JSON encoder/decoder'),
        ('io', 'I/O operations'),
        ('tempfile', 'Temporary files')
    ]
    
    import_errors = []
    
    for module, description in basic_imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            import_errors.append(f"{module}: {e}")
            print(f"❌ {module} - {description} - Error: {e}")
    
    if import_errors:
        print(f"\n⚠️  {len(import_errors)} import errors (basic libraries)")
        return False
    else:
        print(f"\n✅ All basic imports successful")
        return True

def test_gui_availability():
    """Test if GUI framework is available"""
    print("\nTesting GUI availability...")
    
    try:
        import tkinter as tk
        # Try to create a minimal window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ Tkinter GUI framework available")
        return True
    except ImportError:
        print("❌ Tkinter not available - GUI will not work")
        return False
    except Exception as e:
        print(f"⚠️  Tkinter available but display issue: {e}")
        return False

def create_minimal_test_pdf():
    """Create a minimal test PDF using only standard library"""
    print("\nCreating minimal test PDF...")
    
    try:
        # Try to create a simple PDF with reportlab if available
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas('minimal_test.pdf', pagesize=letter)
        c.drawString(100, 750, 'MINIMAL TEST DRAWING')
        c.drawString(100, 700, '100mm')
        c.drawString(100, 650, 'R25')
        c.drawString(100, 600, 'Ø50 ±0.1')
        
        # Draw simple shapes
        c.rect(100, 400, 200, 100)  # Rectangle
        c.circle(200, 450, 25)      # Circle
        
        c.save()
        print("✅ Created minimal_test.pdf")
        return True
        
    except ImportError:
        print("⚠️  ReportLab not available - cannot create test PDF")
        print("    You can test with any existing technical drawing PDF")
        return False
    except Exception as e:
        print(f"❌ Error creating test PDF: {e}")
        return False

def test_requirements_file():
    """Test requirements.txt file"""
    print("\nTesting requirements file...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        print(f"✅ Found {len(requirements)} dependencies in requirements.txt:")
        for req in requirements[:5]:  # Show first 5
            print(f"   - {req}")
        
        if len(requirements) > 5:
            print(f"   ... and {len(requirements) - 5} more")
        
        return True
        
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def main():
    """Run quick tests"""
    print("🚀 PDF Drawing Analysis Tool - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("File Structure", test_file_structure),
        ("Module Syntax", test_module_syntax),
        ("Basic Imports", test_basic_imports),
        ("GUI Availability", test_gui_availability),
        ("Requirements File", test_requirements_file),
        ("Test PDF Creation", create_minimal_test_pdf)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - Unexpected error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("QUICK TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("-" * 50)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All quick tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run full test: python3 test_installation.py")
        print("3. Start GUI: python3 main.py")
        print("4. Or run demo: python3 demo.py your_drawing.pdf")
        
    elif passed >= total * 0.7:  # 70% pass rate
        print("\n⚠️  Most tests passed - likely ready for dependency installation")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run full test: python3 test_installation.py")
        
    else:
        print("\n❌ Several tests failed - check installation")
        print("\nTroubleshooting:")
        print("1. Ensure all files are in the same directory")
        print("2. Check Python version (3.7+ required)")
        print("3. Verify file permissions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)