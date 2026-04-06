"""JSON artifact persistence."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from ai_stability.models import AnalysisResult


def default_result_path(base_dir: Path | None = None) -> Path:
    """Build a timestamped default output path."""
    root = base_dir or Path.cwd()
    output_dir = root / "results"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return output_dir / f"ai-stability-{timestamp}.json"


def resolve_output_path(output_path: Path | None) -> Path:
    """Resolve an explicit output path or generate the default one."""
    if output_path is None:
        return default_result_path()

    if output_path.exists() and output_path.is_dir():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return output_path / f"ai-stability-{timestamp}.json"

    if output_path.suffix.lower() == ".json":
        return output_path

    return output_path / f"ai-stability-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"


def save_analysis_result(result: AnalysisResult, output_path: Path) -> Path:
    """Write the JSON artifact to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
    return output_path
