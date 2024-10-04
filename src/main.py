from machine_temperature_data.machine_temperature_data import MachineTemperatureData

from detector.detector import detect
from detector.sudden_change_detector import SuddenChangeDetector
from detector.threshold_detector import ThresholdDetector

from temperature_anomaly_plotter.temperature_anomaly_plotter import TemperatureAnomalyPlotter





DATA_LIMIT = 30

'''
    1. step one: setup the data and visualization
'''
# Initialize data and detectors
data = MachineTemperatureData(20, 80, 80, 0.1, 0.2)
threshold_detector = ThresholdDetector(10, 90)
sudden_change_detector = SuddenChangeDetector(WINDOW_SIZE=10, ANOMALY_THRESHOLD=2.5)

detectors = [threshold_detector, sudden_change_detector]

plotter = TemperatureAnomalyPlotter(MIN_Y_AXIS=0, MAX_Y_AXIS=100, X_RANGE=30)

def update():
    # Update the data
    data.generateNextData()

    is_anomaly = detect(data, detectors)
    if is_anomaly:
        data.setLastDataAsAnomaly()

    data.limitData(DATA_LIMIT)

    # Update the plot with the new data
    plotter.updateLineData(X=data.getDataIndex(), Y=data.getTemperatureData())
    plotter.updateAnomalyData(X=data.getAnomalyDataIndex(), Y=data.getAnomalyDataTemperature())

    plotter.adjustXAxisLimit(start=data.getDataIndex()[0])

'''
    2. show the animation which will call update function every second
'''

plotter.setupAnimation(func=update, interval=100)

plotter.show()
