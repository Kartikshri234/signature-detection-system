# Frontend Setup Guide

## Prerequisites

- **Node.js** 14+ and **npm** 6+
- **Python** 3.7+

## Installation

### 1. Install Python Dependencies

```bash
# From project root
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Running the Application

### Development Mode

**Terminal 1 - Start Flask Backend:**
```bash
python api.py
```
Backend will run on: `http://localhost:5000`

**Terminal 2 - Start React Frontend:**
```bash
cd frontend
npm start
```
Frontend will run on: `http://localhost:3000`

### Production Build

```bash
cd frontend
npm run build
```
This creates an optimized production build in `frontend/build/` directory.

## Project Structure

```
signature_detection_system/
├── main.py                 # Original Tkinter GUI (legacy)
├── api.py                  # New Flask REST API
├── requirements.txt        # Python dependencies
├── db/                     # Database folder (auto-created)
│   └── *.pickle           # User signature data files
│
└── frontend/              # React web application
    ├── public/            # Static files
    ├── src/               # React source code
    │   ├── App.js         # Main component
    │   ├── App.css        # Global styles
    │   ├── index.js       # React entry point
    │   └── pages/         # Page components
    │       ├── Register.js
    │       ├── Detect.js
    │       └── Users.js
    ├── package.json
    └── README.md
```

## Features

### ✅ Register Page
- Real-time camera capture
- Signature feature extraction
- User registration with name

### ✅ Detect Page
- Live signature detection
- Signature matching against database
- Confidence percentage display

### ✅ Users Page
- View all registered users
- Manage user database
- Delete users

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/users` - Get all registered users
- `POST /api/register` - Register new user
- `POST /api/detect` - Detect signature
- `DELETE /api/delete-user/<username>` - Delete user

## Troubleshooting

### CORS Issues
If you see CORS errors, make sure both servers are running:
- Backend on `http://localhost:5000`
- Frontend on `http://localhost:3000`

### Camera Not Working
- Check browser camera permissions
- Ensure no other app is using the camera
- Try stopping and restarting the app

### Dependencies Installation Error
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
npm install
```

## Performance Tips

1. **Signature Quality**: Use good lighting and clear signatures
2. **Gesture Consistency**: Sign the same way each time
3. **Background**: Use white paper with dark ink

## Next Steps

- Deploy to cloud (Heroku, AWS, Google Cloud)
- Add user authentication
- Implement signature verification threshold settings
- Add logging and analytics
