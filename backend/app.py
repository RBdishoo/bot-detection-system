"""
Bot Detection System - Flask Backend 

Main application server which does the following:
    1. Serves the Frontend (index.html)
    2. Receives Signal Batches from JavaScript
    3. Stores signals using SignalCollector
    4. Provides statistics endpoints


Architecture:
    - Post /api/signals -> Save Signal Batch
    - GET /api/states -> Get collection statistics 
    - GET / -> Serve Frontend HTML    
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import sys

# Add parent Directory to path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collectors.signal_collector import SignalCollector
from utils.helpers import (
    genSeshID,
    isValidSignalBatch,
    formatTimestamp
)

#Initialize Flask application
app = Flask(__name__, static_folder='../frontend', static_url_path='')

#Initialize Signal Collector
collector = SignalCollector()

#Store active session Count for simple tracking
activeSessions = set()

@app.route('/api/stats', methods=['GET'])
def getStats():
    """
    GET /api/stats - Returns collection statistics (total batches, num of unique sessions, signals file size, and server timestamp)
    """

    try:
        totalBatches = collector.getBatchCount()
        uniqueSessions = collector.getSessionCount()
        signalsFile = collector.getSignalsFile()
        fileSizeKb = 0
        if os.path.exists(signalsFile):
            fileSizeKb = os.path.getsize(signalsFile) / 1024

        return jsonify({
            "Total Batches": totalBatches,
            "Unique Sessions": uniqueSessions,
            "Signals File Size (in Kb)": round(fileSizeKb, 1),
            "Signals File": signalsFile,
            "Server Timestamp": formatTimestamp()
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/signals', methods=['POST'])
def saveSignals():
    """
    POST /api/signals - Receives signal batches from frontend JavaScripts
    """

    try:
        #Get JSON data from request
        data = request.get_json()

        print("DEBUG incoming batch:", data, flush=True)

        if not data:
             return jsonify({"Error": "No JSON data received"}), 400

        #Validate structure
        if not isValidSignalBatch(data):
            return jsonify({
                "Error": "Invalid signal batch format",
                "received__keys": list(data.keys()),
                "signals_type": str(type(data.get("signals"))),
                }), 400
        

        
        #Save to file
        success = collector.saveSignalBatch(data)

        if success:
            return jsonify({
                "success": True,
                "message": f"Saved batch for session {data.get('sessionID', 'unknown')}",
                "Total Batches": collector.getBatchCount(),
                "Session ID": data.get('sessionID')
            }), 200
        else:
            return jsonify({"Error": "Failed to save batch"}), 500
        
    except Exception as e:
        return jsonify({"Error": f"Server error: {str(e)}"}), 500
    
@app.route('/', methods=['GET'])

def serveFrontend():
    """
    GET / -> Serves the main frontend page. Returns index.html from frontend/ folder
    """
    return send_from_directory('../frontend', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)