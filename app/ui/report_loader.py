from __future__ import annotations

import argparse
from pathlib import Path

from src.app.domain.reports.service import ReportBundle, ReportService
from src.app.infrastructure.storage.report_store import ReportStore
from src.app.core.config import settings


DEFAULT_RUNS_DIR = Path(settings.REPORTS_DIR)


def parse_streamlit_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", dest="input_path")
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR))
    return parser.parse_known_args(argv)[0]


def find_latest_run_dir(base_dir: Path = DEFAULT_RUNS_DIR) -> Path:
    service = ReportService(ReportStore(base_dir))
    return service.get_latest_report().run_dir


def resolve_report_paths(
    input_path: str | Path | None = None,
    runs_dir: str | Path = DEFAULT_RUNS_DIR,
) -> tuple[Path, Path, Path | None]:
    bundle = load_report_bundle(input_path=input_path, runs_dir=runs_dir)
    return bundle.run_dir, bundle.final_report_path, bundle.aggregate_report_path


def load_report_bundle(
    input_path: str | Path | None = None,
    runs_dir: str | Path = DEFAULT_RUNS_DIR,
) -> ReportBundle:
    service = ReportService(ReportStore(runs_dir))
    if input_path is None:
        return service.get_latest_report()
    return service.get_report(input_path)
