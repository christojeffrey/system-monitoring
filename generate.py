import pandas as pd
import random
import numpy as np

MAX_TEMPERATURE = 100
MIN_TEMPERATURE = 0
WORKING_PROBABILITY = 0.2
NOISE_PROBABILITY = 0.1
NOISE_RANGE = 80

def initiate():
    initial_temp = random.uniform(MIN_TEMPERATURE, MAX_TEMPERATURE)
    return pd.DataFrame({
        'RealTemperature': [initial_temp],
        'Noise': [0],
        'Temperature': [initial_temp],
        'is_working': [True]
    }, index=pd.date_range(start="2024-01-01 00:00:00", periods=1))

def generate(prev):
    last_real_temp = prev['RealTemperature'].iloc[-1]
    is_working = prev['is_working'].iloc[-1]

    # Flip working state with 20% probability
    if random.random() < WORKING_PROBABILITY:
        is_working = not is_working

    # Calculate real temperature change
    if is_working:
        # Heating up
        max_change = (MAX_TEMPERATURE - last_real_temp) / 10
        temp_change = max_change * (1 - (last_real_temp / MAX_TEMPERATURE)**2)
    else:
        # Cooling down
        max_change = (last_real_temp - MIN_TEMPERATURE) / 10
        temp_change = -max_change * (1 - ((MAX_TEMPERATURE - last_real_temp) / MAX_TEMPERATURE)**2)

    new_real_temp = np.clip(last_real_temp + temp_change, MIN_TEMPERATURE, MAX_TEMPERATURE)

    # Generate noise
    noise = 0
    if random.random() < NOISE_PROBABILITY:
        print("noise added")
        noise = random.uniform(-NOISE_RANGE, NOISE_RANGE)

    # Calculate observed temperature (real temperature + noise)
    new_temp = np.clip(new_real_temp + noise, MIN_TEMPERATURE, MAX_TEMPERATURE)

    # Generate the next time index
    new_index = prev.index[-1] + pd.Timedelta(seconds=1)

    # Append the new data
    new_data = pd.DataFrame({
        'RealTemperature': [new_real_temp],
        'Noise': [noise],
        'Temperature': [new_temp],
        'is_working': [is_working]
    }, index=[new_index])
    
    return pd.concat([prev, new_data])