"""
Signal Collector Module 

    Handles persistent storage of behavioral signals to JSON lines format.
    Each line is a complete signal batch (valid JSON).

    Why JSON Lines are used?
    Because they can perform quick append-only operations, each batch is independent (making it easier to process), human-readable making it easier to debug, and no need to load entire file into memory.

    
    __init__() sets up the collector and ensure files exists
    saveSignalBatch() appends one batch of signals to the file
    getBatchCount() returns total batches collected
    getSessionCount() returns unique session count
    getLatestSignal() gets the most recent signals for debugging
"""

import json
import os
from datetime import datetime
from utils.helpers import getSignalsFile, formatTimestamp

class SignalCollector:

    """
    Manages the storage of user behavioral signals. These signals are stored in JSON Lines formate (one JSON object per line).
    It's thread-safe for concurrent writes from multiple users

    """
    def __init__(self):
        """Initializes the signal collector"""
        self.signalsFile = getSignalsFile()
        self.ensureFileExists()

    def ensureFileExists(self):
        """Create signals.json1 file if it doesn't exist"""
        if not os.path.exists(self.signalsFile):
            #creates empty file
            open(self.signalsFile, 'a').close()

    def saveSignalBatch(self, batchData):
        """Saves a batch of signals to the file """
        try:
            #add a timestamp if not present
            if 'timestamp' not in batchData:
                batchData['timestamp'] = formatTimestamp()
            
            #convert to JSON and appent to file (one line per batch)
            with open(self.signalsFile, 'a') as f:
                f.write(json.dumps(batchData) + '\n')

            return True
        except Exception as e:
            print(f"Error saving signal batch: {e}")
            return False
        
    def getBatchCount(self):

        """Get total number of batches collected """
        try:
            with open(self.signalsFile, 'r') as f:
                count = sum(1 for line in f)
            return count
        except Exception as e:
            print(f"Error counting batches: {e}")
            return 0
        
    def getSessionCount(self):
        """Get Number of unique session IDs"""
        try:
            sessions = set()
            with open(self.signalsFile, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    sessions.add(data.get('sessionID'))
            return len(sessions)
        except Exceptions as e:
            print(f"Error counting sessions: {e}")
        return 0

    def getLatestSignals(self, limit=10):
        """Get the most recent signal batches, useful for debugging and seeing what's being collected."""
        try:
            signals = []
            with open(self.signalsFile, 'r') as f:
                allLines = f.readlines()
            
            # Get last 'limit' lines
            for line in allLines[-limit:]:
                signals.append(json.loads(line))

            return signal
        except Exception as e:
            print(f"Error retrieving signals: {e}")
            return []
        
