from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    portal_url: str = os.getenv("PORTAL_URL", "http://127.0.0.1:8010")
    download_dir: Path = Path(os.getenv("DOWNLOAD_DIR", "downloads"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "outputs"))
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"


settings = Settings()
