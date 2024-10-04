import matplotlib.pyplot as plt
import matplotlib.animation as animation


import pandas as pd
class TemperatureAnomalyPlotter:
    def __init__(self, MIN_Y_AXIS, MAX_Y_AXIS, X_RANGE):
        self.MIN_Y_AXIS = MIN_Y_AXIS
        self.MAX_Y_AXIS = MAX_Y_AXIS
        self.X_RANGE = X_RANGE

        # Create figure and axis
        fig, ax = plt.subplots()
        
        self.figure = fig
        self.axis = ax
        
        # Set axis limits and labels
        # ax.set_xlim([data.getDataIndex()[0], data.getDataIndex()[0] + pd.Timedelta(seconds=DATA_LIMIT)])
        ax.set_ylim([MIN_Y_AXIS, MAX_Y_AXIS])
        ax.set(xlabel='Time', ylabel='Temperature [°C]')


        # Create initial plot elements (line and anomaly points)
        line, = ax.plot([], [], label='Temperature over Time')
        self.line = line
        anomaly_points, = ax.plot([], [], 'ro', label='Anomaly')

        self.anomaly_points = anomaly_points

        ax.legend(loc="upper left")
    def updateLineData(self, X, Y):
        self.line.set_xdata(X)
        self.line.set_ydata(Y)

    def updateAnomalyData(self, X, Y):
        self.anomaly_points.set_xdata(X)
        self.anomaly_points.set_ydata(Y)

    def adjustXAxisLimit(self, start):
        self.axis.set_xlim([start, start + pd.Timedelta(seconds=self.X_RANGE)])


    def setupAnimation(self, func, interval):

        def updateFunction(frame):
            func()
            return self.line, self.anomaly_points
        
        self.ani = animation.FuncAnimation(fig=self.figure, func=updateFunction, interval=interval)


    def show(self):
        plt.show()