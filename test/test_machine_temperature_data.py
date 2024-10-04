import unittest
import pandas as pd
from machine_temperature_data.machine_temperature_data import MachineTemperatureData

class TestMachineTemperatureData(unittest.TestCase):
    def setUp(self):
        self.mtd = MachineTemperatureData(
            MACHINE_MIN_TEMPERATURE=20,
            MACHINE_MAX_TEMPERATURE=80,
            NOISE_RANGE=2,
            NOISE_PROBABILITY=0.1,
            WORKING_FLIP_PROBABILITY=0.05
        )

    def test_generate_next_data(self):
        initial_length = self.mtd.getDataLength()
        self.mtd.generateNextData()
        self.assertEqual(self.mtd.getDataLength(), initial_length + 1)

    def test_limit_data(self):
        for _ in range(100):
            self.mtd.generateNextData()
        self.mtd.limitData(30)
        self.assertEqual(self.mtd.getDataLength(), 30)


    def test_get_data_index(self):
        index = self.mtd.getDataIndex()
        self.assertIsInstance(index, pd.DatetimeIndex)

    def test_get_temperature_data(self):
        temp_data = self.mtd.getTemperatureData()
        self.assertIsInstance(temp_data, pd.Series)

    def test_get_last_temperature(self):
        last_temp = self.mtd.getLastTemperature()
        self.assertIsInstance(last_temp, float)
        self.assertTrue(20 <= last_temp <= 80)

if __name__ == '__main__':
    unittest.main()