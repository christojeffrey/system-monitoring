import unittest
from unittest.mock import Mock
from src.detector.threshold_detector import ThresholdDetector

class TestThresholdDetector(unittest.TestCase):
    def setUp(self):
        self.detector = ThresholdDetector(MIN=20.0, MAX=80.0)

    def test_init(self):
        self.assertEqual(self.detector.MIN, 20.0)
        self.assertEqual(self.detector.MAX, 80.0)

    def test_init_invalid_input(self):
        with self.assertRaises(TypeError):
            ThresholdDetector(MIN="20", MAX=80.0)
        with self.assertRaises(ValueError):
            ThresholdDetector(MIN=80.0, MAX=20.0)

    def test_detect_normal(self):
        mock_data = Mock()
        mock_data.getLastTemperature.return_value = 50.0
        
        result = self.detector.detect(mock_data)
        self.assertFalse(result)

    def test_detect_anomaly_low(self):
        mock_data = Mock()
        mock_data.getLastTemperature.return_value = 15.0
        
        result = self.detector.detect(mock_data)
        self.assertTrue(result)

    def test_detect_anomaly_high(self):
        mock_data = Mock()
        mock_data.getLastTemperature.return_value = 85.0
        
        result = self.detector.detect(mock_data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()