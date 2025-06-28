# Vulnerability Scanner Web Interface

This is a web interface for the Automated Vulnerability Scanning with Agentic AI project. It provides a user-friendly UI to start vulnerability scans and view real-time scanning logs and results.

## Project Structure

```
web-project/
├── backend/               # Flask backend
│   ├── app.py             # Main Flask application
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── public/            # Static files
│   ├── src/               # React components and source code
│   └── package.json       # JavaScript dependencies
└── README.md              # This file
```

## Features

- Start vulnerability scans with custom targets and descriptions
- Real-time streaming of scan logs and agent outputs
- View completed scan reports in Markdown format
- Download reports for offline viewing

## Prerequisites

- Node.js (v14+) for the frontend
- Python (v3.7+) for the backend
- OpenAI API key for the AI agents

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the backend server:
   ```
   python app.py
   ```

The backend will be available at http://localhost:5000.

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

The frontend will be available at http://localhost:3000.

## Usage

1. Open the web interface at http://localhost:3000
2. Click on "Start New Scan"
3. Enter the target IP or hostname, your OpenAI API key, and a description of what you want to scan for
4. Click "Start Scan" to begin the vulnerability scan
5. Watch the real-time logs as the AI agents work
6. When the scan is complete, view and download the report

## Environment Variables

### Frontend

- `REACT_APP_API_URL`: The URL of the backend API (default: http://localhost:5000)
- `REACT_APP_SOCKET_URL`: The URL for WebSocket connections (default: same as API_URL)

### Backend

- No specific environment variables are required, but you can set `FLASK_ENV=development` for development mode.

## Development

- The backend uses Flask and Flask-SocketIO for real-time communication
- The frontend is built with React and uses Socket.io client for WebSocket connections
- Bootstrap is used for UI components

## Troubleshooting

- If you see connection errors in the frontend, make sure the backend server is running
- If scanning doesn't start, check that you've entered a valid OpenAI API key
- For any WebSocket issues, check the browser console for error messages 