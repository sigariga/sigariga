#!/usr/bin/env python3
"""
PDF Processor Module
Handles PDF loading, conversion to images, and export of annotated PDFs.
"""

import fitz  # PyMuPDF
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os
import tempfile

class PDFProcessor:
    def __init__(self):
        self.dpi = 300  # High resolution for better feature detection
        
    def pdf_to_images(self, pdf_path):
        """Convert PDF pages to high-resolution images for analysis"""
        try:
            pdf_document = fitz.open(pdf_path)
            images = []
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Create transformation matrix for high DPI
                mat = fitz.Matrix(self.dpi / 72.0, self.dpi / 72.0)
                
                # Render page to pixmap
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("ppm")
                from io import BytesIO
                img = Image.open(BytesIO(img_data))
                
                # Convert to numpy array for OpenCV processing
                img_array = np.array(img)
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                
                images.append({
                    'pil_image': img,
                    'cv_image': img_cv,
                    'page_num': page_num,
                    'width': img.width,
                    'height': img.height
                })
            
            pdf_document.close()
            return images
            
        except Exception as e:
            raise Exception(f"Error converting PDF to images: {str(e)}")
    
    def export_annotated_pdf(self, input_pdf_path, output_pdf_path, balloons, features, gdt_symbols):
        """Export PDF with annotations and balloons"""
        try:
            # Open the original PDF
            input_doc = fitz.open(input_pdf_path)
            
            # Create a new PDF document
            output_doc = fitz.open()
            
            for page_num in range(len(input_doc)):
                # Copy the original page
                input_page = input_doc.load_page(page_num)
                output_page = output_doc.new_page(width=input_page.rect.width, 
                                                height=input_page.rect.height)
                
                # Insert the original page content
                output_page.show_pdf_page(output_page.rect, input_doc, page_num)
                
                # Add annotations for this page
                self._add_page_annotations(output_page, page_num, balloons, features, gdt_symbols)
            
            # Save the annotated PDF
            output_doc.save(output_pdf_path)
            output_doc.close()
            input_doc.close()
            
        except Exception as e:
            raise Exception(f"Error exporting annotated PDF: {str(e)}")
    
    def _add_page_annotations(self, page, page_num, balloons, features, gdt_symbols):
        """Add annotations to a specific page"""
        # Filter items for this page
        page_balloons = [b for b in balloons if b.get('page', 0) == page_num]
        page_features = [f for f in features if f.get('page', 0) == page_num]
        page_gdt = [g for g in gdt_symbols if g.get('page', 0) == page_num]
        
        # Add balloon annotations
        for balloon in page_balloons:
            self._add_balloon_annotation(page, balloon)
        
        # Add feature highlighting
        for feature in page_features:
            self._add_feature_highlight(page, feature)
        
        # Add GD&T symbol highlighting
        for symbol in page_gdt:
            self._add_gdt_highlight(page, symbol)
    
    def _add_balloon_annotation(self, page, balloon):
        """Add a balloon annotation to the page"""
        # Scale coordinates from image space to PDF space
        x, y = self._scale_coordinates(balloon['x'], balloon['y'], balloon['image_width'], 
                                     balloon['image_height'], page.rect.width, page.rect.height)
        
        # Create balloon circle
        circle_radius = 15
        circle_rect = fitz.Rect(x - circle_radius, y - circle_radius, 
                               x + circle_radius, y + circle_radius)
        
        # Add circle annotation
        circle_annot = page.add_circle_annot(circle_rect)
        circle_annot.set_colors(stroke=colors.red)
        circle_annot.set_border(width=2)
        circle_annot.update()
        
        # Add text annotation with balloon number
        text_rect = fitz.Rect(x - 5, y - 5, x + 5, y + 5)
        text_annot = page.add_text_annot(fitz.Point(x, y), balloon['label'])
        text_annot.set_info(content=f"Balloon {balloon['label']}")
        text_annot.update()
        
        # Add leader line if specified
        if 'leader_end_x' in balloon and 'leader_end_y' in balloon:
            end_x, end_y = self._scale_coordinates(balloon['leader_end_x'], balloon['leader_end_y'],
                                                 balloon['image_width'], balloon['image_height'],
                                                 page.rect.width, page.rect.height)
            
            # Create line annotation
            line_annot = page.add_line_annot(fitz.Point(x, y), fitz.Point(end_x, end_y))
            line_annot.set_colors(stroke=colors.red)
            line_annot.set_border(width=1)
            line_annot.update()
    
    def _add_feature_highlight(self, page, feature):
        """Add highlighting for dimensional features"""
        # Scale bounding box coordinates
        x1, y1 = self._scale_coordinates(feature['bbox'][0], feature['bbox'][1],
                                       feature['image_width'], feature['image_height'],
                                       page.rect.width, page.rect.height)
        x2, y2 = self._scale_coordinates(feature['bbox'][2], feature['bbox'][3],
                                       feature['image_width'], feature['image_height'],
                                       page.rect.width, page.rect.height)
        
        # Create highlight rectangle
        highlight_rect = fitz.Rect(x1, y1, x2, y2)
        highlight_annot = page.add_highlight_annot(highlight_rect)
        highlight_annot.set_colors(stroke=colors.blue, fill=colors.lightblue)
        highlight_annot.set_info(content=f"Dimension: {feature.get('value', 'Unknown')}")
        highlight_annot.update()
    
    def _add_gdt_highlight(self, page, symbol):
        """Add highlighting for GD&T symbols"""
        # Scale bounding box coordinates
        x1, y1 = self._scale_coordinates(symbol['bbox'][0], symbol['bbox'][1],
                                       symbol['image_width'], symbol['image_height'],
                                       page.rect.width, page.rect.height)
        x2, y2 = self._scale_coordinates(symbol['bbox'][2], symbol['bbox'][3],
                                       symbol['image_width'], symbol['image_height'],
                                       page.rect.width, page.rect.height)
        
        # Create highlight rectangle
        highlight_rect = fitz.Rect(x1, y1, x2, y2)
        highlight_annot = page.add_highlight_annot(highlight_rect)
        highlight_annot.set_colors(stroke=colors.green, fill=colors.lightgreen)
        highlight_annot.set_info(content=f"GD&T: {symbol.get('type', 'Unknown')}")
        highlight_annot.update()
    
    def _scale_coordinates(self, img_x, img_y, img_width, img_height, pdf_width, pdf_height):
        """Scale coordinates from image space to PDF space"""
        scale_x = pdf_width / img_width
        scale_y = pdf_height / img_height
        
        pdf_x = img_x * scale_x
        pdf_y = img_y * scale_y
        
        return pdf_x, pdf_y
    
    def get_pdf_info(self, pdf_path):
        """Get basic information about the PDF"""
        try:
            pdf_document = fitz.open(pdf_path)
            info = {
                'page_count': len(pdf_document),
                'title': pdf_document.metadata.get('title', ''),
                'author': pdf_document.metadata.get('author', ''),
                'subject': pdf_document.metadata.get('subject', ''),
                'creator': pdf_document.metadata.get('creator', ''),
                'pages': []
            }
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                page_info = {
                    'page_num': page_num,
                    'width': page.rect.width,
                    'height': page.rect.height,
                    'rotation': page.rotation
                }
                info['pages'].append(page_info)
            
            pdf_document.close()
            return info
            
        except Exception as e:
            raise Exception(f"Error reading PDF info: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from PDF for analysis"""
        try:
            pdf_document = fitz.open(pdf_path)
            text_data = []
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Extract text with position information
                text_dict = page.get_text("dict")
                
                page_text = {
                    'page_num': page_num,
                    'blocks': []
                }
                
                for block in text_dict["blocks"]:
                    if "lines" in block:  # Text block
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text_info = {
                                    'text': span["text"],
                                    'bbox': span["bbox"],
                                    'font': span["font"],
                                    'size': span["size"]
                                }
                                page_text['blocks'].append(text_info)
                
                text_data.append(page_text)
            
            pdf_document.close()
            return text_data
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")