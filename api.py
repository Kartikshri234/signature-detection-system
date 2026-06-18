"""
Flask API for Signature Detection System
Provides REST endpoints for the React frontend
"""

import os
import pickle
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)

# Configuration
DB_DIR = './db'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create directories if they don't exist
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_features(image_data):
    """Extract ORB features from image"""
    orb = cv2.ORB_create()
    gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    keypoints, descriptors = orb.detectAndCompute(thresh, None)
    return keypoints, descriptors


def recognize_signature(image_data):
    """Compare captured signature with database"""
    orb = cv2.ORB_create()
    gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    keypoints_unknown, descriptors_unknown = orb.detectAndCompute(thresh, None)
    
    if descriptors_unknown is None or len(keypoints_unknown) < 10:
        return {'status': 'invalid', 'name': None, 'confidence': 0}
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    best_match_count = 0
    best_match_name = None
    
    if not os.path.exists(DB_DIR):
        return {'status': 'invalid', 'name': None, 'confidence': 0}
    
    for filename in os.listdir(DB_DIR):
        if not filename.endswith('.pickle'):
            continue
        
        file_path = os.path.join(DB_DIR, filename)
        
        try:
            with open(file_path, 'rb') as file:
                descriptors_stored = pickle.load(file)
            
            if descriptors_stored is None:
                continue
            
            matches = bf.match(descriptors_stored, descriptors_unknown)
            good_matches = [m for m in matches if m.distance < 50]
            
            if len(good_matches) > best_match_count and len(good_matches) > 15:
                best_match_count = len(good_matches)
                best_match_name = filename.replace('.pickle', '')
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    if best_match_name:
        confidence = min(100, (best_match_count / 20) * 100)  # Calculate confidence
        return {'status': 'valid', 'name': best_match_name, 'confidence': confidence}
    else:
        return {'status': 'invalid', 'name': None, 'confidence': 0}


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Signature Detection API is running'})


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get list of registered users"""
    users = []
    if os.path.exists(DB_DIR):
        for filename in os.listdir(DB_DIR):
            if filename.endswith('.pickle'):
                users.append(filename.replace('.pickle', ''))
    return jsonify({'users': sorted(users)})


@app.route('/api/register', methods=['POST'])
def register_user():
    """Register a new user with signature"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'image' not in data:
            return jsonify({'status': 'error', 'message': 'Name and image are required'}), 400
        
        name = secure_filename(data['name'].strip())
        if not name:
            return jsonify({'status': 'error', 'message': 'Invalid name'}), 400
        
        # Decode base64 image
        try:
            image_data = base64.b64decode(data['image'].split(',')[1])
            image = Image.open(BytesIO(image_data))
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Invalid image format: {str(e)}'}), 400
        
        # Extract features
        keypoints, descriptors = extract_features(image_cv)
        
        if descriptors is None or len(keypoints) < 10:
            return jsonify({'status': 'error', 'message': 'No valid signature found. Try again with a clearer signature.'}), 400
        
        # Check if user already exists
        file_path = os.path.join(DB_DIR, f"{name}.pickle")
        if os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': f'User "{name}" already registered'}), 400
        
        # Save signature
        with open(file_path, 'wb') as file:
            pickle.dump(descriptors, file)
        
        return jsonify({'status': 'success', 'message': f'User "{name}" registered successfully!'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


@app.route('/api/detect', methods=['POST'])
def detect_signature():
    """Detect and validate signature"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'status': 'error', 'message': 'Image is required'}), 400
        
        # Decode base64 image
        try:
            image_data = base64.b64decode(data['image'].split(',')[1])
            image = Image.open(BytesIO(image_data))
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Invalid image format: {str(e)}'}), 400
        
        # Recognize signature
        result = recognize_signature(image_cv)
        
        if result['status'] == 'valid':
            return jsonify({
                'status': 'success',
                'result': result['status'],
                'name': result['name'],
                'confidence': round(result['confidence'], 2),
                'message': f'Signature matched! Welcome, {result["name"]}!'
            })
        else:
            return jsonify({
                'status': 'success',
                'result': result['status'],
                'name': None,
                'confidence': 0,
                'message': 'Signature not matched. Please try again or register.'
            })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


@app.route('/api/delete-user/<username>', methods=['DELETE'])
def delete_user(username):
    """Delete a registered user"""
    try:
        username = secure_filename(username)
        file_path = os.path.join(DB_DIR, f"{username}.pickle")
        
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': f'User "{username}" not found'}), 404
        
        os.remove(file_path)
        return jsonify({'status': 'success', 'message': f'User "{username}" deleted successfully!'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
