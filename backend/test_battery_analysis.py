import unittest

from battery_analysis import analyze_battery, control_actuators


class BatteryAnalysisTests(unittest.TestCase):
    def test_normal_state(self):
        result = analyze_battery([4.10, 4.11, 4.09, 4.10], 2.0, [30, 31, 30, 31])
        self.assertEqual(result.battery_status, "NORMAL")
        self.assertEqual(control_actuators(result)["relay"], "ON")

    def test_warning_imbalance(self):
        result = analyze_battery([4.10, 4.11, 4.00, 4.10], 2.0, [30, 31, 30, 31])
        self.assertEqual(result.imbalance_status, "WARNING")
        self.assertEqual(result.battery_status, "WARNING")

    def test_critical_imbalance(self):
        result = analyze_battery([4.10, 4.11, 3.80, 4.10], 2.0, [30, 31, 30, 31])
        self.assertEqual(result.battery_status, "CRITICAL")
        self.assertEqual(control_actuators(result)["relay"], "OFF")


if __name__ == "__main__":
    unittest.main()
