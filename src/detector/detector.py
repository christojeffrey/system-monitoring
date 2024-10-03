from detector.sudden_change_detector import SuddenChangeDetector
from detector.threshold_detector import ThresholdDetector 


threshold_detector = ThresholdDetector(10, 90)
sudden_change_detector = SuddenChangeDetector(10, 2)

def detect(data):
    res = threshold_detector.detect(data)
    if(res):
        print("threshold detected")
        return True
    
    res_sudden_change = sudden_change_detector.detect(data)
    if(res_sudden_change):
        print("sudden change detected")
        return True
    return False