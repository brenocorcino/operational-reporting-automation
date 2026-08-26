from __future__ import annotations

import unittest

from report_automation.mock_portal import REPORTS, health, home


class MockPortalTests(unittest.TestCase):
    def test_health(self) -> None:
        self.assertEqual(health(), {"status": "ok"})

    def test_home_contains_every_download_control(self) -> None:
        html = home()
        for report_name in REPORTS:
            self.assertIn(f'id="{report_name}-export"', html)


if __name__ == "__main__":
    unittest.main()
