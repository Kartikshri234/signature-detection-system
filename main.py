"""
Live Signature Detection System
A GUI-based application for registering and validating signatures using computer vision.
"""

import os
import pickle
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np

class SignatureDetectionApp:
    def __init__(self):
        # Initialize main window
        self.main_window = tk.Tk()
        self.main_window.title("Live Signature Detection System")
        self.main_window.geometry("1200x700")
        self.main_window.configure(bg="#2C3E50")
        
        # Database directory setup
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        
        # Variables for capturing signatures
        self.most_recent_capture_arr = None
        self.register_new_user_capture = None
        
        # Initialize webcam
        self.webcam = cv2.VideoCapture(0)
        
        # Build the GUI
        self.build_gui()
        
        # Start video feed
        self.update_webcam_feed()
    
    def build_gui(self):
        """Create the main GUI layout"""
        # Title Label
        title_label = tk.Label(
            self.main_window,
            text="LIVE SIGNATURE DETECTION SYSTEM",
            font=("Arial", 24, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Main container frame
        container = tk.Frame(self.main_window, bg="#2C3E50")
        container.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Left side - Webcam feed
        left_frame = tk.Frame(container, bg="#34495E", relief=tk.RIDGE, bd=3)
        left_frame.pack(side="left", padx=10, fill="both", expand=True)
        
        webcam_label = tk.Label(
            left_frame,
            text="CAMERA FOR CAPTURING SIGNATURE",
            font=("Arial", 12, "bold"),
            bg="#34495E",
            fg="#ECF0F1"
        )
        webcam_label.pack(pady=10)
        
        self.webcam_label = tk.Label(left_frame, bg="#000000")
        self.webcam_label.pack(padx=10, pady=10)
        
        # Right side - Controls
        right_frame = tk.Frame(container, bg="#34495E", relief=tk.RIDGE, bd=3)
        right_frame.pack(side="right", padx=10, fill="both", expand=True)
        
        controls_label = tk.Label(
            right_frame,
            text="SIGNATURE CONTROLS",
            font=("Arial", 14, "bold"),
            bg="#34495E",
            fg="#ECF0F1"
        )
        controls_label.pack(pady=15)
        
        # Detect Button
        self.detect_button = tk.Button(
            right_frame,
            text="Detect Signature",
            font=("Arial", 14, "bold"),
            bg="#27AE60",
            fg="white",
            command=self.detect_signature,
            height=2,
            width=20
        )
        self.detect_button.pack(pady=15)
        
        # Register Section
        register_frame = tk.Frame(right_frame, bg="#34495E")
        register_frame.pack(pady=20, padx=20, fill="x")
        
        register_title = tk.Label(
            register_frame,
            text="REGISTER NEW USER",
            font=("Arial", 12, "bold"),
            bg="#34495E",
            fg="#ECF0F1"
        )
        register_title.pack(pady=10)
        
        name_label = tk.Label(
            register_frame,
            text="Please Enter Your Name:",
            font=("Arial", 11),
            bg="#34495E",
            fg="#ECF0F1"
        )
        name_label.pack(pady=5)
        
        self.entry_text_register_new_user = tk.Text(
            register_frame,
            height=1,
            width=25,
            font=("Arial", 12)
        )
        self.entry_text_register_new_user.pack(pady=5)
        
        # Button frame for Accept and Try Again
        button_frame = tk.Frame(register_frame, bg="#34495E")
        button_frame.pack(pady=10)
        
        self.accept_button = tk.Button(
            button_frame,
            text="Accept",
            font=("Arial", 11, "bold"),
            bg="#3498DB",
            fg="white",
            command=self.accept_register_new_user,
            width=12
        )
        self.accept_button.pack(side="left", padx=5)
        
        self.try_again_button = tk.Button(
            button_frame,
            text="Try Again",
            font=("Arial", 11, "bold"),
            bg="#E74C3C",
            fg="white",
            command=self.try_again_registration,
            width=12
        )
        self.try_again_button.pack(side="left", padx=5)
        
        self.register_button = tk.Button(
            right_frame,
            text="Register New User",
            font=("Arial", 14, "bold"),
            bg="#E67E22",
            fg="white",
            command=self.register_new_user,
            height=2,
            width=20
        )
        self.register_button.pack(pady=15)
    
    def update_webcam_feed(self):
        """Continuously update the webcam feed"""
        ret, frame = self.webcam.read()
        if ret:
            # Store the most recent frame
            self.most_recent_capture_arr = frame.copy()
            
            # Convert frame for display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            
            # Add text overlay
            cv2.putText(frame, "Place signature here", (180, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Convert to PhotoImage
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.webcam_label.imgtk = imgtk
            self.webcam_label.configure(image=imgtk)
        
        # Schedule next update
        self.webcam_label.after(20, self.update_webcam_feed)
    
    def detect_signature(self):
        """Detect and validate signature"""
        if self.most_recent_capture_arr is None:
            self.show_message("Error", "No image captured. Please try again.")
            return
        
        result, name = self.recognize_signature(self.most_recent_capture_arr)
        
        if result == 'valid':
            self.show_message("Valid", f"Signature is valid. Welcome, {name}!")
        else:
            self.show_message("Invalid", "Signature is invalid. Please try again or register.")
    
    def register_new_user(self):
        """Capture signature for new user registration"""
        if self.most_recent_capture_arr is None:
            self.show_message("Error", "No image captured. Please try again.")
            return
        
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
        self.show_message("Success", "Signature captured! Please enter your name and click Accept.")
    
    def accept_register_new_user(self):
        """Save the registered user's signature"""
        name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()
        
        if not name:
            self.show_message("Error", "Please enter a name.")
            return
        
        if self.register_new_user_capture is None:
            self.show_message("Error", "Please capture a signature first.")
            return
        
        # Extract features using ORB
        orb = cv2.ORB_create()
        gray = cv2.cvtColor(self.register_new_user_capture, cv2.COLOR_BGR2GRAY)
        
        # Preprocess: Apply thresholding to enhance signature
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        keypoints, descriptors = orb.detectAndCompute(thresh, None)
        
        if descriptors is not None and len(keypoints) > 10:
            # Save to database
            file_path = os.path.join(self.db_dir, f"{name}.pickle")
            with open(file_path, 'wb') as file:
                pickle.dump(descriptors, file)
            
            self.show_message("Success", "User was registered successfully!")
            self.entry_text_register_new_user.delete(1.0, tk.END)
            self.register_new_user_capture = None
        else:
            self.show_message("Error", "No valid signature found. Try again with a clearer signature.")
    
    def try_again_registration(self):
        """Reset registration capture"""
        self.register_new_user_capture = None
        self.entry_text_register_new_user.delete(1.0, tk.END)
        self.show_message("Info", "Ready to capture new signature. Click 'Register New User'.")
    
    def recognize_signature(self, img):
        """Compare captured signature with database"""
        orb = cv2.ORB_create()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Preprocess
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        keypoints_unknown, descriptors_unknown = orb.detectAndCompute(thresh, None)
        
        if descriptors_unknown is None or len(keypoints_unknown) < 10:
            return 'invalid', None
        
        # BFMatcher for descriptor matching
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        best_match_count = 0
        best_match_name = None
        
        # Check all registered signatures
        if not os.path.exists(self.db_dir):
            return 'invalid', None
        
        for filename in os.listdir(self.db_dir):
            if not filename.endswith('.pickle'):
                continue
            
            file_path = os.path.join(self.db_dir, filename)
            
            try:
                with open(file_path, 'rb') as file:
                    descriptors_stored = pickle.load(file)
                
                if descriptors_stored is None:
                    continue
                
                # Match descriptors
                matches = bf.match(descriptors_stored, descriptors_unknown)
                
                # Filter good matches (distance threshold)
                good_matches = [m for m in matches if m.distance < 50]
                
                # Check if this is the best match
                if len(good_matches) > best_match_count and len(good_matches) > 15:
                    best_match_count = len(good_matches)
                    best_match_name = filename.replace('.pickle', '')
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        if best_match_name:
            return 'valid', best_match_name
        else:
            return 'invalid', None
    
    def show_message(self, title, message):
        """Display message box"""
        messagebox.showinfo(title, message)
    
    def run(self):
        """Start the application"""
        self.main_window.mainloop()
    
    def __del__(self):
        """Cleanup when application closes"""
        if hasattr(self, 'webcam'):
            self.webcam.release()

if __name__ == "__main__":
    app = SignatureDetectionApp()
    app.run()