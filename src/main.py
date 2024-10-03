import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation

from machine_temperature_data.data import MachineTemperatureData
from detector.detector import detect

# Initialize data
data = MachineTemperatureData(20, 80, 80, 0.2, 0.2)

def setupPlot():
    # Create figure and axis
    fig, ax = plt.subplots()
    
    # Set axis limits and labels
    ax.set_xlim([data.getDataIndex()[0], data.getDataIndex()[0] + pd.Timedelta(seconds=30)])
    ax.set_ylim([0, 100])
    ax.set(xlabel='Time', ylabel='Temperature [°C]')
    
    return fig, ax

fig, ax = setupPlot()

# Create initial plot elements (line and anomaly points)
line, = ax.plot(data.getDataIndex(), data.getTemperatureData(), label='Temperature over Time')
anomaly_points, = ax.plot([], [], 'ro', label='Anomaly')

ax.legend(loc="upper left")

# Function to update the plot with new data
def update(frame):
    data.generateNextData()
    
    # Limit data to 30 most recent seconds
    data.limitData(30)
    
    # Detect anomaly
    is_anomaly = detect(data)
    if is_anomaly:
        data.setLastDataAsAnomaly()

    # Update the line data with new values
    line.set_xdata(data.getDataIndex())
    line.set_ydata(data.getTemperatureData())

    # Highlight anomalies on the plot
    anomaly_points.set_xdata(data.getDataIndex()[data.getAnomalyData()])
    anomaly_points.set_ydata(data.getAnomalyData())
    
    # Dynamically adjust the x-limits as new data is added
    ax.set_xlim([data.getDataIndex()[0], data.getDataIndex()[-1] + pd.Timedelta(seconds=1)])

    # Return the updated plot elements
    return line, anomaly_points

# Set up the animation
ani = animation.FuncAnimation(fig=fig, func=update, interval=1000)

# Show the plot
plt.show()
