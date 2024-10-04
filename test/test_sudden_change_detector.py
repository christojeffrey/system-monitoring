import unittest
from unittest.mock import Mock
from src.detector.sudden_change_detector import SuddenChangeDetector

class TestSuddenChangeDetector(unittest.TestCase):
    def setUp(self):
        self.detector = SuddenChangeDetector(WINDOW_SIZE=10, ANOMALY_THRESHOLD=2.0)

    def test_init(self):
        self.assertEqual(self.detector.WINDOW_SIZE, 10)
        self.assertEqual(self.detector.ANOMALY_THRESHOLD, 2.0)

    def test_init_invalid_input(self):
        with self.assertRaises(ValueError):
            SuddenChangeDetector(WINDOW_SIZE=0, ANOMALY_THRESHOLD=2.0)
        with self.assertRaises(ValueError):
            SuddenChangeDetector(WINDOW_SIZE=10, ANOMALY_THRESHOLD=-1)

    def test_detect_normal(self):
        mock_data = Mock()
        mock_data.getLastTemperature.return_value = 25.0
        mock_data.getLastTemperatureThatsNotAnomaly.return_value = [24.5, 24.8, 25.2, 25.0, 24.7, 25.1, 24.9, 25.3, 24.6, 25.2]
        
        result = self.detector.detect(mock_data)
        self.assertFalse(result)

    def test_detect_anomaly(self):
        mock_data = Mock()
        mock_data.getLastTemperature.side_effect = [30.0,[24.5, 24.8, 25.2, 25.0, 24.7, 25.1, 24.9, 25.3, 24.6, 25.2]]
        
        result = self.detector.detect(mock_data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()