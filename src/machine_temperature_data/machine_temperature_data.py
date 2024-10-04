import pandas as pd
import random
import numpy as np
import math

class MachineTemperatureData:
    '''
        NOISE_RANGE: the range of noise that can be added to the temperature. the bigger the value, the worse the fluctuation
        HEAT_CHANGE_COEFFICIENT: the higher the value, the faster the machine will heat up or cool down
    '''
    def __init__(self, MACHINE_MIN_TEMPERATURE, MACHINE_MAX_TEMPERATURE, NOISE_RANGE, NOISE_PROBABILITY, WORKING_FLIP_PROBABILITY, HEAT_CHANGE_COEFFICIENT):
        # Input validation
        if not isinstance(MACHINE_MIN_TEMPERATURE, (int, float)) or not isinstance(MACHINE_MAX_TEMPERATURE, (int, float)):
            raise TypeError("Temperature limits must be numbers")
        if MACHINE_MIN_TEMPERATURE >= MACHINE_MAX_TEMPERATURE:
            raise ValueError("Min temperature must be less than max temperature")
        if not isinstance(NOISE_RANGE, (int, float)) or NOISE_RANGE < 0:
            raise ValueError("Noise range must be a non-negative number")
        if not 0 <= NOISE_PROBABILITY <= 1 or not 0 <= WORKING_FLIP_PROBABILITY <= 1:
            raise ValueError("Probabilities must be between 0 and 1")
        if not isinstance(HEAT_CHANGE_COEFFICIENT, (int, float)) or HEAT_CHANGE_COEFFICIENT < 0:
            raise ValueError("Heat change coefficient must be a non-negative number")
        
        self.MACHINE_MIN_TEMPERATURE = MACHINE_MIN_TEMPERATURE
        self.MACHINE_MAX_TEMPERATURE = MACHINE_MAX_TEMPERATURE
        self.NOISE_RANGE = NOISE_RANGE
        self.NOISE_PROBABILITY = NOISE_PROBABILITY
        self.WORKING_FLIP_PROBABILITY = WORKING_FLIP_PROBABILITY
        self.HEAT_CHANGE_COEFFICIENT = HEAT_CHANGE_COEFFICIENT
        
        initial_temp = random.uniform(MACHINE_MIN_TEMPERATURE, MACHINE_MAX_TEMPERATURE)

        self.data = pd.DataFrame({
            'Temperature': [initial_temp],
            'RealTemperature': [initial_temp],
            'Noise': [0],
            'is_working': [False],
            'is_anomaly': [False]
        }, index=pd.date_range(start="2024-01-01 00:00:00", periods=1))

    
    def limitData(self, limit: int) -> None:
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")
        if limit <= 0:
            raise ValueError("limit must be a positive number")
        
        if len(self.data) > limit:
            self.data = self.data.iloc[-limit:]
    
    '''
    Used to generate the next data point.
    How: It simulates a working machine. if the machine is working, it will heat up; otherwise, it will cool down.

    '''
    def generateNextData(self):
        last_real_temp = self.data['RealTemperature'].iloc[-1]
        is_working = self.data['is_working'].iloc[-1]

        if random.random() < self.WORKING_FLIP_PROBABILITY:
            is_working = not is_working

        # Calculate real temperature change
        if is_working:
            # Heating up
            # get how long since the latest is not working, then add by 1 second
            last_working_index = self.data[self.data['is_working'] == False]
            if len(last_working_index) == 0:
                last_working_index = self.data.index[0]
            else:
                last_working_index = last_working_index.index[-1]
            time_since_last_working = self.data.index[-1] - last_working_index
            seconds_since_last_working = time_since_last_working.seconds + 1
            new_real_temp = temperature_change(last_real_temp, self.MACHINE_MAX_TEMPERATURE, self.HEAT_CHANGE_COEFFICIENT, seconds_since_last_working)
        else:
            # Cooling down
            # get how long since the latest is working, then add by 1 second
            last_not_working_index = self.data[self.data['is_working'] == True]
            if len(last_not_working_index) == 0:
                last_not_working_index = self.data.index[0]
            else:
                last_not_working_index = last_not_working_index.index[-1]
            time_since_last_not_working = self.data.index[-1] - last_not_working_index
            seconds_since_last_not_working = time_since_last_not_working.seconds + 1
            new_real_temp = temperature_change(last_real_temp, self.MACHINE_MIN_TEMPERATURE, self.HEAT_CHANGE_COEFFICIENT, seconds_since_last_not_working)

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
    
    
    def getDataLength(self):
        return len(self.data)
    
    def getLastTemperature(self, limit=1):
        # Get the last n temperature values that are not anomalies. if the number of non-anomalies is less than n,
        # return what is available
        if(limit == 1):
            return self.data['Temperature'].iloc[-1]
        if len(self.data['Temperature']) < limit:
            return self.data['Temperature']
        else:
            return self.data['Temperature'].iloc[-limit:]
        
    def getLastTemperatureThatsNotAnomaly(self, limit):
        # Get the last n temperature values that are not anomalies. if the number of non-anomalies is less than n,
        # return what is available
        non_anomalies = self.data[self.data['is_anomaly'] == False]
        if len(non_anomalies) < limit:
            return non_anomalies['Temperature']
        else:
            return non_anomalies['Temperature'].iloc[-limit:]
           
    


def temperature_change(last_real_temp, T_ambient, k, time):
    """
    Models the temperature change of a machine over time, using exponential heating or cooling.

    :param last_real_temp: The current temperature of the machine (T_0)
    :param MACHINE_MAX_TEMPERATURE: The maximum temperature the machine can reach (T_max)
    :param T_ambient: The ambient (or target) temperature the machine is heating or cooling toward
    :param k: A constant that represents the rate of heating/cooling
    :param time: The amount of time passed
    :return: The new temperature after the time interval
    """
    new_temp = T_ambient - (T_ambient - last_real_temp) * math.exp(-k * time)
    return new_temp