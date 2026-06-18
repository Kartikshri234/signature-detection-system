# Live Signature Detection System

A computer vision-based application for registering and validating signatures in real-time using webcam input.

---

## 📋 Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [Code Explanation](#code-explanation)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **Real-time Signature Capture**: Uses webcam to capture signatures
- **Signature Registration**: Register new users with their signatures
- **Signature Validation**: Validate signatures against registered database
- **Feature Extraction**: Uses ORB (Oriented FAST and Rotated BRIEF) algorithm
- **User-Friendly GUI**: Built with Tkinter
- **File-based Database**: Stores signatures as pickle files

---

## 💻 System Requirements

- **Python**: 3.7 or higher
- **Webcam**: Built-in or external USB webcam
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB recommended
- **Storage**: At least 100MB free space

---

## 📦 Installation

### Step 1: Install Python
Download and install Python from [python.org](https://www.python.org/downloads/)

During installation, make sure to check "Add Python to PATH"

### Step 2: Create Project Directory
```bash
# Create a new folder for the project
mkdir signature_detection_system
cd signature_detection_system
```

### Step 3: Install Required Libraries
```bash
# Install all dependencies
pip install opencv-python==4.8.1.78
pip install opencv-contrib-python==4.8.1.78
pip install pillow==10.0.0
pip install numpy==1.24.3
```

**Alternative (using requirements.txt):**
Create a file named `requirements.txt` with:
```
opencv-python==4.8.1.78
opencv-contrib-python==4.8.1.78
pillow==10.0.0
numpy==1.24.3
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 4: Create Project Files
1. Copy the `main.py` code into a file named `main.py`
2. The application will automatically create a `db` folder for storing signatures

---

## 📁 Project Structure

```
signature_detection_system/
│
├── main.py                 # Original Tkinter GUI
├── api.py                  # New Flask REST API
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── FRONTEND_SETUP.md      # Frontend setup guide
│
├── frontend/              # React web application
│   ├── public/            # Static files
│   ├── src/               # React source code
│   ├── package.json
│   └── ...
│
└── db/                    # Database folder (auto-created)
    ├── user1.pickle       # Stored signature features
    ├── user2.pickle
    └── ...
```

---

## 🚀 How to Run

### Method 1: Using the Modern Web Frontend (Recommended) ✨

**NEW!** We now have a modern React web interface with Flask API backend.

1. **Install dependencies:**
```bash
pip install -r requirements.txt
cd frontend && npm install
```

2. **Start the backend (Terminal 1):**
```bash
python api.py
```

3. **Start the frontend (Terminal 2):**
```bash
cd frontend
npm start
```

4. **Open browser:** `http://localhost:3000`

See [FRONTEND_SETUP.md](FRONTEND_SETUP.md) for detailed setup instructions.

### Method 2: Using the Original Tkinter GUI

**Original desktop application using Tkinter:**

```bash
python main.py
```

This is simpler but less feature-rich than the web version.

---

## 📖 How to Use

### Registering a New User

1. **Launch the application**
   - The webcam feed will appear on the left side

2. **Capture signature**
   - Place a white paper with your signature in front of the camera
   - Ensure good lighting and clear visibility
   - Click **"Register New User"** button

3. **Enter name**
   - Type your name in the text box
   - Click **"Accept"** to save
   - Or click **"Try Again"** to recapture

4. **Success!**
   - A popup will confirm registration
   - Your signature is now stored in the database

### Validating a Signature

1. **Position signature**
   - Show your signature to the camera
   - Ensure it's clearly visible

2. **Click "Detect Signature"**
   - The system will process the image
   - Compare with registered signatures

3. **View result**
   - **Valid**: Shows "Signature is valid. Welcome, [Name]!"
   - **Invalid**: Shows "Signature is invalid"

---

## 🔍 Code Explanation

### 1. **Class Structure** (`SignatureDetectionApp`)

The entire application is built as a single class for better organization:

```python
class SignatureDetectionApp:
    def __init__(self):
        # Initialize GUI, webcam, and database
```

### 2. **GUI Components** (`build_gui()`)

Creates the user interface with:
- **Left Panel**: Webcam feed display
- **Right Panel**: Control buttons and registration form
- **Styling**: Professional look with colors

### 3. **Webcam Feed** (`update_webcam_feed()`)

```python
def update_webcam_feed(self):
    # Continuously capture frames from webcam
    # Update display every 20ms for smooth video
```

**How it works:**
- Reads frames from webcam using OpenCV
- Converts BGR to RGB for Tkinter display
- Adds overlay text
- Schedules next update (creates video effect)

### 4. **Feature Extraction** (ORB Algorithm)

```python
orb = cv2.ORB_create()
keypoints, descriptors = orb.detectAndCompute(image, None)
```

**ORB (Oriented FAST and Rotated BRIEF):**
- Detects key points (distinctive features) in signature
- Creates descriptors (unique patterns) for each keypoint
- Fast and rotation-invariant
- Perfect for signature matching

### 5. **Image Preprocessing**

```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
```

**Steps:**
1. Convert to grayscale (reduces complexity)
2. Apply binary threshold (signature becomes white, background black)
3. Enhances signature features for better detection

### 6. **Registration** (`accept_register_new_user()`)

**Process:**
1. Gets user's name from text input
2. Extracts features from captured signature
3. Saves descriptors to pickle file (serialization)
4. File named as `username.pickle`

### 7. **Validation** (`recognize_signature()`)

**Matching Process:**
```python
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(stored_descriptors, new_descriptors)
good_matches = [m for m in matches if m.distance < 50]
```

**Steps:**
1. Extract features from live signature
2. Load all registered signatures from database
3. Use BFMatcher (Brute Force Matcher) to compare
4. Count matches with distance < 50 (threshold)
5. If good_matches > 15, signature is valid

**Why these thresholds?**
- **Distance < 50**: Ensures similar features
- **Matches > 15**: Prevents false positives

### 8. **Database System**

**File-based storage:**
- Each user = one `.pickle` file
- Contains serialized numpy array of descriptors
- Lightweight and portable
- Easy to upgrade to SQL database later

---

## 🔧 Troubleshooting

### Issue 1: "No module named 'cv2'"
**Solution:**
```bash
pip install opencv-python
```

### Issue 2: Webcam not opening
**Solutions:**
- Check if camera is connected
- Close other apps using the camera
- Try changing camera index:
```python
self.webcam = cv2.VideoCapture(1)  # Try 1, 2, etc.
```

### Issue 3: "No valid signature found"
**Solutions:**
- Use black ink on white paper
- Ensure good lighting
- Signature should be clear and visible
- Hold signature steady for 2-3 seconds
- Adjust threshold value (line 158):
```python
_, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)  # Try 100 instead of 127
```

### Issue 4: False rejections (valid signature marked invalid)
**Solutions:**
- Lower the matching threshold:
```python
good_matches = [m for m in matches if m.distance < 60]  # Increase from 50
```
- Lower required matches:
```python
if len(good_matches) > 12:  # Decrease from 15
```

### Issue 5: Database errors
**Solution:**
- Delete the `db` folder and restart
- Re-register all users

### Issue 6: GUI appears too small/large
**Solution:**
Change window size (line 21):
```python
self.main_window.geometry("1400x800")  # Adjust dimensions
```

---

## 🎯 Tips for Best Results

1. **Lighting**: Use bright, even lighting
2. **Background**: Plain white background works best
3. **Signature**: Use thick, clear strokes
4. **Distance**: Keep signature 1-2 feet from camera
5. **Steadiness**: Hold signature still for capture
6. **Consistency**: Sign the same way each time

---

## 🔐 Security Notes

- This is a **basic implementation** for educational purposes
- For production use, consider:
  - Encrypting pickle files
  - Using proper database (PostgreSQL/MongoDB)
  - Adding anti-spoofing measures
  - Implementing liveness detection
  - Adding user authentication

---

## 📝 Future Enhancements

- [ ] Add signature quality check
- [ ] Support multiple signatures per user
- [ ] Implement cloud storage
- [ ] Add signature similarity percentage
- [ ] Create admin panel for user management
- [ ] Add logging and audit trails
- [ ] Export/import database functionality

---

## 📄 License

This project is for educational purposes. Feel free to modify and use.

---

## 👥 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure webcam permissions are granted
4. Test with different signatures and lighting

---

**Happy Coding! 🚀**