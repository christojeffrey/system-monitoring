
class ThresholdDetector:
    def __init__(self, MIN, MAX):
        self.window = []
        self.MIN = MIN
        self.MAX = MAX

   
    def detect(self, data):
        # temp = data['Temperature'].iloc[-1]
        temp = data.getLastTemperature()
        
        # Detect if temperature is out of working range
        if temp < self.MIN or temp > self.MAX:
            return True
        
        return False