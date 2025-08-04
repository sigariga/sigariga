#!/usr/bin/env python3
"""
GD&T Detector Module
Detects and classifies Geometric Dimensioning and Tolerancing symbols
in technical drawings using computer vision and pattern recognition.
"""

import cv2
import numpy as np
import re
from PIL import Image, ImageDraw
import pytesseract
from scipy import ndimage
from skimage import feature, morphology, measure
import math

class GDTDetector:
    def __init__(self):
        # GD&T symbol definitions
        self.gdt_symbols = {
            'straightness': '⏤',
            'flatness': '⏥',
            'circularity': '○',
            'cylindricity': '⌭',
            'profile_line': '⌒',
            'profile_surface': '⌓',
            'angularity': '∠',
            'perpendicularity': '⊥',
            'parallelism': '∥',
            'position': '⊕',
            'concentricity': '◎',
            'symmetry': '⌖',
            'runout_circular': '↗',
            'runout_total': '↗↗'
        }
        
        # Feature control frame patterns
        self.fcf_patterns = [
            r'([⏤⏥○⌭⌒⌓∠⊥∥⊕◎⌖↗])\s*([Ⓜ]?)\s*(\d+\.?\d*)\s*([ⒶⒷⒸ]?)',
            r'\|([⏤⏥○⌭⌒⌓∠⊥∥⊕◎⌖↗])\|([Ⓜ]?)\|(\d+\.?\d*)\|([ⒶⒷⒸ]?)\|',
        ]
        
        # Material condition modifiers
        self.material_conditions = {
            'Ⓜ': 'MMC',  # Maximum Material Condition
            'Ⓛ': 'LMC',  # Least Material Condition
            'Ⓢ': 'RFS'   # Regardless of Feature Size
        }
        
        # Datum reference modifiers
        self.datum_references = {
            'Ⓐ': 'A',
            'Ⓑ': 'B', 
            'Ⓒ': 'C',
            'Ⓓ': 'D',
            'Ⓔ': 'E',
            'Ⓕ': 'F'
        }
        
        # Create symbol templates
        self.symbol_templates = self._create_symbol_templates()
        
    def detect_gdt_symbols(self, image_data):
        """Main function to detect GD&T symbols in an image"""
        image = image_data['cv_image']
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        detected_symbols = []
        
        # Detect different types of GD&T features
        fcf_symbols = self._detect_feature_control_frames(gray, image_data)
        symbol_matches = self._detect_individual_symbols(gray, image_data)
        datum_symbols = self._detect_datum_references(gray, image_data)
        tolerance_symbols = self._detect_tolerance_values(gray, image_data)
        
        # Combine all detected symbols
        detected_symbols.extend(fcf_symbols)
        detected_symbols.extend(symbol_matches)
        detected_symbols.extend(datum_symbols)
        detected_symbols.extend(tolerance_symbols)
        
        # Group related symbols and filter
        grouped_symbols = self._group_and_filter_symbols(detected_symbols, image_data)
        
        return grouped_symbols
    
    def _detect_feature_control_frames(self, gray_image, image_data):
        """Detect feature control frames (rectangular boxes with GD&T symbols)"""
        symbols = []
        
        # Find rectangular contours that could be feature control frames
        binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Check if contour is rectangular and appropriate size
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            
            # Feature control frames are typically rectangular with specific aspect ratio
            aspect_ratio = w / h if h > 0 else 0
            area = cv2.contourArea(contour)
            
            if (2 < aspect_ratio < 8 and 500 < area < 5000 and 
                w > 50 and h > 15 and h < 50):
                
                # Extract the region inside the frame
                roi = gray_image[y:y+h, x:x+w]
                
                # Analyze the content of the frame
                frame_content = self._analyze_frame_content(roi)
                
                if frame_content:
                    symbol = {
                        'type': 'feature_control_frame',
                        'bbox': [x, y, x + w, y + h],
                        'content': frame_content,
                        'symbol_type': frame_content.get('geometric_symbol'),
                        'tolerance': frame_content.get('tolerance_value'),
                        'material_condition': frame_content.get('material_condition'),
                        'datum_references': frame_content.get('datum_references', []),
                        'image_width': image_data['width'],
                        'image_height': image_data['height']
                    }
                    symbols.append(symbol)
        
        return symbols
    
    def _analyze_frame_content(self, roi):
        """Analyze the content of a feature control frame"""
        try:
            # Use OCR to extract text from the frame
            text = pytesseract.image_to_string(roi, config='--psm 7')
            
            # Look for GD&T patterns in the text
            for pattern in self.fcf_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    match = matches[0]
                    
                    content = {
                        'geometric_symbol': self._identify_geometric_symbol(match[0]),
                        'material_condition': self.material_conditions.get(match[1], None),
                        'tolerance_value': match[2],
                        'datum_references': self._parse_datum_references(match[3:])
                    }
                    return content
                    
            # If no pattern match, try template matching for symbols
            symbol_found = self._match_symbols_in_roi(roi)
            if symbol_found:
                return symbol_found
                
        except Exception as e:
            print(f"Frame analysis error: {e}")
        
        return None
    
    def _detect_individual_symbols(self, gray_image, image_data):
        """Detect individual GD&T symbols using template matching"""
        symbols = []
        
        for symbol_name, template in self.symbol_templates.items():
            if template is not None:
                # Perform template matching
                result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.7
                locations = np.where(result >= threshold)
                
                for pt in zip(*locations[::-1]):
                    x, y = pt
                    h, w = template.shape
                    
                    # Look for associated tolerance values nearby
                    tolerance_info = self._find_nearby_tolerance(gray_image, x + w, y, y + h)
                    
                    symbol = {
                        'type': 'individual_symbol',
                        'symbol_type': symbol_name,
                        'position': [x, y],
                        'bbox': [x, y, x + w, y + h],
                        'tolerance': tolerance_info.get('value') if tolerance_info else None,
                        'material_condition': tolerance_info.get('material_condition') if tolerance_info else None,
                        'image_width': image_data['width'],
                        'image_height': image_data['height']
                    }
                    symbols.append(symbol)
        
        return symbols
    
    def _detect_datum_references(self, gray_image, image_data):
        """Detect datum reference symbols (circled letters)"""
        symbols = []
        
        # Find circles that could contain datum letters
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20,
                                  param1=50, param2=30, minRadius=8, maxRadius=25)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            for circle in circles[0, :]:
                x, y, r = circle
                
                # Extract the area inside the circle
                mask = np.zeros(gray_image.shape, dtype=np.uint8)
                cv2.circle(mask, (x, y), r, 255, -1)
                
                roi = cv2.bitwise_and(gray_image, mask)
                roi_crop = roi[y-r:y+r, x-r:x+r]
                
                if roi_crop.size > 0:
                    # Try to read the letter inside
                    try:
                        text = pytesseract.image_to_string(roi_crop, 
                                                         config='--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                        text = text.strip()
                        
                        if len(text) == 1 and text.isalpha():
                            symbol = {
                                'type': 'datum_reference',
                                'datum_letter': text,
                                'position': [x, y],
                                'radius': r,
                                'bbox': [x - r, y - r, x + r, y + r],
                                'image_width': image_data['width'],
                                'image_height': image_data['height']
                            }
                            symbols.append(symbol)
                            
                    except Exception as e:
                        print(f"Datum OCR error: {e}")
        
        return symbols
    
    def _detect_tolerance_values(self, gray_image, image_data):
        """Detect standalone tolerance values"""
        symbols = []
        
        try:
            # Use OCR to find all text
            ocr_data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)
            
            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip()
                confidence = ocr_data['conf'][i]
                
                if confidence > 40 and text:
                    # Check for tolerance patterns
                    tolerance_patterns = [
                        r'±\s*(\d+\.?\d*)',  # Plus/minus tolerance
                        r'\+(\d+\.?\d*)\s*-(\d+\.?\d*)',  # Plus/minus tolerance
                        r'(\d+\.?\d*)\s*±\s*(\d+\.?\d*)',  # Value with tolerance
                        r'[ⓂⒶⒷⒸ]'  # Material condition or datum modifiers
                    ]
                    
                    for pattern in tolerance_patterns:
                        if re.search(pattern, text):
                            x = ocr_data['left'][i]
                            y = ocr_data['top'][i]
                            w = ocr_data['width'][i]
                            h = ocr_data['height'][i]
                            
                            symbol = {
                                'type': 'tolerance_value',
                                'value': text,
                                'bbox': [x, y, x + w, y + h],
                                'confidence': confidence,
                                'image_width': image_data['width'],
                                'image_height': image_data['height']
                            }
                            symbols.append(symbol)
                            break
                            
        except Exception as e:
            print(f"Tolerance detection error: {e}")
        
        return symbols
    
    def _create_symbol_templates(self):
        """Create templates for GD&T symbols"""
        templates = {}
        
        # Straightness symbol
        template = np.zeros((20, 30), dtype=np.uint8)
        cv2.line(template, (5, 10), (25, 10), 255, 2)
        templates['straightness'] = template
        
        # Flatness symbol
        template = np.zeros((20, 30), dtype=np.uint8)
        cv2.line(template, (5, 8), (25, 8), 255, 2)
        cv2.line(template, (5, 12), (25, 12), 255, 2)
        templates['flatness'] = template
        
        # Circularity symbol (circle)
        template = np.zeros((20, 20), dtype=np.uint8)
        cv2.circle(template, (10, 10), 8, 255, 2)
        templates['circularity'] = template
        
        # Position symbol (circle with cross)
        template = np.zeros((20, 20), dtype=np.uint8)
        cv2.circle(template, (10, 10), 8, 255, 2)
        cv2.line(template, (10, 2), (10, 18), 255, 2)
        cv2.line(template, (2, 10), (18, 10), 255, 2)
        templates['position'] = template
        
        # Perpendicularity symbol
        template = np.zeros((20, 20), dtype=np.uint8)
        cv2.line(template, (10, 2), (10, 18), 255, 2)
        cv2.line(template, (5, 16), (15, 16), 255, 2)
        templates['perpendicularity'] = template
        
        # Parallelism symbol
        template = np.zeros((20, 25), dtype=np.uint8)
        cv2.line(template, (8, 2), (8, 18), 255, 2)
        cv2.line(template, (12, 2), (12, 18), 255, 2)
        templates['parallelism'] = template
        
        # Angularity symbol
        template = np.zeros((20, 25), dtype=np.uint8)
        cv2.line(template, (5, 15), (10, 5), 255, 2)
        cv2.line(template, (10, 5), (15, 15), 255, 2)
        templates['angularity'] = template
        
        return templates
    
    def _identify_geometric_symbol(self, symbol_char):
        """Identify the type of geometric symbol"""
        symbol_map = {v: k for k, v in self.gdt_symbols.items()}
        return symbol_map.get(symbol_char, 'unknown')
    
    def _parse_datum_references(self, datum_matches):
        """Parse datum reference letters from matches"""
        datums = []
        for match in datum_matches:
            if match and match in self.datum_references:
                datums.append(self.datum_references[match])
        return datums
    
    def _find_nearby_tolerance(self, image, start_x, start_y, end_y):
        """Find tolerance values near a symbol"""
        search_width = 100
        roi = image[start_y:end_y, start_x:min(image.shape[1], start_x + search_width)]
        
        try:
            text = pytesseract.image_to_string(roi, config='--psm 8')
            
            # Look for numerical values
            numbers = re.findall(r'\d+\.?\d*', text)
            material_conditions = re.findall(r'[ⓂⓁⓈ]', text)
            
            if numbers:
                result = {'value': numbers[0]}
                if material_conditions:
                    result['material_condition'] = self.material_conditions.get(
                        material_conditions[0], 'unknown')
                return result
                
        except Exception:
            pass
        
        return None
    
    def _match_symbols_in_roi(self, roi):
        """Match GD&T symbols within a ROI using template matching"""
        best_match = None
        best_score = 0
        
        for symbol_name, template in self.symbol_templates.items():
            if template is not None and template.shape[0] <= roi.shape[0] and template.shape[1] <= roi.shape[1]:
                result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                
                if max_val > best_score and max_val > 0.6:
                    best_score = max_val
                    best_match = {
                        'geometric_symbol': symbol_name,
                        'confidence': max_val
                    }
        
        return best_match
    
    def _group_and_filter_symbols(self, symbols, image_data):
        """Group related symbols and filter out false positives"""
        grouped_symbols = []
        
        # Sort symbols by type and position
        fcf_symbols = [s for s in symbols if s['type'] == 'feature_control_frame']
        individual_symbols = [s for s in symbols if s['type'] == 'individual_symbol']
        datum_symbols = [s for s in symbols if s['type'] == 'datum_reference']
        tolerance_symbols = [s for s in symbols if s['type'] == 'tolerance_value']
        
        # Process feature control frames first (highest priority)
        for fcf in fcf_symbols:
            # Check for conflicts with individual symbols
            fcf_bbox = fcf['bbox']
            conflicting_symbols = []
            
            for symbol in individual_symbols:
                if self._symbols_overlap(fcf_bbox, symbol['bbox']):
                    conflicting_symbols.append(symbol)
            
            # Remove conflicting individual symbols
            for conflict in conflicting_symbols:
                if conflict in individual_symbols:
                    individual_symbols.remove(conflict)
            
            grouped_symbols.append(fcf)
        
        # Add remaining individual symbols
        for symbol in individual_symbols:
            # Check for duplicates
            is_duplicate = False
            for existing in grouped_symbols:
                if (existing.get('symbol_type') == symbol.get('symbol_type') and
                    self._symbols_overlap(existing['bbox'], symbol['bbox'])):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                grouped_symbols.append(symbol)
        
        # Add datum references
        grouped_symbols.extend(datum_symbols)
        
        # Add standalone tolerance values
        for tolerance in tolerance_symbols:
            # Only add if not already associated with a symbol
            is_associated = False
            for symbol in grouped_symbols:
                if self._symbols_nearby(symbol['bbox'], tolerance['bbox']):
                    is_associated = True
                    break
            
            if not is_associated:
                grouped_symbols.append(tolerance)
        
        return grouped_symbols
    
    def _symbols_overlap(self, bbox1, bbox2, threshold=0.3):
        """Check if two symbol bounding boxes overlap"""
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
    
    def _symbols_nearby(self, bbox1, bbox2, max_distance=50):
        """Check if two symbols are nearby (for association)"""
        center1_x = (bbox1[0] + bbox1[2]) / 2
        center1_y = (bbox1[1] + bbox1[3]) / 2
        center2_x = (bbox2[0] + bbox2[2]) / 2
        center2_y = (bbox2[1] + bbox2[3]) / 2
        
        distance = np.sqrt((center1_x - center2_x)**2 + (center1_y - center2_y)**2)
        return distance <= max_distance