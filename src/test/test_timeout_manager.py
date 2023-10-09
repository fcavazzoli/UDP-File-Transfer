import unittest
from lib.TimeoutManager import TimeoutManager

class TestTimeoutManager(unittest.TestCase):

    def setUp(self):
        self.timeout_manager = TimeoutManager()

    def test_get_timeout_interval(self):
        print("Testing test_get_timeout_interval...")
        # Test when timeout_interval is less than 0.01
        print("Test when timeout_interval is less than 0.01")
        self.timeout_manager.timeout_interval = 0.001
        self.assertEqual(self.timeout_manager.get_timeout_interval(), 0.01)

        # Test when timeout_interval is between 0.01 and 1.0
        print("Test when timeout_interval is between 0.01 and 1.0")
        self.timeout_manager.timeout_interval = 0.5
        self.assertEqual(self.timeout_manager.get_timeout_interval(), 0.5)

        # Test when timeout_interval is greater than 1.0
        self.timeout_manager.timeout_interval = 2.0
        self.assertEqual(self.timeout_manager.get_timeout_interval(), 1.0)

    def test_handle_timeout_event(self):
        print("Testing test_handle_timeout_event...")
        self.timeout_manager.timeout_interval = 0.5
        self.timeout_manager.handle_timeout_event()
        self.assertEqual(self.timeout_manager.timeout_interval, 1.0)

    def test_calculate_timeout_from_now(self):
        print("Testing test_calculate_timeout_from_now...")
        # Mock the 'now' function for testing purposes
        self.timeout_manager.calculate_timeout = lambda sample_rtt: 0.5  # Mocked calculation
        self.assertAlmostEqual(self.timeout_manager.calculate_timeout_from_now(0.0), 0.5, delta=0.001)

if __name__ == '__main__':
    unittest.main()
