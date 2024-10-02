import numpy as np

WORKING_RANGE_MIN = 10
WORKING_RANGE_MAX = 90
WINDOW_SIZE = 10
ANOMALY_THRESHOLD = 2.5
class AnomalyDetector:
    def __init__(self):
        self.window = []

   
    def detect(self, data):
        temp = data['Temperature'].iloc[-1]
        
        # Detect if temperature is out of working range
        if temp < WORKING_RANGE_MIN or temp > WORKING_RANGE_MAX:
            return True, "Out of working range"

        # Add the new temperature to the window
        self.window.append(temp)
        if len(self.window) > WINDOW_SIZE:
            self.window.pop(0)

        # If we don't have enough data points yet, return normal
        if len(self.window) < WINDOW_SIZE:
            return False, "Normal"

        # Calculate moving average and standard deviation
        moving_avg = np.mean(self.window)
        moving_std = np.std(self.window)

        # If the current temperature deviates significantly from the moving average,
        # consider it an anomaly
        if abs(temp - moving_avg) > ANOMALY_THRESHOLD * moving_std:
            return True, "Contextual anomaly"

        return False, "Normal"

detector = AnomalyDetector()

def detect(data):
    res =  detector.detect(data)
    if(res[0]):
        print(res)
    return res[0]