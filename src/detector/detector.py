from detector.sudden_change_detector import SuddenChangeDetector
from detector.threshold_detector import ThresholdDetector 


threshold_detector = ThresholdDetector(10, 90)
sudden_change_detector = SuddenChangeDetector(10, 2.5)

def detect(data):
    res = threshold_detector.detect(data)
    if(res):
        print(res)
    return res