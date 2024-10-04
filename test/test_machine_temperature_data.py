import unittest
import pandas as pd
from src.machine_temperature_data.machine_temperature_data import MachineTemperatureData

class TestMachineTemperatureData(unittest.TestCase):
    def setUp(self):
        self.mtd = MachineTemperatureData(20, 80, 2, 0.1, 0.05, 0.025)

    def test_init(self):
        self.assertIsInstance(self.mtd.data, pd.DataFrame)
        self.assertEqual(len(self.mtd.data), 1)
        self.assertTrue(20 <= self.mtd.data['Temperature'].iloc[0] <= 80)

    def test_limit_data(self):
        for _ in range(50):
            self.mtd.generateNextData()
        self.mtd.limitData(30)
        self.assertEqual(len(self.mtd.data), 30)

    def test_limit_data_error(self):
        with self.assertRaises(TypeError):
            self.mtd.limitData("not a number")

    def test_generate_next_data(self):
        initial_len = len(self.mtd.data)
        self.mtd.generateNextData()
        self.assertEqual(len(self.mtd.data), initial_len + 1)

    def test_set_last_data_as_anomaly(self):
        self.mtd.setLastDataAsAnomaly()
        self.assertTrue(self.mtd.data['is_anomaly'].iloc[-1])

    def test_get_data_index(self):
        self.assertIsInstance(self.mtd.getDataIndex(), pd.DatetimeIndex)

    def test_get_temperature_data(self):
        self.assertIsInstance(self.mtd.getTemperatureData(), pd.Series)

    def test_get_anomaly_data(self):
        self.mtd.setLastDataAsAnomaly()
        self.assertEqual(len(self.mtd.getAnomalyDataIndex()), 1)
        self.assertEqual(len(self.mtd.getAnomalyDataTemperature()), 1)

    def test_get_last_temperature(self):
        self.assertIsInstance(self.mtd.getLastTemperature(), float)

    def test_get_data_length(self):
        self.assertEqual(self.mtd.getDataLength(), len(self.mtd.data))

    def test_get_last_temperature_thats_not_anomaly(self):
        for _ in range(10):
            self.mtd.generateNextData()
        self.mtd.setLastDataAsAnomaly()
        non_anomalies = self.mtd.getLastTemperatureThatsNotAnomaly(5)
        self.assertEqual(len(non_anomalies), 5)
        self.assertFalse(non_anomalies.index.isin(self.mtd.getAnomalyDataIndex()).any())


if __name__ == '__main__':
    unittest.main()