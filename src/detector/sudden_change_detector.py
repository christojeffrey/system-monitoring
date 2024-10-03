import numpy as np


# detect using moving average
class SuddenChangeDetector:
    def __init__(self, WINDOW_SIZE, ANOMALY_THRESHOLD):
        self.window = []
        self.WINDOW_SIZE = WINDOW_SIZE
        self.ANOMALY_THRESHOLD = ANOMALY_THRESHOLD
    
    def detect(self, data):
        temp = data['Temperature'].iloc[-1]

        # Add the new temperature to the window
        self.window.append(temp)
        if len(self.window) > self.WINDOW_SIZE:
            self.window.pop(0)

        # If we don't have enough data points yet, return normal
        if len(self.window) < self.WINDOW_SIZE:
            return False, "Normal"

        # Calculate moving average and standard deviation
        moving_avg = np.mean(self.window)
        moving_std = np.std(self.window)

        # If the current temperature deviates significantly from the moving average,
        # consider it an anomaly
        if abs(temp - moving_avg) > self.ANOMALY_THRESHOLD * moving_std:
            return True
        
        return False
       