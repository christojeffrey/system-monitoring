import matplotlib.pyplot as plt
import pandas as pd

import matplotlib.animation as animation


from generate import generate, initiate

df = initiate()

print(df)



fig, ax = plt.subplots()

# Set up the plot
line, = ax.plot(df.index, df['Temperature'], label='Temperature over Time')  # Initial plot line

# Set plot limits (can be adjusted)
ax.set_xlim([df.index[0], df.index[0] + pd.Timedelta(seconds=10)])  # Update x-limits as needed
ax.set_ylim([0, 100])  # Adjust y-limits as needed
ax.set(xlabel='Time', ylabel='Temperature [°C]')
ax.legend(loc="upper left")


# Function to update the plot with new data
def update(frame):
    global df
    df = generate(df)  # Generate new data and append to df
    
    # Update the line data with new df values
    line.set_xdata(df.index)  # Update x-data with the time index
    line.set_ydata(df['Temperature'])  # Update y-data with the temperature values
    

    # Keep only the last 30 data points
    if len(df) > 30:
        df = df.iloc[-30:]  # Trim the DataFrame to the last 30 rows


    # Dynamically adjust the x-limits as new data is added
    ax.set_xlim([df.index[0], df.index[-1] + pd.Timedelta(seconds=1)])  # Adjust x-limits

    # Return the updated line for the animation
    return line,


ani = animation.FuncAnimation(fig=fig, func=update, interval=1000)
plt.show()