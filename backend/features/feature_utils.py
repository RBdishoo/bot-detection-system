"""
Utility Functions for Feature Engineering

Mathematical functions used to calculate:
1) Mouse Trajectory Analysis (distance, velocity, angles)
2) Keystroke dynamics Analysis (entropy, inter-key delays)


"""

import math
import numpy as np
from typing import List, Tuple

class MouseTrajectoryUtils:

    """
    Utility Functions for Mouse Movement Analysis
    """

    @staticmethod

    def distance(pointOne: Tuple[float, float], pointTwo: Tuple[float, float]) -> float:

        """
        Calculating Euclidean distance between two 2D points

        Formula: distance = sqrt((x2-x1)^2 + (y2-y1)^2)

        Arguments: pointOne - first point as (x,y) tuple.   pointTwo - second point as (x,y) tuple

        Return: Distance in Pixels

        Why this matters for bot detection:

        Human movement:
            move 50px, pause
            move 30 px at a different angle
            move 80px slowly 
            Result : varying distances -> possible bot detection

        Bot Movement:
            Move exactly 25px every 100ms
            Move exactly 25px again every 100ms
            Result: Too perfect -> more suspicious, lack of irregularity (hence robotic)
        """

        #Unpack coordinates
        x1, y1 = pointOne
        x2, y2 = pointTwo

        #Calculate Differences
        dx = x2 - x1 #horizontal
        dy = y2-y1  #Vertical

        #apply pythagorean theorem
        return math.sqrt(dx**2 + dy**2)

    @staticmethod
    def velocityPixelsPerSecond(distancePx : float, timeMs: float) -> float:
        """
        Calculating Mouse Movement
        
            - converts distance and time to velocity in pixels/second
            Fomula: velocity = (distance / time(in Milliseconds) * 1000) 

            Why this matters for bot detection:

            Human mouse movement:
                varies in speed, natural acceleration and deceleration (not constant / regular)

            Bot Movement:
                perfectly consistent, Mechanical precision (no irregularities, standard deviation near to 0) -> more suspicious, easier to flag
        """

        #Edge Case: avoiding division by 0
        if timeMs <= 0:
            return 0.0
        
        #Convert: (px/ms) * (1000ms / sec) = px/sec
        return (distancePx / timeMs) * 1000.0

    @staticmethod
    def angleBetween(pointOne: Tuple[float, float], pointTwo: Tuple[float, float], pointThree: Tuple[float, float]) -> float:

        """
        Calculate the angle at pointTwo formed by the path pointOne, pointTwo, and pointThree.

        This measures how much the path curves at point2
            Straight line: angle approx 0
            Right Angle: angle Approx 1.57 rad (pi/2)
            Sharp Turn: angle approx 3.14 rad (pi)

        Uses Vector math:
        1) Create two vectors from pointTwo 
        2) Calculate angle between them using aTan2

        What's returned:
            Angle in radians, Range between 0 and pi

        Why this matters:

            Humans have curved, irregular paths (high angle variance)
            Bots often move in straight lines (low angle variance)
            std deviation of angles = bot detection signal
        
        """

        #Create vectors from pointTwo to pointOne, and pointTwo to pointThree
        vectorOne = (pointOne[0] - pointTwo[0], pointOne[1] - pointTwo[1])     #Vector pointTwo -> pointOne 
        vectorTwo = (pointThree[0] - pointTwo[0], pointThree[1] - pointTwo[1])   #Vector pointTwo -> pointThree

        #Dot Product for angle magnitude

        dot = vectorOne[0] * vectorTwo[0] + vectorOne[1] * vectorTwo[1]

        #Determinant for angle sign

        det = vectorOne[0] * vectorTwo[1] - vectorOne[1] * vectorTwo[0]

        #aTan2 gives signed angle, abs() gives range [0, pi]

        angle = math.atan2(det, dot)

        return abs(angle) #Always positive



    @staticmethod
    def extractCoordinatesAndTimes(moves: List[dict]) -> Tuple[List[Tuple[float, float]], List[float]]:
        """
        Extract coordinates and time deltas from raw mouse move events.

        Converts raw format to usable format for calculations

        Returns: 
        Tuple of - Coordinates: List of (x, y) tuples
        timeDeltas: List of milliseconds between consecutive events

        Why useful:
            - Seperates posistions from time intervals
            - Allows Calculating Velocity for each interval
            - Enables Angle calculation for triplets of points
        """

        #Edge Case: need at least 2 points to have a movement

        if len(moves) < 2:
            return [], []
        
        #Extract (x, y) coordinates from each move
        coords = [(m['x'], m['y']) for m in moves]

        #Extract timestamps in milliseconds

        timestamps = [m['ts'] for m in moves]

        #Calculate time between consecutive events
        # for example: events at [1000ms, 1100ms, 1300ms]
        #Deltas are [100ms, 200ms]

        timeDeltas = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]

        return coords, timeDeltas
    
class KeystrokeUtils:

    """Utility functions for keystroke dynamics"""

    @staticmethod
    def calculateEntropy(items: List) -> float:
        """
        Calculate Shannon entropy of a List
        
        Entropy measuers randomness:
            low entropy = more repetition, less randmoness
            high entropy = more diverse, more unique items

            Formula: H = -Σ(probabilityI * log₂(probabilityI))
            where probabilityI = probability of an item i

        Arguments: 
            List of any items(strings, ints etc)

        Returns:
            Entropy Val (0 to approx 3 typical for keystroke data)

        Why this matters:
            Humans - diverse keys, higher entropy (2.0+)
            Bots - Repetitive keys, low entropy (0.0-0.5)
        """

        #Edge Case: empty list
        
        if len(items) == 0:
            return 0.0
        
        from collections import Counter

        #Count occurences of each item
        counts = Counter(items)
        total = len(items)

        #Calculate Entropy 
        entropy = 0.0
        for count in counts.values():
            #Probability of this item
            p = count / total

            #Shannon entropy formula
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy
    
    @staticmethod
    def interKeyDelays(keys: List[dict]) -> List[float]:
        """
        Calculate time between consecutive keypresses.

        Most effective way to determine between human and bot signals

        Human typing:
            natural variance(50-300ms typically)
            Each keystroke takes human reaction time

        Bot Typing:
            Too fast (less than 30ms) or perfectly regular
            no natural variation

        Returns:
            List of delays in milliseconds between consecutive keystrokes
        
        """
        #Edge Case: Need at least 2 keystrokes to measure delay 
        if len(keys) < 2:
            return []
        
        #Extract timestamps
        timestamps = [k['ts'] for k in keys]

        #Calculate delays between consecutive keystrokes
        delays = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]

        return delays
    




   