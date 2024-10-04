from machine_temperature_data.machine_temperature_data import MachineTemperatureData

from detector.detector import detect
from detector.sudden_change_detector import SuddenChangeDetector
from detector.threshold_detector import ThresholdDetector

from temperature_anomaly_plotter.temperature_anomaly_plotter import TemperatureAnomalyPlotter


DATA_LIMIT = 30

MACHINE_MIN_TEMPERATURE = 20
MACHINE_MAX_TEMPERATURE = 80
NOISE_RANGE = 80
NOISE_PROBABILITY = 0.1
WORKING_FLIP_PROBABILITY = 0.2

SENSOR_MIN_TEMPERATURE = 10
SENSOR_MAX_TEMPERATURE = 90

SUDDEN_CHANGE_DETECTOR_WINDOW_SIZE = 10
SUDDEN_CHANGE_DETECTOR_ANOMALY_THRESHOLD = 2.5

PLOTTER_MIN_Y_AXIS = 0
PLOTTER_MAX_Y_AXIS = 100
PLOTTER_X_RANGE = 30

'''
    1. step one: setup the data and visualization
'''

# Initialize data and detectors
data = MachineTemperatureData(MACHINE_MIN_TEMPERATURE, MACHINE_MAX_TEMPERATURE, NOISE_RANGE, NOISE_PROBABILITY, WORKING_FLIP_PROBABILITY)
threshold_detector = ThresholdDetector(SENSOR_MIN_TEMPERATURE, SENSOR_MAX_TEMPERATURE)
sudden_change_detector = SuddenChangeDetector(SUDDEN_CHANGE_DETECTOR_WINDOW_SIZE, SUDDEN_CHANGE_DETECTOR_ANOMALY_THRESHOLD)

detectors = [threshold_detector, sudden_change_detector]

plotter = TemperatureAnomalyPlotter(PLOTTER_MIN_Y_AXIS, PLOTTER_MAX_Y_AXIS, PLOTTER_X_RANGE)

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
