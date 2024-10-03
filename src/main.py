import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation
from machine_temperature_data.data import MachineTemperatureData
from detector.detector import detect

# Initialize data
data = MachineTemperatureData(20, 80, 80, 0.1, 0.2)

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

    # Check if the latest data point is an anomaly
       # Detect anomaly
    is_anomaly = detect(data)
    if is_anomaly:
        data.setLastDataAsAnomaly()

    df = data.data

    data.limitData(30)
    

      # Update the line data with new values
    line.set_xdata(data.getDataIndex())
    line.set_ydata(data.getTemperatureData())

    # Highlight anomalies on the plot
    anomaly_points.set_xdata(data.getAnomalyDataIndex())
    anomaly_points.set_ydata(data.getAnomalyDataTemperature())
    
    # Dynamically adjust the x-limits as new data is added
    ax.set_xlim([data.getDataIndex()[0], data.getDataIndex()[-1] + pd.Timedelta(seconds=1)])


    # Return the updated line for the animation
    return line, anomaly_points

ani = animation.FuncAnimation(fig=fig, func=update, interval=100)
plt.show()