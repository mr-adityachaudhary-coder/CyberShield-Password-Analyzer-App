"""
Unit & Integration Tests for CyberShield Dashboard Logic
Verifies dataset structure, dynamic metric calculations, and threat detection rules.
"""

import unittest
import pandas as pd
from app import get_initial_sample_records, calculate_metrics, analyze_security_threats

class TestCyberShieldLogic(unittest.TestCase):
    def setUp(self):
        self.df = get_initial_sample_records()

    def test_sample_records_count(self):
        """Verify exactly 20 sample records are provided as required."""
        self.assertEqual(len(self.df), 20, "Dataset must contain exactly 20 records")

    def test_sample_records_columns(self):
        """Verify all required columns are present in the dataset."""
        expected_cols = {"Timestamp", "Username", "IP Address", "Login Status", "Activity Classification"}
        self.assertTrue(expected_cols.issubset(set(self.df.columns)), f"Missing expected columns in {self.df.columns}")

    def test_metric_calculations(self):
        """Verify all statistics are calculated automatically and correctly."""
        metrics = calculate_metrics(self.df)
        
        self.assertEqual(metrics["total_logins"], 20)
        self.assertEqual(metrics["successful_logins"], (self.df["Login Status"] == "Success").sum())
        self.assertEqual(metrics["failed_logins"], (self.df["Login Status"] == "Failed").sum())
        self.assertEqual(metrics["suspicious_activities"], (self.df["Activity Classification"] == "Suspicious").sum())
        self.assertAlmostEqual(metrics["successful_logins"] + metrics["failed_logins"], metrics["total_logins"])
        
        expected_rate = round((metrics["successful_logins"] / 20) * 100, 1)
        self.assertEqual(metrics["success_rate"], expected_rate)

    def test_empty_dataframe_handling(self):
        """Verify metrics and detection handle empty dataframes gracefully."""
        empty_df = pd.DataFrame(columns=self.df.columns)
        metrics = calculate_metrics(empty_df)
        threats = analyze_security_threats(empty_df)
        
        self.assertEqual(metrics["total_logins"], 0)
        self.assertEqual(metrics["successful_logins"], 0)
        self.assertEqual(metrics["failed_logins"], 0)
        self.assertEqual(metrics["suspicious_activities"], 0)
        self.assertEqual(metrics["success_rate"], 0.0)
        self.assertEqual(threats, [])

    def test_threat_detection_brute_force(self):
        """Verify Rule 1 flags repeated failed logins (e.g. user 'admin')."""
        threats = analyze_security_threats(self.df)
        self.assertTrue(len(threats) > 0, "Threats should be detected in baseline dataset")
        
        # Check if user 'admin' is flagged for repeated failed logins
        admin_threats = [t for t in threats if t["user"] == "admin" and "Repeated Failed Logins" in t["title"]]
        self.assertTrue(len(admin_threats) > 0, "User 'admin' should trigger Rule 1 (Repeated Failed Logins)")
        self.assertEqual(admin_threats[0]["severity"], "High")

    def test_threat_detection_explicit_suspicious(self):
        """Verify Rule 2 flags explicitly suspicious records (e.g. finance_mgr, root_service)."""
        threats = analyze_security_threats(self.df)
        users_in_threats = {t["user"] for t in threats}
        self.assertIn("finance_mgr", users_in_threats)
        self.assertIn("guest_user", users_in_threats)
        self.assertIn("root_service", users_in_threats)

    def test_filtering_logic(self):
        """Verify search and status filtering logic."""
        # Filter by Status == 'Success'
        success_df = self.df[self.df["Login Status"] == "Success"]
        self.assertEqual(len(success_df), 13)

        # Filter by Status == 'Failed'
        failed_df = self.df[self.df["Login Status"] == "Failed"]
        self.assertEqual(len(failed_df), 7)

        # Filter by Classification == 'Suspicious'
        suspicious_df = self.df[self.df["Activity Classification"] == "Suspicious"]
        self.assertEqual(len(suspicious_df), 6)

        # Search by username 'alex.ops'
        alex_df = self.df[self.df["Username"].str.lower().str.contains("alex.ops")]
        self.assertEqual(len(alex_df), 3)

if __name__ == "__main__":
    unittest.main()