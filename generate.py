import pandas as pd
import random
import numpy as np

def initiate():
    return pd.DataFrame({'Temperature': [random.random() * 100]}, index=pd.date_range(start="2024-01-01 00:00:00", periods=1))

def generate(prev):
    input_value = (random.random() - 0.5) * 10

    # Generate the next time index
    last_index = prev.index[-1]
    next_value = prev['Temperature'].iloc[-1] + input_value
    new_index = last_index + pd.Timedelta(seconds=1)

    next_value = np.clip(next_value, 0, 100)
    
    # Append the new data
    new_data = pd.DataFrame({'Temperature': [next_value]}, index=[new_index])
    return pd.concat([prev, new_data])