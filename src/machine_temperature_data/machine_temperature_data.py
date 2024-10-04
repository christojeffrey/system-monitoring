import pandas as pd
import random
import numpy as np


# why using class?
# initially I was using function, and set this up as somewhat a pipeline. As I was trying to refactor the code
# I notice that is was quite highly coupled. 
class MachineTemperatureData:
    def __init__(self, MACHINE_MIN_TEMPERATURE, MACHINE_MAX_TEMPERATURE, NOISE_RANGE, NOISE_PROBABILITY, WORKING_FLIP_PROBABILITY):
        # Input validation
        if not isinstance(MACHINE_MIN_TEMPERATURE, (int, float)) or not isinstance(MACHINE_MAX_TEMPERATURE, (int, float)):
            raise TypeError("Temperature limits must be numbers")
        if MACHINE_MIN_TEMPERATURE >= MACHINE_MAX_TEMPERATURE:
            raise ValueError("Min temperature must be less than max temperature")
        if not isinstance(NOISE_RANGE, (int, float)) or NOISE_RANGE < 0:
            raise ValueError("Noise range must be a non-negative number")
        if not 0 <= NOISE_PROBABILITY <= 1 or not 0 <= WORKING_FLIP_PROBABILITY <= 1:
            raise ValueError("Probabilities must be between 0 and 1")
        
        self.MACHINE_MIN_TEMPERATURE = MACHINE_MIN_TEMPERATURE
        self.MACHINE_MAX_TEMPERATURE = MACHINE_MAX_TEMPERATURE
        self.NOISE_RANGE = NOISE_RANGE
        self.NOISE_PROBABILITY = NOISE_PROBABILITY
        self.WORKING_FLIP_PROBABILITY = WORKING_FLIP_PROBABILITY
        
        initial_temp = random.uniform(MACHINE_MIN_TEMPERATURE, MACHINE_MAX_TEMPERATURE)

        self.data = pd.DataFrame({
            'Temperature': [initial_temp],
            'RealTemperature': [initial_temp],
            'Noise': [0],
            'is_working': [True],
            'is_anomaly': [False]
        }, index=pd.date_range(start="2024-01-01 00:00:00", periods=1))

    
    def limitData(self, limit: int) -> None:
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")
        if limit <= 0:
            raise ValueError("limit must be a positive number")
        
        if len(self.data) > limit:
            self.data = self.data.iloc[-limit:]
    
    def generateNextData(self):
        last_real_temp = self.data['RealTemperature'].iloc[-1]
        is_working = self.data['is_working'].iloc[-1]

        if random.random() < self.WORKING_FLIP_PROBABILITY:
            is_working = not is_working

        # Calculate real temperature change
        if is_working:
            # Heating up
            max_change = (self.MACHINE_MAX_TEMPERATURE - last_real_temp) / 10
            temp_change = max_change * (1 - (last_real_temp / self.MACHINE_MAX_TEMPERATURE)**2)
        else:
            # Cooling down
            max_change = (last_real_temp - self.MACHINE_MIN_TEMPERATURE) / 10
            temp_change = -max_change * (1 - ((self.MACHINE_MAX_TEMPERATURE - last_real_temp) / self.MACHINE_MAX_TEMPERATURE)**2)

        new_real_temp = np.clip(last_real_temp + temp_change, self.MACHINE_MIN_TEMPERATURE, self.MACHINE_MAX_TEMPERATURE)

        # Generate noise
        noise = 0
        if random.random() < self.NOISE_PROBABILITY:
            print("noise added")
            noise = random.uniform(-self.NOISE_RANGE, self.NOISE_RANGE)

        # Calculate observed temperature (real temperature + noise)
        new_temp = np.clip(new_real_temp + noise, self.MACHINE_MIN_TEMPERATURE, self.MACHINE_MAX_TEMPERATURE)

        # Generate the next time index
        new_index = self.data.index[-1] + pd.Timedelta(seconds=1)

        # Append the new data
        new_data = pd.DataFrame({
            'RealTemperature': [new_real_temp],
            'Noise': [noise],
            'Temperature': [new_temp],
            'is_working': [is_working],
            'is_anomaly': [False]
        }, index=[new_index])
        
        self.data = pd.concat([self.data, new_data])


    def setLastDataAsAnomaly(self):
        self.data.loc[self.data.index[-1], 'is_anomaly'] = True
    
    def getDataIndex(self):
        return self.data.index
    
    def getTemperatureData(self):
        return self.data['Temperature']

    def getAnomalyDataIndex(self):
        return self.data[self.data['is_anomaly'] == True].index
    

    def getAnomalyDataTemperature(self):
        return self.data[self.data['is_anomaly'] == True]['Temperature']
    
    def getLastTemperature(self):
        return  self.data['Temperature'].iloc[-1]
    
    def getDataLength(self):
        return len(self.data)
    

    def getLastTemperatureThatsNotAnomaly(self, limit):
        # Get the last n temperature values that are not anomalies. if the number of non-anomalies is less than n,
        # return what is available
        non_anomalies = self.data[self.data['is_anomaly'] == False]
        if len(non_anomalies) < limit:
            return non_anomalies['Temperature']
        else:
            return non_anomalies['Temperature'].iloc[-limit:]
        
        