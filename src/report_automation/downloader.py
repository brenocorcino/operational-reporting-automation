from __future__ import annotations

from datetime import date
from pathlib import Path

from playwright.sync_api import sync_playwright

REPORT_NAMES = ("collection", "transfer", "exceptions")


def download_reports(
    portal_url: str,
    report_date: date,
    download_dir: Path,
    *,
    headless: bool = True,
) -> list[Path]:
    destination = download_dir / report_date.isoformat()
    destination.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_page(accept_downloads=True)
        page.goto(portal_url, wait_until="networkidle")
        page.locator("#report-date").fill(report_date.isoformat())
        page.locator("#report-date").dispatch_event("change")

        for report_name in REPORT_NAMES:
            with page.expect_download() as download_info:
                page.locator(f"#{report_name}-export").click()
            target = destination / f"{report_name}_{report_date.isoformat()}.csv"
            download_info.value.save_as(target)
            downloaded.append(target)

        browser.close()

    return downloaded
