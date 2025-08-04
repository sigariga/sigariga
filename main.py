#!/usr/bin/env python3
"""
PDF Drawing Analysis Tool
Identifies dimensional features and GD&T symbols from technical drawings,
adds auto ballooning, and exports annotated PDFs.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pdf_processor import PDFProcessor
from feature_detector import FeatureDetector
from gdt_detector import GDTDetector
from balloon_manager import BalloonManager
from annotation_editor import AnnotationEditor

class PDFDrawingAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Drawing Analysis Tool")
        self.root.geometry("1200x800")
        
        # Initialize processors
        self.pdf_processor = PDFProcessor()
        self.feature_detector = FeatureDetector()
        self.gdt_detector = GDTDetector()
        self.balloon_manager = BalloonManager()
        self.annotation_editor = AnnotationEditor()
        
        # Current file data
        self.current_pdf_path = None
        self.current_images = []
        self.detected_features = []
        self.gdt_symbols = []
        self.balloons = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Create main menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PDF", command=self.open_pdf)
        file_menu.add_command(label="Export Annotated PDF", command=self.export_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        control_panel = ttk.LabelFrame(main_frame, text="Controls", width=300)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_panel.pack_propagate(False)
        
        # File selection
        ttk.Button(control_panel, text="Select PDF File", 
                  command=self.open_pdf).pack(pady=5, padx=10, fill=tk.X)
        
        self.file_label = ttk.Label(control_panel, text="No file selected", 
                                   wraplength=280)
        self.file_label.pack(pady=5, padx=10)
        
        # Analysis controls
        analysis_frame = ttk.LabelFrame(control_panel, text="Analysis")
        analysis_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(analysis_frame, text="Detect Features", 
                  command=self.detect_features).pack(pady=2, fill=tk.X)
        ttk.Button(analysis_frame, text="Detect GD&T", 
                  command=self.detect_gdt).pack(pady=2, fill=tk.X)
        ttk.Button(analysis_frame, text="Auto Balloon", 
                  command=self.auto_balloon).pack(pady=2, fill=tk.X)
        
        # Detection results
        results_frame = ttk.LabelFrame(control_panel, text="Detection Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Treeview for results
        self.results_tree = ttk.Treeview(results_frame, columns=("Type", "Value"), 
                                        show="tree headings")
        self.results_tree.heading("#0", text="Item")
        self.results_tree.heading("Type", text="Type")
        self.results_tree.heading("Value", text="Value")
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", 
                                 command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel for image display
        self.image_panel = ttk.LabelFrame(main_frame, text="Drawing View")
        self.image_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas for image display
        self.canvas = tk.Canvas(self.image_panel, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def open_pdf(self):
        """Open and process a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF Drawing",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_pdf_path = file_path
            self.file_label.config(text=f"File: {os.path.basename(file_path)}")
            self.status_var.set("Loading PDF...")
            
            try:
                # Convert PDF to images
                self.current_images = self.pdf_processor.pdf_to_images(file_path)
                self.display_image(0)  # Display first page
                self.status_var.set(f"PDF loaded: {len(self.current_images)} pages")
                
                # Clear previous results
                self.clear_results()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")
                self.status_var.set("Error loading PDF")
    
    def detect_features(self):
        """Detect dimensional features in the current drawing"""
        if not self.current_images:
            messagebox.showwarning("Warning", "Please load a PDF first")
            return
            
        self.status_var.set("Detecting dimensional features...")
        
        try:
            # Detect features in all pages
            self.detected_features = []
            for i, image in enumerate(self.current_images):
                features = self.feature_detector.detect_dimensions(image)
                for feature in features:
                    feature['page'] = i
                    self.detected_features.append(feature)
            
            self.update_results_display()
            self.status_var.set(f"Found {len(self.detected_features)} dimensional features")
            
        except Exception as e:
            messagebox.showerror("Error", f"Feature detection failed: {str(e)}")
            self.status_var.set("Feature detection failed")
    
    def detect_gdt(self):
        """Detect GD&T symbols in the current drawing"""
        if not self.current_images:
            messagebox.showwarning("Warning", "Please load a PDF first")
            return
            
        self.status_var.set("Detecting GD&T symbols...")
        
        try:
            # Detect GD&T symbols in all pages
            self.gdt_symbols = []
            for i, image in enumerate(self.current_images):
                symbols = self.gdt_detector.detect_gdt_symbols(image)
                for symbol in symbols:
                    symbol['page'] = i
                    self.gdt_symbols.append(symbol)
            
            self.update_results_display()
            self.status_var.set(f"Found {len(self.gdt_symbols)} GD&T symbols")
            
        except Exception as e:
            messagebox.showerror("Error", f"GD&T detection failed: {str(e)}")
            self.status_var.set("GD&T detection failed")
    
    def auto_balloon(self):
        """Automatically add balloons to detected features"""
        if not self.detected_features and not self.gdt_symbols:
            messagebox.showwarning("Warning", "Please detect features first")
            return
            
        self.status_var.set("Adding balloons...")
        
        try:
            # Generate balloons for all detected items
            all_items = self.detected_features + self.gdt_symbols
            self.balloons = self.balloon_manager.create_balloons(all_items)
            
            self.update_results_display()
            self.display_with_balloons()
            self.status_var.set(f"Added {len(self.balloons)} balloons")
            
        except Exception as e:
            messagebox.showerror("Error", f"Auto ballooning failed: {str(e)}")
            self.status_var.set("Auto ballooning failed")
    
    def export_pdf(self):
        """Export the annotated PDF with balloons"""
        if not self.current_pdf_path or not self.balloons:
            messagebox.showwarning("Warning", "Please load a PDF and add balloons first")
            return
            
        output_path = filedialog.asksaveasfilename(
            title="Save Annotated PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if output_path:
            self.status_var.set("Exporting annotated PDF...")
            
            try:
                self.pdf_processor.export_annotated_pdf(
                    self.current_pdf_path, 
                    output_path,
                    self.balloons,
                    self.detected_features,
                    self.gdt_symbols
                )
                
                messagebox.showinfo("Success", f"Annotated PDF saved to:\n{output_path}")
                self.status_var.set("PDF exported successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
                self.status_var.set("Export failed")
    
    def display_image(self, page_index):
        """Display the specified page on the canvas"""
        if page_index < len(self.current_images):
            # Load image data to annotation editor
            self.annotation_editor.load_image_data(self.current_images[page_index])
            self.annotation_editor.set_canvas(self.canvas)
    
    def display_with_balloons(self):
        """Display the current image with balloon overlays"""
        # Update annotation editor with current data
        self.annotation_editor.set_features(self.detected_features)
        self.annotation_editor.set_balloons(self.balloons)
    
    def update_results_display(self):
        """Update the results tree view"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add dimensional features
        if self.detected_features:
            features_node = self.results_tree.insert("", "end", text="Dimensional Features")
            for i, feature in enumerate(self.detected_features):
                self.results_tree.insert(features_node, "end", 
                                       text=f"Feature {i+1}",
                                       values=(feature.get('type', 'Unknown'), 
                                              feature.get('value', 'N/A')))
        
        # Add GD&T symbols
        if self.gdt_symbols:
            gdt_node = self.results_tree.insert("", "end", text="GD&T Symbols")
            for i, symbol in enumerate(self.gdt_symbols):
                self.results_tree.insert(gdt_node, "end", 
                                       text=f"Symbol {i+1}",
                                       values=(symbol.get('type', 'Unknown'), 
                                              symbol.get('tolerance', 'N/A')))
        
        # Add balloons
        if self.balloons:
            balloons_node = self.results_tree.insert("", "end", text="Balloons")
            for i, balloon in enumerate(self.balloons):
                self.results_tree.insert(balloons_node, "end", 
                                       text=f"Balloon {i+1}",
                                       values=("Balloon", balloon.get('label', f'B{i+1}')))
        
        # Expand all nodes
        for item in self.results_tree.get_children():
            self.results_tree.item(item, open=True)
    
    def clear_results(self):
        """Clear all detection results"""
        self.detected_features = []
        self.gdt_symbols = []
        self.balloons = []
        self.update_results_display()

def main():
    root = tk.Tk()
    app = PDFDrawingAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()