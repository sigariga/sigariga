#!/usr/bin/env python3
"""
Balloon Manager Module
Handles automatic balloon generation and placement for detected features
in technical drawings with intelligent positioning algorithms.
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import math
from shapely.geometry import Point, Polygon
from scipy.spatial.distance import cdist

class BalloonManager:
    def __init__(self):
        self.balloon_radius = 20
        self.leader_line_length = 50
        self.min_distance_between_balloons = 80
        self.margin_from_edges = 50
        self.preferred_positions = ['top-right', 'top-left', 'bottom-right', 'bottom-left']
        
    def create_balloons(self, detected_items):
        """Create balloons for all detected items with optimal placement"""
        balloons = []
        
        if not detected_items:
            return balloons
        
        # Sort items by priority and position
        prioritized_items = self._prioritize_items(detected_items)
        
        # Track occupied positions to avoid overlaps
        occupied_positions = []
        
        for i, item in enumerate(prioritized_items):
            balloon_number = i + 1
            
            # Calculate optimal balloon position
            balloon_position = self._calculate_optimal_position(
                item, occupied_positions, balloon_number
            )
            
            if balloon_position:
                balloon = self._create_balloon(item, balloon_position, balloon_number)
                balloons.append(balloon)
                occupied_positions.append(balloon_position)
        
        return balloons
    
    def _prioritize_items(self, items):
        """Prioritize items for balloon placement based on importance and position"""
        priority_weights = {
            'feature_control_frame': 10,
            'text_dimension': 8,
            'individual_symbol': 7,
            'dimension_line': 6,
            'arrow_dimension': 5,
            'datum_reference': 4,
            'tolerance_value': 3,
            'diameter_symbol': 7,
            'radius_symbol': 7
        }
        
        # Calculate priority scores
        scored_items = []
        for item in items:
            item_type = item.get('type', 'unknown')
            symbol_type = item.get('symbol_type', '')
            
            # Base priority from type
            priority = priority_weights.get(item_type, 1)
            
            # Boost priority for specific symbol types
            if symbol_type in ['position', 'perpendicularity', 'parallelism']:
                priority += 2
            
            # Consider position (top-left items get higher priority)
            bbox = item.get('bbox', [0, 0, 0, 0])
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            
            # Normalize position score (0-1, where top-left is higher)
            image_width = item.get('image_width', 1000)
            image_height = item.get('image_height', 1000)
            
            position_score = (1 - center_x / image_width) * 0.3 + (1 - center_y / image_height) * 0.2
            
            total_score = priority + position_score
            scored_items.append((total_score, item))
        
        # Sort by score (highest first)
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        return [item for score, item in scored_items]
    
    def _calculate_optimal_position(self, item, occupied_positions, balloon_number):
        """Calculate the optimal position for a balloon"""
        bbox = item.get('bbox', [0, 0, 100, 100])
        image_width = item.get('image_width', 1000)
        image_height = item.get('image_height', 1000)
        
        # Feature center point
        feature_center_x = (bbox[0] + bbox[2]) / 2
        feature_center_y = (bbox[1] + bbox[3]) / 2
        
        # Try different positions around the feature
        candidate_positions = self._generate_candidate_positions(
            feature_center_x, feature_center_y, bbox, image_width, image_height
        )
        
        # Evaluate each candidate position
        best_position = None
        best_score = -1
        
        for position in candidate_positions:
            score = self._evaluate_position(position, occupied_positions, 
                                          feature_center_x, feature_center_y,
                                          image_width, image_height)
            
            if score > best_score:
                best_score = score
                best_position = position
        
        return best_position
    
    def _generate_candidate_positions(self, center_x, center_y, bbox, image_width, image_height):
        """Generate candidate positions for balloon placement"""
        candidates = []
        
        # Define distances and angles for balloon placement
        distances = [self.leader_line_length, self.leader_line_length * 1.5, self.leader_line_length * 2]
        angles = [i * math.pi / 4 for i in range(8)]  # 8 directions around the feature
        
        for distance in distances:
            for angle in angles:
                balloon_x = center_x + distance * math.cos(angle)
                balloon_y = center_y + distance * math.sin(angle)
                
                # Check if position is within image bounds
                if (self.margin_from_edges <= balloon_x <= image_width - self.margin_from_edges and
                    self.margin_from_edges <= balloon_y <= image_height - self.margin_from_edges):
                    
                    # Calculate leader line end point (on feature boundary)
                    leader_end_x, leader_end_y = self._calculate_leader_end_point(
                        balloon_x, balloon_y, bbox
                    )
                    
                    position = {
                        'x': balloon_x,
                        'y': balloon_y,
                        'leader_end_x': leader_end_x,
                        'leader_end_y': leader_end_y,
                        'distance': distance,
                        'angle': angle
                    }
                    candidates.append(position)
        
        return candidates
    
    def _calculate_leader_end_point(self, balloon_x, balloon_y, bbox):
        """Calculate where the leader line should end on the feature"""
        x1, y1, x2, y2 = bbox
        feature_center_x = (x1 + x2) / 2
        feature_center_y = (y1 + y2) / 2
        
        # Calculate direction from balloon to feature center
        dx = feature_center_x - balloon_x
        dy = feature_center_y - balloon_y
        
        # Normalize direction
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
        
        # Find intersection with feature bounding box
        # Use feature edge closest to balloon
        if abs(dx) > abs(dy):
            # Horizontal edge
            if dx > 0:  # Right edge
                leader_end_x = x2
                leader_end_y = feature_center_y
            else:  # Left edge
                leader_end_x = x1
                leader_end_y = feature_center_y
        else:
            # Vertical edge
            if dy > 0:  # Bottom edge
                leader_end_x = feature_center_x
                leader_end_y = y2
            else:  # Top edge
                leader_end_x = feature_center_x
                leader_end_y = y1
        
        return leader_end_x, leader_end_y
    
    def _evaluate_position(self, position, occupied_positions, 
                          feature_center_x, feature_center_y,
                          image_width, image_height):
        """Evaluate the quality of a balloon position"""
        score = 100  # Base score
        
        balloon_x = position['x']
        balloon_y = position['y']
        
        # Check distance from other balloons
        for occupied in occupied_positions:
            distance = math.sqrt((balloon_x - occupied['x'])**2 + 
                               (balloon_y - occupied['y'])**2)
            
            if distance < self.min_distance_between_balloons:
                score -= 50  # Heavy penalty for being too close
            elif distance < self.min_distance_between_balloons * 1.5:
                score -= 20  # Medium penalty for being somewhat close
        
        # Prefer positions in top-right quadrant (conventional practice)
        if balloon_x > feature_center_x and balloon_y < feature_center_y:
            score += 20
        elif balloon_x > feature_center_x or balloon_y < feature_center_y:
            score += 10
        
        # Prefer shorter leader lines
        leader_length = math.sqrt((balloon_x - position['leader_end_x'])**2 + 
                                (balloon_y - position['leader_end_y'])**2)
        score -= leader_length * 0.1
        
        # Prefer positions not too close to image edges
        edge_distance = min(balloon_x - self.margin_from_edges,
                          image_width - balloon_x - self.margin_from_edges,
                          balloon_y - self.margin_from_edges,
                          image_height - balloon_y - self.margin_from_edges)
        
        if edge_distance < 20:
            score -= 30
        
        # Prefer positions that don't create crossing leader lines
        crossing_penalty = self._check_leader_line_crossings(position, occupied_positions)
        score -= crossing_penalty
        
        return score
    
    def _check_leader_line_crossings(self, position, occupied_positions):
        """Check if the leader line would cross with existing leader lines"""
        penalty = 0
        
        new_line = ((position['x'], position['y']), 
                   (position['leader_end_x'], position['leader_end_y']))
        
        for occupied in occupied_positions:
            if 'leader_end_x' in occupied and 'leader_end_y' in occupied:
                existing_line = ((occupied['x'], occupied['y']),
                               (occupied['leader_end_x'], occupied['leader_end_y']))
                
                if self._lines_intersect(new_line, existing_line):
                    penalty += 25  # Penalty for crossing lines
        
        return penalty
    
    def _lines_intersect(self, line1, line2):
        """Check if two line segments intersect"""
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if abs(denom) < 1e-10:
            return False  # Lines are parallel
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        return 0 <= t <= 1 and 0 <= u <= 1
    
    def _create_balloon(self, item, position, balloon_number):
        """Create a balloon object with all necessary information"""
        balloon = {
            'label': str(balloon_number),
            'x': position['x'],
            'y': position['y'],
            'radius': self.balloon_radius,
            'leader_end_x': position['leader_end_x'],
            'leader_end_y': position['leader_end_y'],
            'item_reference': item,
            'item_type': item.get('type'),
            'symbol_type': item.get('symbol_type'),
            'bbox': item.get('bbox'),
            'page': item.get('page', 0),
            'image_width': item.get('image_width'),
            'image_height': item.get('image_height')
        }
        
        # Add specific information based on item type
        if item.get('type') == 'text_dimension':
            balloon['dimension_value'] = item.get('value')
        elif item.get('type') == 'feature_control_frame':
            balloon['gdt_symbol'] = item.get('symbol_type')
            balloon['tolerance'] = item.get('tolerance')
        elif item.get('type') == 'datum_reference':
            balloon['datum_letter'] = item.get('datum_letter')
        
        return balloon
    
    def update_balloon_positions(self, balloons, new_constraints=None):
        """Update balloon positions based on new constraints or user modifications"""
        if not balloons:
            return balloons
        
        updated_balloons = []
        occupied_positions = []
        
        for balloon in balloons:
            # Check if current position is still valid
            if self._is_position_valid(balloon, occupied_positions, new_constraints):
                updated_balloons.append(balloon)
                occupied_positions.append(balloon)
            else:
                # Recalculate position
                item = balloon['item_reference']
                new_position = self._calculate_optimal_position(
                    item, occupied_positions, int(balloon['label'])
                )
                
                if new_position:
                    # Update balloon with new position
                    balloon['x'] = new_position['x']
                    balloon['y'] = new_position['y']
                    balloon['leader_end_x'] = new_position['leader_end_x']
                    balloon['leader_end_y'] = new_position['leader_end_y']
                    
                    updated_balloons.append(balloon)
                    occupied_positions.append(balloon)
        
        return updated_balloons
    
    def _is_position_valid(self, balloon, occupied_positions, constraints=None):
        """Check if a balloon position is still valid"""
        balloon_x = balloon['x']
        balloon_y = balloon['y']
        
        # Check distance from other balloons
        for occupied in occupied_positions:
            distance = math.sqrt((balloon_x - occupied['x'])**2 + 
                               (balloon_y - occupied['y'])**2)
            
            if distance < self.min_distance_between_balloons:
                return False
        
        # Check any new constraints
        if constraints:
            for constraint in constraints:
                if not self._satisfies_constraint(balloon, constraint):
                    return False
        
        return True
    
    def _satisfies_constraint(self, balloon, constraint):
        """Check if balloon satisfies a specific constraint"""
        # Implementation depends on constraint type
        # Could include minimum distances, forbidden areas, etc.
        return True
    
    def create_balloon_table(self, balloons):
        """Create a balloon table/legend for the drawing"""
        table_data = []
        
        for balloon in sorted(balloons, key=lambda b: int(b['label'])):
            row = {
                'balloon_number': balloon['label'],
                'item_type': balloon.get('item_type', 'Unknown'),
                'description': self._get_item_description(balloon),
                'value': self._get_item_value(balloon)
            }
            table_data.append(row)
        
        return table_data
    
    def _get_item_description(self, balloon):
        """Get a description for the ballooned item"""
        item_type = balloon.get('item_type')
        symbol_type = balloon.get('symbol_type')
        
        if item_type == 'text_dimension':
            return 'Dimension'
        elif item_type == 'feature_control_frame':
            return f'GD&T: {symbol_type or "Unknown"}'
        elif item_type == 'datum_reference':
            return f'Datum {balloon.get("datum_letter", "")}'
        elif symbol_type:
            return f'{symbol_type.title()} Symbol'
        else:
            return item_type.replace('_', ' ').title()
    
    def _get_item_value(self, balloon):
        """Get the value/measurement for the ballooned item"""
        if balloon.get('dimension_value'):
            return balloon['dimension_value']
        elif balloon.get('tolerance'):
            return balloon['tolerance']
        elif balloon.get('datum_letter'):
            return balloon['datum_letter']
        else:
            return 'See Drawing'
    
    def export_balloon_data(self, balloons, format='json'):
        """Export balloon data in various formats"""
        if format == 'json':
            import json
            return json.dumps(balloons, indent=2)
        elif format == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            table_data = self.create_balloon_table(balloons)
            
            if table_data:
                writer = csv.DictWriter(output, fieldnames=table_data[0].keys())
                writer.writeheader()
                writer.writerows(table_data)
            
            return output.getvalue()
        else:
            return str(balloons)