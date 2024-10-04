
from typing import List
from machine_temperature_data.data import MachineTemperatureData



# makeshift interface
class Detector:
    def detect(self, data: MachineTemperatureData) -> bool:
        pass


def detect(data: MachineTemperatureData, detectors : List[Detector]) -> bool:
    for detector in detectors:
        res = detector.detect(data)
        if(res):
            print("detector:", detector)
            return True
    
    return False