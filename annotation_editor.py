#!/usr/bin/env python3
"""
Annotation Editor Module
Provides interface for viewing, editing, and managing annotations
and balloons in technical drawings.
"""

import tkinter as tk
from tkinter import ttk, Canvas, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math

class AnnotationEditor:
    def __init__(self):
        self.canvas = None
        self.image_data = None
        self.features = []
        self.balloons = []
        self.annotations = []
        
        # Display settings
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Selection and editing
        self.selected_balloon = None
        self.selected_feature = None
        self.edit_mode = 'view'  # 'view', 'move', 'edit'
        
        # Colors for different elements
        self.colors = {
            'feature_highlight': '#0080FF',
            'gdt_highlight': '#00FF80',
            'balloon_circle': '#FF0000',
            'balloon_text': '#FFFFFF',
            'leader_line': '#FF0000',
            'selection': '#FFFF00'
        }
        
    def set_canvas(self, canvas):
        """Set the canvas for drawing"""
        self.canvas = canvas
        self.setup_canvas_bindings()
        
    def setup_canvas_bindings(self):
        """Setup mouse and keyboard bindings for the canvas"""
        if self.canvas:
            self.canvas.bind("<Button-1>", self.on_canvas_click)
            self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
            self.canvas.bind("<Button-3>", self.on_right_click)
            self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
            self.canvas.bind("<KeyPress>", self.on_key_press)
            self.canvas.focus_set()
    
    def load_image_data(self, image_data):
        """Load image data for annotation"""
        self.image_data = image_data
        self.display_image()
    
    def set_features(self, features):
        """Set detected features"""
        self.features = features
        self.refresh_display()
    
    def set_balloons(self, balloons):
        """Set balloon annotations"""
        self.balloons = balloons
        self.refresh_display()
    
    def display_image(self):
        """Display the base image on canvas"""
        if not self.canvas or not self.image_data:
            return
            
        try:
            # Get PIL image
            pil_image = self.image_data['pil_image']
            
            # Apply zoom and pan
            display_width = int(pil_image.width * self.zoom_factor)
            display_height = int(pil_image.height * self.zoom_factor)
            
            # Resize image if zoomed
            if self.zoom_factor != 1.0:
                pil_image = pil_image.resize((display_width, display_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            self.photo_image = ImageTk.PhotoImage(pil_image)
            
            # Clear canvas and display image
            self.canvas.delete("all")
            self.canvas.create_image(self.pan_x, self.pan_y, anchor=tk.NW, image=self.photo_image, tags="base_image")
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def refresh_display(self):
        """Refresh the entire display with current annotations"""
        if not self.canvas:
            return
            
        # Redraw base image
        self.display_image()
        
        # Draw features
        self.draw_features()
        
        # Draw balloons
        self.draw_balloons()
        
        # Draw selection indicators
        self.draw_selection_indicators()
    
    def draw_features(self):
        """Draw feature highlights on the canvas"""
        if not self.features:
            return
            
        for i, feature in enumerate(self.features):
            bbox = feature.get('bbox', [0, 0, 0, 0])
            feature_type = feature.get('type', 'unknown')
            
            # Apply zoom and pan transformations
            x1 = int(bbox[0] * self.zoom_factor + self.pan_x)
            y1 = int(bbox[1] * self.zoom_factor + self.pan_y)
            x2 = int(bbox[2] * self.zoom_factor + self.pan_x)
            y2 = int(bbox[3] * self.zoom_factor + self.pan_y)
            
            # Choose color based on feature type
            if 'gdt' in feature_type.lower() or feature_type == 'feature_control_frame':
                color = self.colors['gdt_highlight']
            else:
                color = self.colors['feature_highlight']
            
            # Draw feature rectangle
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                       outline=color, width=2, fill="", 
                                       tags=f"feature_{i}")
            
            # Add feature label
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            label = feature.get('value', feature.get('symbol_type', f'F{i+1}'))
            
            self.canvas.create_text(center_x, center_y - 15, text=label, 
                                  fill=color, font=("Arial", 8), 
                                  tags=f"feature_label_{i}")
    
    def draw_balloons(self):
        """Draw balloon annotations on the canvas"""
        if not self.balloons:
            return
            
        for i, balloon in enumerate(self.balloons):
            # Apply zoom and pan transformations
            x = int(balloon['x'] * self.zoom_factor + self.pan_x)
            y = int(balloon['y'] * self.zoom_factor + self.pan_y)
            radius = int(balloon['radius'] * self.zoom_factor)
            
            # Draw balloon circle
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                  outline=self.colors['balloon_circle'], 
                                  fill=self.colors['balloon_circle'],
                                  width=2, tags=f"balloon_{i}")
            
            # Draw balloon number
            self.canvas.create_text(x, y, text=balloon['label'],
                                  fill=self.colors['balloon_text'],
                                  font=("Arial", int(12 * self.zoom_factor), "bold"),
                                  tags=f"balloon_text_{i}")
            
            # Draw leader line if present
            if 'leader_end_x' in balloon and 'leader_end_y' in balloon:
                end_x = int(balloon['leader_end_x'] * self.zoom_factor + self.pan_x)
                end_y = int(balloon['leader_end_y'] * self.zoom_factor + self.pan_y)
                
                self.canvas.create_line(x, y, end_x, end_y,
                                      fill=self.colors['leader_line'],
                                      width=int(2 * self.zoom_factor),
                                      tags=f"leader_{i}")
    
    def draw_selection_indicators(self):
        """Draw selection indicators for selected items"""
        if self.selected_balloon is not None:
            balloon = self.balloons[self.selected_balloon]
            x = int(balloon['x'] * self.zoom_factor + self.pan_x)
            y = int(balloon['y'] * self.zoom_factor + self.pan_y)
            radius = int(balloon['radius'] * self.zoom_factor)
            
            # Draw selection circle
            self.canvas.create_oval(x - radius - 5, y - radius - 5, 
                                  x + radius + 5, y + radius + 5,
                                  outline=self.colors['selection'], 
                                  width=3, fill="", tags="selection")
        
        if self.selected_feature is not None:
            feature = self.features[self.selected_feature]
            bbox = feature.get('bbox', [0, 0, 0, 0])
            
            x1 = int(bbox[0] * self.zoom_factor + self.pan_x)
            y1 = int(bbox[1] * self.zoom_factor + self.pan_y)
            x2 = int(bbox[2] * self.zoom_factor + self.pan_x)
            y2 = int(bbox[3] * self.zoom_factor + self.pan_y)
            
            # Draw selection rectangle
            self.canvas.create_rectangle(x1 - 3, y1 - 3, x2 + 3, y2 + 3,
                                       outline=self.colors['selection'],
                                       width=3, fill="", tags="selection")
    
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        # Convert screen coordinates to image coordinates
        img_x = (event.x - self.pan_x) / self.zoom_factor
        img_y = (event.y - self.pan_y) / self.zoom_factor
        
        # Check if clicking on a balloon
        balloon_clicked = self.find_balloon_at_position(img_x, img_y)
        if balloon_clicked is not None:
            self.selected_balloon = balloon_clicked
            self.selected_feature = None
            self.refresh_display()
            return
        
        # Check if clicking on a feature
        feature_clicked = self.find_feature_at_position(img_x, img_y)
        if feature_clicked is not None:
            self.selected_feature = feature_clicked
            self.selected_balloon = None
            self.refresh_display()
            return
        
        # Clear selection if clicking on empty space
        self.selected_balloon = None
        self.selected_feature = None
        self.refresh_display()
    
    def on_canvas_drag(self, event):
        """Handle canvas drag events for moving balloons"""
        if self.selected_balloon is not None and self.edit_mode == 'move':
            # Convert screen coordinates to image coordinates
            img_x = (event.x - self.pan_x) / self.zoom_factor
            img_y = (event.y - self.pan_y) / self.zoom_factor
            
            # Update balloon position
            self.balloons[self.selected_balloon]['x'] = img_x
            self.balloons[self.selected_balloon]['y'] = img_y
            
            # Refresh display
            self.refresh_display()
        elif self.edit_mode == 'view':
            # Pan the view
            self.pan_x += event.x - getattr(self, 'last_x', event.x)
            self.pan_y += event.y - getattr(self, 'last_y', event.y)
            self.last_x = event.x
            self.last_y = event.y
            self.refresh_display()
    
    def on_canvas_release(self, event):
        """Handle canvas release events"""
        if hasattr(self, 'last_x'):
            delattr(self, 'last_x')
        if hasattr(self, 'last_y'):
            delattr(self, 'last_y')
    
    def on_right_click(self, event):
        """Handle right-click context menu"""
        # Convert screen coordinates to image coordinates
        img_x = (event.x - self.pan_x) / self.zoom_factor
        img_y = (event.y - self.pan_y) / self.zoom_factor
        
        # Show context menu
        self.show_context_menu(event, img_x, img_y)
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        # Zoom in/out
        if event.delta > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor *= 0.9
        
        # Limit zoom range
        self.zoom_factor = max(0.1, min(5.0, self.zoom_factor))
        
        self.refresh_display()
    
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.keysym == 'Delete' and self.selected_balloon is not None:
            self.delete_balloon(self.selected_balloon)
        elif event.keysym == 'Escape':
            self.selected_balloon = None
            self.selected_feature = None
            self.refresh_display()
    
    def find_balloon_at_position(self, x, y):
        """Find balloon at the given position"""
        for i, balloon in enumerate(self.balloons):
            balloon_x = balloon['x']
            balloon_y = balloon['y']
            radius = balloon['radius']
            
            distance = math.sqrt((x - balloon_x)**2 + (y - balloon_y)**2)
            if distance <= radius:
                return i
        return None
    
    def find_feature_at_position(self, x, y):
        """Find feature at the given position"""
        for i, feature in enumerate(self.features):
            bbox = feature.get('bbox', [0, 0, 0, 0])
            
            if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]:
                return i
        return None
    
    def show_context_menu(self, event, img_x, img_y):
        """Show context menu at cursor position"""
        context_menu = tk.Menu(self.canvas, tearoff=0)
        
        balloon_at_pos = self.find_balloon_at_position(img_x, img_y)
        feature_at_pos = self.find_feature_at_position(img_x, img_y)
        
        if balloon_at_pos is not None:
            # Balloon context menu
            context_menu.add_command(label="Edit Balloon", 
                                   command=lambda: self.edit_balloon(balloon_at_pos))
            context_menu.add_command(label="Delete Balloon", 
                                   command=lambda: self.delete_balloon(balloon_at_pos))
            context_menu.add_separator()
            context_menu.add_command(label="Move Balloon", 
                                   command=lambda: self.set_edit_mode('move'))
        elif feature_at_pos is not None:
            # Feature context menu
            context_menu.add_command(label="Add Balloon", 
                                   command=lambda: self.add_balloon_to_feature(feature_at_pos))
            context_menu.add_command(label="Edit Feature", 
                                   command=lambda: self.edit_feature(feature_at_pos))
        else:
            # General context menu
            context_menu.add_command(label="Add Manual Balloon", 
                                   command=lambda: self.add_manual_balloon(img_x, img_y))
            context_menu.add_separator()
            context_menu.add_command(label="Reset View", 
                                   command=self.reset_view)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def set_edit_mode(self, mode):
        """Set the editing mode"""
        self.edit_mode = mode
        if mode == 'view':
            self.canvas.configure(cursor="")
        elif mode == 'move':
            self.canvas.configure(cursor="hand2")
    
    def edit_balloon(self, balloon_index):
        """Open balloon editing dialog"""
        if balloon_index >= len(self.balloons):
            return
            
        balloon = self.balloons[balloon_index]
        
        # Create edit dialog
        dialog = BalloonEditDialog(self.canvas, balloon)
        result = dialog.show()
        
        if result:
            # Update balloon with new values
            self.balloons[balloon_index].update(result)
            self.refresh_display()
    
    def delete_balloon(self, balloon_index):
        """Delete a balloon"""
        if balloon_index >= len(self.balloons):
            return
            
        if messagebox.askyesno("Confirm Delete", "Delete this balloon?"):
            del self.balloons[balloon_index]
            self.selected_balloon = None
            self.refresh_display()
    
    def add_balloon_to_feature(self, feature_index):
        """Add a balloon to a specific feature"""
        if feature_index >= len(self.features):
            return
            
        feature = self.features[feature_index]
        
        # Create new balloon
        from balloon_manager import BalloonManager
        balloon_manager = BalloonManager()
        
        new_balloons = balloon_manager.create_balloons([feature])
        if new_balloons:
            # Assign next available number
            existing_numbers = [int(b['label']) for b in self.balloons if b['label'].isdigit()]
            next_number = max(existing_numbers) + 1 if existing_numbers else 1
            
            new_balloon = new_balloons[0]
            new_balloon['label'] = str(next_number)
            
            self.balloons.append(new_balloon)
            self.refresh_display()
    
    def add_manual_balloon(self, x, y):
        """Add a manual balloon at specified position"""
        # Create balloon data
        existing_numbers = [int(b['label']) for b in self.balloons if b['label'].isdigit()]
        next_number = max(existing_numbers) + 1 if existing_numbers else 1
        
        balloon = {
            'label': str(next_number),
            'x': x,
            'y': y,
            'radius': 20,
            'item_type': 'manual',
            'image_width': self.image_data['width'] if self.image_data else 1000,
            'image_height': self.image_data['height'] if self.image_data else 1000
        }
        
        self.balloons.append(balloon)
        self.refresh_display()
    
    def edit_feature(self, feature_index):
        """Open feature editing dialog"""
        if feature_index >= len(self.features):
            return
            
        feature = self.features[feature_index]
        
        # Create edit dialog
        dialog = FeatureEditDialog(self.canvas, feature)
        result = dialog.show()
        
        if result:
            # Update feature with new values
            self.features[feature_index].update(result)
            self.refresh_display()
    
    def reset_view(self):
        """Reset zoom and pan to default"""
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.refresh_display()
    
    def get_annotations_data(self):
        """Get current annotations data for export"""
        return {
            'features': self.features,
            'balloons': self.balloons,
            'image_data': self.image_data
        }

