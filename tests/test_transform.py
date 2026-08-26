from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from report_automation.transform import prepare_reports, read_csv


class TransformTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.source = Path(self.temp.name)
        suffix = "2026-08-25"
        (self.source / f"collection_{suffix}.csv").write_text(
            "report_date,hub,planned_packages,collected_packages,on_time_collections\n"
            "2026-08-25,SP-01,100,95,90\n"
            "2026-08-25,RJ-01,200,180,170\n",
            encoding="utf-8",
        )
        (self.source / f"transfer_{suffix}.csv").write_text(
            "report_date,route,total_shipments,on_time_shipments,delayed_shipments,average_delay_minutes\n"
            "2026-08-25,SP-01>RJ-01,100,80,20,45\n",
            encoding="utf-8",
        )
        (self.source / f"exceptions_{suffix}.csv").write_text(
            "report_date,hub,exception_type,affected_shipments\n"
            "2026-08-25,SP-01,missing_dispatch_scan,7\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_calculates_weighted_summary_rates(self) -> None:
        data = prepare_reports(self.source, date(2026, 8, 25))

        self.assertEqual(data.summary["planned_packages"], 300)
        self.assertEqual(data.summary["collected_packages"], 275)
        self.assertAlmostEqual(data.summary["collection_rate"], 275 / 300)
        self.assertEqual(data.summary["affected_shipments"], 7)
        self.assertAlmostEqual(data.summary["transfer_on_time_rate"], 0.8)

    def test_adds_row_level_rates(self) -> None:
        data = prepare_reports(self.source, date(2026, 8, 25))

        self.assertAlmostEqual(data.collection.iloc[0]["collection_rate"], 0.95)
        self.assertAlmostEqual(data.transfer.iloc[0]["on_time_rate"], 0.8)

    def test_reports_missing_columns(self) -> None:
        invalid = self.source / "invalid.csv"
        invalid.write_text("hub,value\nSP-01,1\n", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "missing columns"):
            read_csv(invalid, {"hub", "report_date"})


if __name__ == "__main__":
    unittest.main()
