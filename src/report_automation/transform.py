from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

COLLECTION_COLUMNS = {
    "report_date",
    "hub",
    "planned_packages",
    "collected_packages",
    "on_time_collections",
}
TRANSFER_COLUMNS = {
    "report_date",
    "route",
    "total_shipments",
    "on_time_shipments",
    "delayed_shipments",
    "average_delay_minutes",
}
EXCEPTION_COLUMNS = {
    "report_date",
    "hub",
    "exception_type",
    "affected_shipments",
}


@dataclass(frozen=True)
class ReportData:
    collection: pd.DataFrame
    transfer: pd.DataFrame
    exceptions: pd.DataFrame
    summary: dict[str, int | float | str]


def read_csv(path: Path, required_columns: set[str]) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = required_columns - set(frame.columns)
    if missing:
        raise ValueError(f"{path.name} is missing columns: {sorted(missing)}")
    return frame


def prepare_reports(source_dir: Path, report_date: date) -> ReportData:
    suffix = report_date.isoformat()
    collection = read_csv(source_dir / f"collection_{suffix}.csv", COLLECTION_COLUMNS)
    transfer = read_csv(source_dir / f"transfer_{suffix}.csv", TRANSFER_COLUMNS)
    exceptions = read_csv(source_dir / f"exceptions_{suffix}.csv", EXCEPTION_COLUMNS)

    for frame in (collection, transfer, exceptions):
        frame["report_date"] = pd.to_datetime(frame["report_date"]).dt.date

    collection["collection_rate"] = collection["collected_packages"] / collection[
        "planned_packages"
    ].replace(0, pd.NA)
    transfer["on_time_rate"] = transfer["on_time_shipments"] / transfer[
        "total_shipments"
    ].replace(0, pd.NA)

    planned = int(collection["planned_packages"].sum())
    collected = int(collection["collected_packages"].sum())
    total_shipments = int(transfer["total_shipments"].sum())
    on_time_shipments = int(transfer["on_time_shipments"].sum())

    summary: dict[str, int | float | str] = {
        "report_date": report_date.isoformat(),
        "planned_packages": planned,
        "collected_packages": collected,
        "collection_rate": collected / planned if planned else 0.0,
        "total_shipments": total_shipments,
        "on_time_shipments": on_time_shipments,
        "transfer_on_time_rate": (
            on_time_shipments / total_shipments if total_shipments else 0.0
        ),
        "affected_shipments": int(exceptions["affected_shipments"].sum()),
    }

    return ReportData(collection, transfer, exceptions, summary)
