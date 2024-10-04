we have two detector
threshold detector, and sudden change detector

# threshold detector

this detector will simply detect anomaly when the **value is above or below the threshold**.
this simulates the working temperature range of the machine. If the temperature goes above or below, it will be considered as anomaly (it might mean that the machine is broken, or the sensor is broken)

# sudden change detector

this simulates the working condition of the machine. the temperature should heat up or cool down gradually.
if the value changed to rapidly, it will be considered as anomaly.

the data that is checked is a **time series data** that is produced somewhat randomly (**no pattern** every minute, or everyday, etc).
to handle this kind of data, **Moving Average** is used.

---

## note

that the configuration of the detector is set according to the data that is being consumed. so if the configuration of the data is change, the configuration of the detector should be changed as well to maintain the accuracy of the detector.

## effectiveness

1. the threshold is basically perfect. it will detect the anomaly 100% of the time.

2. the sudden change detector has some limitation.
if the last previous data is particularly littered with noise, it will have a hard time to detect the anomaly.

    but it's very **robust**: 
   - doesn't matter if the temperature is going up or down, as long as it's in the same ballpark as the last few data, it will be considered as normal.
   - doesn't matter if the temperature is high or low, as long as it's in the same ballpack as the last few data, it will be considered as normal.

1. both detector is **cheap on compute**, both has constant time complexity O(1) and space complexity O(1) for each data point.


4. the **noise that is produced need to differ significantly** from the normal data. if the noise is too close to the normal data, the detector will have a hard time to detect the anomaly.
