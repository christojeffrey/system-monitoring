
class ThresholdDetector:
    def __init__(self, MIN, MAX):

        if not isinstance(MIN, (int, float)) or not isinstance(MAX, (int, float)):
            raise TypeError("MIN and MAX must be numbers")
        if MIN >= MAX:
            raise ValueError("MIN must be less than MAX")
        self.MIN = MIN
        self.MAX = MAX
   
    def detect(self, data):
        temp = data.getLastTemperature()
        
        # Detect if temperature is out of working range
        if temp < self.MIN or temp > self.MAX:
            return True
        
        return False