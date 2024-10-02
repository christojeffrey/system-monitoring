import numpy as np
from filterpy.kalman import KalmanFilter

WORKING_RANGE_MIN = 10
WORKING_RANGE_MAX = 90

class AnomalyDetector:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=2, dim_z=1)
        self.kf.x = np.array([50., 0.])  # Initial state (position and velocity)
        self.kf.F = np.array([[1., 1.], [0., 1.]])  # State transition matrix
        self.kf.H = np.array([[1., 0.]])  # Measurement function
        self.kf.P *= 1000.  # Covariance matrix
        self.kf.R = 5  # Measurement noise
        self.kf.Q = np.array([[0.1, 0.1], [0.1, 0.1]])  # Process noise

    def detect(self, data):
        temp = data['Temperature'].iloc[-1]
        
        # Detect if temperature is out of working range
        if temp < WORKING_RANGE_MIN or temp > WORKING_RANGE_MAX:
            return True, "Out of working range"

        # Kalman filter prediction and update
        self.kf.predict()
        self.kf.update(temp)

        # Calculate the difference between predicted and actual temperature
        predicted_temp = self.kf.x[0]
        temp_diff = abs(predicted_temp - temp)

        # If the difference is more than 3 times the measurement noise, consider it an anomaly
        if temp_diff > 3 * np.sqrt(self.kf.R):
            return True, "Contextual anomaly"

        return False, "Normal"

detector = AnomalyDetector()

def detect(data):
    res =  detector.detect(data)
    if(res[0]):
        print(res)
    return res[0]