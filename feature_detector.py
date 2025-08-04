#!/usr/bin/env python3
"""
Feature Detector Module
Detects dimensional features, measurements, and tolerances in technical drawings
using computer vision and pattern recognition techniques.
"""

import cv2
import numpy as np
import re
from PIL import Image, ImageDraw
import pytesseract
from scipy import ndimage
from skimage import feature, morphology, measure
import math

class FeatureDetector:
    def __init__(self):
        # Configuration for different types of features
        self.dimension_patterns = [
            r'(\d+\.?\d*)\s*(?:mm|in|inch|")',  # Basic dimensions with units
            r'Ø\s*(\d+\.?\d*)',  # Diameter symbols
            r'R\s*(\d+\.?\d*)',  # Radius
            r'(\d+\.?\d*)\s*±\s*(\d+\.?\d*)',  # Tolerances
            r'(\d+\.?\d*)\s*\+(\d+\.?\d*)\s*-(\d+\.?\d*)',  # Plus/minus tolerances
        ]
        
        # Template for common dimension symbols
        self.symbol_templates = self._load_symbol_templates()
        
    def detect_dimensions(self, image_data):
        """Main function to detect dimensional features in an image"""
        image = image_data['cv_image']
        pil_image = image_data['pil_image']
        
        detected_features = []
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect different types of dimensional features
        text_dimensions = self._detect_text_dimensions(gray, image_data)
        line_dimensions = self._detect_dimension_lines(gray, image_data)
        arrow_dimensions = self._detect_arrow_dimensions(gray, image_data)
        symbol_dimensions = self._detect_dimension_symbols(gray, image_data)
        
        # Combine all detected features
        detected_features.extend(text_dimensions)
        detected_features.extend(line_dimensions)
        detected_features.extend(arrow_dimensions)
        detected_features.extend(symbol_dimensions)
        
        # Filter and refine detections
        filtered_features = self._filter_and_refine(detected_features, image_data)
        
        return filtered_features
    
    def _detect_text_dimensions(self, gray_image, image_data):
        """Detect dimensional text using OCR"""
        features = []
        
        try:
            # Use OCR to extract text with bounding boxes
            ocr_data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)
            
            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip()
                confidence = ocr_data['conf'][i]
                
                if confidence > 30 and text:  # Filter low confidence results
                    # Check if text matches dimension patterns
                    for pattern in self.dimension_patterns:
                        matches = re.findall(pattern, text)
                        if matches:
                            x = ocr_data['left'][i]
                            y = ocr_data['top'][i]
                            w = ocr_data['width'][i]
                            h = ocr_data['height'][i]
                            
                            feature = {
                                'type': 'text_dimension',
                                'value': text,
                                'bbox': [x, y, x + w, y + h],
                                'confidence': confidence,
                                'pattern_match': matches[0] if isinstance(matches[0], str) else matches[0][0],
                                'image_width': image_data['width'],
                                'image_height': image_data['height']
                            }
                            features.append(feature)
                            
        except Exception as e:
            print(f"OCR error: {e}")
        
        return features
    
    def _detect_dimension_lines(self, gray_image, image_data):
        """Detect dimension lines and extension lines"""
        features = []
        
        # Apply edge detection
        edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                               minLineLength=50, maxLineGap=10)
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # Calculate line properties
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                
                # Check if this could be a dimension line
                if self._is_dimension_line(gray_image, x1, y1, x2, y2, angle):
                    feature = {
                        'type': 'dimension_line',
                        'start_point': [x1, y1],
                        'end_point': [x2, y2],
                        'length': length,
                        'angle': angle,
                        'bbox': [min(x1, x2) - 5, min(y1, y2) - 5, 
                               max(x1, x2) + 5, max(y1, y2) + 5],
                        'image_width': image_data['width'],
                        'image_height': image_data['height']
                    }
                    features.append(feature)
        
        return features
    
    def _detect_arrow_dimensions(self, gray_image, image_data):
        """Detect dimension arrows and arrowheads"""
        features = []
        
        # Look for arrowhead patterns
        arrowhead_kernel = np.array([
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0]
        ], dtype=np.uint8)
        
        # Apply morphological operations to find arrowheads
        binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        arrow_matches = cv2.matchTemplate(binary, arrowhead_kernel * 255, cv2.TM_CCOEFF_NORMED)
        
        # Find arrow locations
        threshold = 0.7
        locations = np.where(arrow_matches >= threshold)
        
        for pt in zip(*locations[::-1]):
            x, y = pt
            
            # Look for associated dimension line
            dimension_info = self._find_associated_dimension_line(gray_image, x, y)
            
            if dimension_info:
                feature = {
                    'type': 'arrow_dimension',
                    'arrow_position': [x, y],
                    'dimension_info': dimension_info,
                    'bbox': [x - 10, y - 10, x + 20, y + 20],
                    'image_width': image_data['width'],
                    'image_height': image_data['height']
                }
                features.append(feature)
        
        return features
    
    def _detect_dimension_symbols(self, gray_image, image_data):
        """Detect common dimension symbols (diameter, radius, etc.)"""
        features = []
        
        # Define symbol templates
        symbols = {
            'diameter': self._create_diameter_template(),
            'radius': self._create_radius_template(),
            'depth': self._create_depth_template(),
            'counterbore': self._create_counterbore_template()
        }
        
        for symbol_name, template in symbols.items():
            if template is not None:
                # Template matching
                result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                locations = np.where(result >= threshold)
                
                for pt in zip(*locations[::-1]):
                    x, y = pt
                    h, w = template.shape
                    
                    # Look for associated numerical value
                    value = self._find_associated_number(gray_image, x + w, y, y + h)
                    
                    feature = {
                        'type': f'{symbol_name}_symbol',
                        'symbol_name': symbol_name,
                        'position': [x, y],
                        'value': value,
                        'bbox': [x, y, x + w, y + h],
                        'image_width': image_data['width'],
                        'image_height': image_data['height']
                    }
                    features.append(feature)
        
        return features
    
    def _is_dimension_line(self, image, x1, y1, x2, y2, angle):
        """Check if a line could be a dimension line based on context"""
        # Horizontal or vertical lines are more likely to be dimension lines
        if abs(angle) < 10 or abs(angle - 90) < 10 or abs(angle + 90) < 10 or abs(angle - 180) < 10:
            # Check for nearby text or arrows
            line_center_x = (x1 + x2) // 2
            line_center_y = (y1 + y2) // 2
            
            # Look for text near the line
            search_radius = 30
            roi = image[max(0, line_center_y - search_radius):min(image.shape[0], line_center_y + search_radius),
                       max(0, line_center_x - search_radius):min(image.shape[1], line_center_x + search_radius)]
            
            # Check if there's text content in the ROI
            text_density = np.sum(roi < 200) / (roi.shape[0] * roi.shape[1])
            
            return text_density > 0.1  # Threshold for text presence
        
        return False
    
    def _find_associated_dimension_line(self, image, arrow_x, arrow_y):
        """Find dimension line associated with an arrow"""
        # Search in a radius around the arrow for lines
        search_radius = 50
        roi = image[max(0, arrow_y - search_radius):min(image.shape[0], arrow_y + search_radius),
                   max(0, arrow_x - search_radius):min(image.shape[1], arrow_x + search_radius)]
        
        # Apply edge detection to find lines
        edges = cv2.Canny(roi, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=20, maxLineGap=5)
        
        if lines is not None and len(lines) > 0:
            # Return the longest line found
            longest_line = max(lines, key=lambda l: np.sqrt((l[0][2] - l[0][0])**2 + (l[0][3] - l[0][1])**2))
            return {
                'line': longest_line[0],
                'length': np.sqrt((longest_line[0][2] - longest_line[0][0])**2 + 
                                (longest_line[0][3] - longest_line[0][1])**2)
            }
        
        return None
    
    def _find_associated_number(self, image, x, y, max_y):
        """Find numerical value associated with a symbol"""
        # Search to the right of the symbol for numbers
        search_width = 100
        roi = image[y:max_y, x:min(image.shape[1], x + search_width)]
        
        try:
            text = pytesseract.image_to_string(roi, config='--psm 8 -c tessedit_char_whitelist=0123456789.')
            # Extract first number found
            numbers = re.findall(r'\d+\.?\d*', text)
            return numbers[0] if numbers else None
        except:
            return None
    
    def _create_diameter_template(self):
        """Create template for diameter symbol (Ø)"""
        template = np.zeros((20, 20), dtype=np.uint8)
        cv2.circle(template, (10, 10), 8, 255, 2)
        cv2.line(template, (3, 3), (17, 17), 255, 2)
        return template
    
    def _create_radius_template(self):
        """Create template for radius symbol (R)"""
        template = np.zeros((20, 15), dtype=np.uint8)
        # Draw R shape
        cv2.line(template, (2, 2), (2, 18), 255, 2)  # Vertical line
        cv2.line(template, (2, 2), (10, 2), 255, 2)  # Top horizontal
        cv2.line(template, (10, 2), (10, 10), 255, 2)  # Right vertical
        cv2.line(template, (2, 10), (10, 10), 255, 2)  # Middle horizontal
        cv2.line(template, (6, 10), (13, 18), 255, 2)  # Diagonal
        return template
    
    def _create_depth_template(self):
        """Create template for depth symbol"""
        template = np.zeros((15, 15), dtype=np.uint8)
        # Draw depth symbol (square with diagonal)
        cv2.rectangle(template, (2, 2), (13, 13), 255, 2)
        cv2.line(template, (5, 5), (10, 10), 255, 2)
        return template
    
    def _create_counterbore_template(self):
        """Create template for counterbore symbol"""
        template = np.zeros((20, 20), dtype=np.uint8)
        # Draw counterbore symbol (circle with cross)
        cv2.circle(template, (10, 10), 8, 255, 2)
        cv2.line(template, (10, 2), (10, 18), 255, 2)
        cv2.line(template, (2, 10), (18, 10), 255, 2)
        return template
    
    def _load_symbol_templates(self):
        """Load pre-defined symbol templates"""
        return {
            'diameter': self._create_diameter_template(),
            'radius': self._create_radius_template(),
            'depth': self._create_depth_template(),
            'counterbore': self._create_counterbore_template()
        }
    
    def _filter_and_refine(self, features, image_data):
        """Filter out false positives and refine detection results"""
        refined_features = []
        
        # Group similar features and remove duplicates
        for feature in features:
            # Skip very small features
            bbox = feature['bbox']
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            
            if width < 10 or height < 10:
                continue
            
            # Check for overlapping features and keep the best one
            is_duplicate = False
            for existing in refined_features:
                if self._features_overlap(feature['bbox'], existing['bbox']):
                    # Keep the one with higher confidence
                    if feature.get('confidence', 100) > existing.get('confidence', 100):
                        refined_features.remove(existing)
                    else:
                        is_duplicate = True
                    break
            
            if not is_duplicate:
                refined_features.append(feature)
        
        return refined_features
    
    def _features_overlap(self, bbox1, bbox2, threshold=0.5):
        """Check if two bounding boxes overlap significantly"""
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2
        
        # Calculate intersection
        x_min = max(x1_min, x2_min)
        y_min = max(y1_min, y2_min)
        x_max = min(x1_max, x2_max)
        y_max = min(y1_max, y2_max)
        
        if x_max <= x_min or y_max <= y_min:
            return False
        
        intersection_area = (x_max - x_min) * (y_max - y_min)
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        
        overlap_ratio = intersection_area / min(area1, area2)
        return overlap_ratio > threshold