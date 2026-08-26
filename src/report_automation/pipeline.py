from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .config import settings
from .downloader import download_reports
from .transform import prepare_reports
from .workbook import build_workbook


def run(report_date: date, *, skip_download: bool = False) -> Path:
    source_dir = settings.download_dir / report_date.isoformat()
    if not skip_download:
        download_reports(
            settings.portal_url,
            report_date,
            settings.download_dir,
            headless=settings.headless,
        )

    data = prepare_reports(source_dir, report_date)
    output = settings.output_dir / f"operational_report_{report_date.isoformat()}.xlsx"
    return build_workbook(data, output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automate operational reports")
    parser.add_argument("--date", required=True, type=date.fromisoformat)
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Reuse files already present in the date download directory",
    )
    args = parser.parse_args()
    output = run(args.date, skip_download=args.skip_download)
    print(f"Report created: {output.resolve()}")


if __name__ == "__main__":
    main()
