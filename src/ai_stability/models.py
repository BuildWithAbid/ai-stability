"""Typed models used throughout the project."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class RunResult:
    """One provider execution for a repeated prompt."""

    run_index: int
    output_text: str


@dataclass(slots=True)
class PairwiseSimilarity:
    """Similarity score between two outputs."""

    run_a: int
    run_b: int
    similarity: float


@dataclass(slots=True)
class DiffResult:
    """Human-readable diff against the reference output."""

    reference_run: int
    compared_run: int
    diff_text: str


@dataclass(slots=True)
class AnalysisResult:
    """Saved artifact for one ai-stability execution."""

    created_at: str
    prompt_path: str
    prompt_text: str
    provider: str
    model: str
    temperature: float
    requested_runs: int
    runs: list[RunResult]
    pairwise_similarities: list[PairwiseSimilarity]
    average_similarity: float
    stability_score: int
    stability_label: str
    diffs: list[DiffResult]
    result_path: str

    def to_dict(self) -> dict[str, Any]:
        """Convert the artifact to a JSON-safe dictionary."""
        return asdict(self)

    @property
    def prompt_file(self) -> Path:
        """Return the prompt path as a Path."""
        return Path(self.prompt_path)
