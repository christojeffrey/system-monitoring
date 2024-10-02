# this file mostly handle the visualization


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation

from generate import generate, initiate
from detect import detect

df = initiate()

fig, ax = plt.subplots()

# Set up the plot
line, = ax.plot(df.index, df['Temperature'], label='Temperature over Time')
anomaly_points, = ax.plot([], [], 'ro', label='Anomaly')

ax.set_xlim([df.index[0], df.index[0] + pd.Timedelta(seconds=30)])
ax.set_ylim([0, 100])
ax.set(xlabel='Time', ylabel='Temperature [°C]')
ax.legend(loc="upper left")

# Function to update the plot with new data
def update(frame):
    global df
    df = generate(df)

    # Check if the latest data point is an anomaly
    is_anomaly = detect(df)
    
    # If anomaly, update the way the data looks
    df.loc[df.index[-1], 'is_anomaly'] = is_anomaly

    # Update the line data with new df values
    line.set_xdata(df.index)
    line.set_ydata(df['Temperature'])

    # Keep only the last 30 data points
    if len(df) > 30:
        df = df.iloc[-30:]

    # Highlight anomalies on the plot
    anomaly_data = df[df['is_anomaly'] == True]
    anomaly_points.set_xdata(anomaly_data.index)
    anomaly_points.set_ydata(anomaly_data['Temperature'])
    
    # Dynamically adjust the x-limits as new data is added
    ax.set_xlim([df.index[0], df.index[-1] + pd.Timedelta(seconds=1)])

    # Return the updated line for the animation
    return line, anomaly_points

ani = animation.FuncAnimation(fig=fig, func=update, interval=1000)
plt.show()