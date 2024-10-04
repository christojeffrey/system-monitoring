import numpy as np

# detect using moving average
class SuddenChangeDetector:
    # the lower the anomaly threshold, the more sensitive the detector is to sudden changes
    def __init__(self, WINDOW_SIZE, ANOMALY_THRESHOLD):
        if not isinstance(WINDOW_SIZE, int) or WINDOW_SIZE <= 0:
            raise ValueError("WINDOW_SIZE must be a positive integer")
        if not isinstance(ANOMALY_THRESHOLD, (int, float)) or ANOMALY_THRESHOLD <= 0:
            raise ValueError("ANOMALY_THRESHOLD must be a positive number")
    
        self.WINDOW_SIZE = WINDOW_SIZE
        self.ANOMALY_THRESHOLD = ANOMALY_THRESHOLD
    
    def detect(self, data):
        temp = data.getLastTemperature()
        
        window = data.getLastTemperatureThatsNotAnomaly(10)

        # Calculate moving average and standard deviation
        moving_avg = np.mean(window)
        moving_std = np.std(window)

        # If the current temperature deviates significantly from the moving average,
        # consider it an anomaly
        if abs(temp - moving_avg) > self.ANOMALY_THRESHOLD * moving_std:
            return True
        
        return False
       