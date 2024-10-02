import pandas as pd
import random
import numpy as np

MAX_TEMPERATURE = 100
MIN_TEMPERATURE = 0
WORKING_PROBABILITY = 0.2
NOISE_PROBABILITY = 0.1
NOISE_RANGE = 80

def initiate():
    return pd.DataFrame({
        'Temperature': [random.uniform(MIN_TEMPERATURE, MAX_TEMPERATURE)],
        'is_working': [True]
    }, index=pd.date_range(start="2024-01-01 00:00:00", periods=1))

def generate(prev):
    last_temp = prev['Temperature'].iloc[-1]
    is_working = prev['is_working'].iloc[-1]

    # Flip working state with 20% probability
    if random.random() < WORKING_PROBABILITY:
        is_working = not is_working

    # Calculate temperature change
    if is_working:
        # Heating up
        max_change = (MAX_TEMPERATURE - last_temp) / 10
        temp_change = max_change * (1 - (last_temp / MAX_TEMPERATURE)**2)
    else:
        # Cooling down
        max_change = (last_temp - MIN_TEMPERATURE) / 10
        temp_change = -max_change * (1 - ((MAX_TEMPERATURE - last_temp) / MAX_TEMPERATURE)**2)

    # Add noise with 10% probability
    if random.random() < NOISE_PROBABILITY:
        temp_change += random.uniform(-NOISE_RANGE, NOISE_RANGE)

    new_temp = np.clip(last_temp + temp_change, MIN_TEMPERATURE, MAX_TEMPERATURE)

    # Generate the next time index
    new_index = prev.index[-1] + pd.Timedelta(seconds=1)

    # Append the new data
    new_data = pd.DataFrame({
        'Temperature': [new_temp],
        'is_working': [is_working]
    }, index=[new_index])
    
    return pd.concat([prev, new_data])