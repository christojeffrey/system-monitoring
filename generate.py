import pandas as pd
import random
from scipy.interpolate import CubicSpline
import numpy as np

def initiate():
    return pd.DataFrame(random.random() * 100, index=pd.date_range(start="2024-01-01 00:00:00", periods=1), columns=['Temperature'])
# Generate new data using cubic spline interpolation based on the last 10 points
def generate(prev):

    input_value = (random.random() - 0.5) * 10
    # Get the last 10 values and corresponding indices
    if len(prev) >= 10:
        last_10_indices = np.arange(10)
        last_10_values = prev['Temperature'].iloc[-10:].values
    else:
        new_index = prev.index[-1] + pd.Timedelta(seconds=1)
        prev.loc[new_index] = random.random() * 100
        return prev

    # Create cubic spline based on the last 10 values
    cubic_spline = CubicSpline(last_10_indices, last_10_values, bc_type='natural')

    # Generate the next time index
    last_index = prev.index[-1]
    new_index = last_index + pd.Timedelta(seconds=1)
    
    # Calculate next temperature value using the cubic spline
    next_value = cubic_spline(len(last_10_indices))

    last_slope = cubic_spline.derivative()(len(last_10_indices) - 1)  # Derivative at the last valid point (index 9)
    next_value += input_value * last_slope * 0.01  # Scale the effect of the slope adjustment
    next_value = np.clip(next_value, 0, 100)

    print(next_value)

    # Append the new data
    prev.loc[new_index] = next_value
    return prev
    