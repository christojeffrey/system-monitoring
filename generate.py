import pandas as pd
import random
import numpy as np

def initiate():
    return pd.DataFrame(random.random() * 100, index=pd.date_range(start="2024-01-01 00:00:00", periods=1), columns=['Temperature'])
# Generate new data using cubic spline interpolation based on the last 10 points
def generate(prev):

    input_value = (random.random() - 0.5) * 10
    # Get the last 10 values and corresponding indices

    # Generate the next time index
    last_index = prev.index[-1]
    next_value = prev['Temperature'][last_index] + input_value
    new_index = last_index + pd.Timedelta(seconds=1)

    next_value = np.clip(next_value, 0, 100)
    

    print(next_value)

    # Append the new data
    prev.loc[new_index] = next_value
    return prev
    