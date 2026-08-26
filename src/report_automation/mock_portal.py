from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(
    title="Synthetic Operations Portal",
    description="A safe local portal used to demonstrate browser automation.",
    version="1.0.0",
)

SOURCE_DIR = Path(__file__).resolve().parents[2] / "data" / "source"
REPORTS = {
    "collection": "collection_performance.csv",
    "transfer": "transfer_performance.csv",
    "exceptions": "scan_exceptions.csv",
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    links = "".join(
        f'<a id="{name}-export" data-report="{name}" '
        f'href="/exports/{name}.csv?report_date=2026-08-25">'
        f"Download {name}</a>"
        for name in REPORTS
    )
    return f"""
    <!doctype html>
    <html lang="en">
      <head><meta charset="utf-8"><title>Synthetic Operations Portal</title></head>
      <body>
        <h1>Operational reports</h1>
        <label for="report-date">Report date</label>
        <input id="report-date" type="date" value="2026-08-25">
        <div>{links}</div>
        <script>
          const input = document.getElementById('report-date');
          input.addEventListener('change', () => {{
            document.querySelectorAll('[data-report]').forEach((link) => {{
              link.href = `/exports/${{link.dataset.report}}.csv?report_date=${{input.value}}`;
            }});
          }});
        </script>
      </body>
    </html>
    """


@app.get("/exports/{report_name}.csv")
def export_report(
    report_name: str,
    report_date: Annotated[date, Query()],
) -> FileResponse:
    filename = REPORTS.get(report_name)
    if filename is None:
        raise HTTPException(status_code=404, detail="unknown report")
    source = SOURCE_DIR / filename
    return FileResponse(
        source,
        media_type="text/csv",
        filename=f"{report_name}_{report_date.isoformat()}.csv",
    )
