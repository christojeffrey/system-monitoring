import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.temperature_anomaly_plotter.temperature_anomaly_plotter import TemperatureAnomalyPlotter

class TestTemperatureAnomalyPlotter(unittest.TestCase):
    def setUp(self):
        self.plotter = TemperatureAnomalyPlotter(MIN_Y_AXIS=0, MAX_Y_AXIS=100, X_RANGE=60)

    def test_init(self):
        self.assertEqual(self.plotter.MIN_Y_AXIS, 0)
        self.assertEqual(self.plotter.MAX_Y_AXIS, 100)
        self.assertEqual(self.plotter.X_RANGE, 60)

    def test_init_invalid_input(self):
        with self.assertRaises(TypeError):
            TemperatureAnomalyPlotter(MIN_Y_AXIS="0", MAX_Y_AXIS=100, X_RANGE=60)
        with self.assertRaises(ValueError):
            TemperatureAnomalyPlotter(MIN_Y_AXIS=100, MAX_Y_AXIS=0, X_RANGE=60)
        with self.assertRaises(ValueError):
            TemperatureAnomalyPlotter(MIN_Y_AXIS=0, MAX_Y_AXIS=100, X_RANGE=-60)

    def test_update_line_data(self):
        X = [1, 2, 3]
        Y = [10, 20, 30]
        self.plotter.updateLineData(X, Y)
        self.assertEqual(list(self.plotter.line.get_xdata()), X)
        self.assertEqual(list(self.plotter.line.get_ydata()), Y)


    def test_update_anomaly_data(self):
        X = [1, 2, 3]
        Y = [10, 20, 30]
        self.plotter.updateAnomalyData(X, Y)
        self.assertEqual(list(self.plotter.anomaly_points.get_xdata()), X)
        self.assertEqual(list(self.plotter.anomaly_points.get_ydata()), Y)

    def test_adjust_x_axis_limit_invalid_input(self):
        with self.assertRaises(TypeError):
            self.plotter.adjustXAxisLimit("2024-01-01 00:00:00")

    @patch('matplotlib.animation.FuncAnimation')
    def test_setup_animation(self, mock_func_animation):
        mock_func = MagicMock()
        self.plotter.setupAnimation(mock_func, 1000)
        mock_func_animation.assert_called_once()

if __name__ == '__main__':
    unittest.main()