class BalloonEditDialog:
    """Dialog for editing balloon properties"""
    
    def __init__(self, parent, balloon):
        self.parent = parent
        self.balloon = balloon
        self.result = None
        
    def show(self):
        """Show the dialog and return result"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Edit Balloon")
        self.dialog.geometry("300x200")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Create form
        self.create_form()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
        return self.result
    
    def create_form(self):
        """Create the form elements"""
        frame = ttk.Frame(self.dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Label
        ttk.Label(frame, text="Label:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.label_var = tk.StringVar(value=self.balloon.get('label', ''))
        ttk.Entry(frame, textvariable=self.label_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        # Type
        ttk.Label(frame, text="Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.type_var = tk.StringVar(value=self.balloon.get('item_type', ''))
        ttk.Entry(frame, textvariable=self.type_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        frame.columnconfigure(1, weight=1)
    
    def ok_clicked(self):
        """Handle OK button click"""
        self.result = {
            'label': self.label_var.get(),
            'item_type': self.type_var.get()
        }
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click"""
        self.result = None
        self.dialog.destroy()

class FeatureEditDialog:
    """Dialog for editing feature properties"""
    
    def __init__(self, parent, feature):
        self.parent = parent
        self.feature = feature
        self.result = None
        
    def show(self):
        """Show the dialog and return result"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Edit Feature")
        self.dialog.geometry("350x250")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Create form
        self.create_form()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
        return self.result
    
    def create_form(self):
        """Create the form elements"""
        frame = ttk.Frame(self.dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Type
        ttk.Label(frame, text="Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.type_var = tk.StringVar(value=self.feature.get('type', ''))
        ttk.Entry(frame, textvariable=self.type_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        # Value
        ttk.Label(frame, text="Value:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.value_var = tk.StringVar(value=self.feature.get('value', ''))
        ttk.Entry(frame, textvariable=self.value_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        # Symbol type
        ttk.Label(frame, text="Symbol:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.symbol_var = tk.StringVar(value=self.feature.get('symbol_type', ''))
        ttk.Entry(frame, textvariable=self.symbol_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        frame.columnconfigure(1, weight=1)
    
    def ok_clicked(self):
        """Handle OK button click"""
        self.result = {
            'type': self.type_var.get(),
            'value': self.value_var.get(),
            'symbol_type': self.symbol_var.get()
        }
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click"""
        self.result = None
        self.dialog.destroy()