"""Execution flow for ai-stability."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ai_stability.diffing import build_reference_diffs
from ai_stability.exceptions import PromptError
from ai_stability.models import AnalysisResult, RunResult
from ai_stability.providers import get_provider
from ai_stability.scoring import (
    average_similarity,
    compute_pairwise_similarities,
    stability_label,
    stability_score_from_similarity,
)
from ai_stability.storage import resolve_output_path, save_analysis_result


def load_prompt(prompt_path: Path) -> str:
    """Load prompt text from a file."""
    try:
        prompt_text = prompt_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise PromptError(f"Could not read prompt file '{prompt_path}': {exc}") from exc

    if not prompt_text:
        raise PromptError("Prompt file is empty.")
    return prompt_text


def run_analysis(
    prompt_path: Path,
    run_count: int,
    provider_name: str,
    model: str,
    temperature: float,
    output_path: Path | None = None,
) -> tuple[AnalysisResult, Path]:
    """Execute repeated runs and persist the resulting artifact."""
    prompt_text = load_prompt(prompt_path)
    provider = get_provider(provider_name)

    run_results: list[RunResult] = []
    for run_index in range(1, run_count + 1):
        output_text = provider.generate(prompt_text, model=model, temperature=temperature)
        run_results.append(RunResult(run_index=run_index, output_text=output_text))

    outputs = [item.output_text for item in run_results]
    pairwise_scores = compute_pairwise_similarities(outputs)
    avg_similarity = average_similarity(pairwise_scores)
    score = stability_score_from_similarity(avg_similarity)
    diffs = build_reference_diffs(outputs, reference_run=1)

    resolved_output_path = resolve_output_path(output_path)
    result = AnalysisResult(
        created_at=datetime.now(timezone.utc).isoformat(),
        prompt_path=str(prompt_path),
        prompt_text=prompt_text,
        provider=provider_name,
        model=model,
        temperature=temperature,
        requested_runs=run_count,
        runs=run_results,
        pairwise_similarities=pairwise_scores,
        average_similarity=avg_similarity,
        stability_score=score,
        stability_label=stability_label(score),
        diffs=diffs,
        result_path=str(resolved_output_path),
    )

    saved_path = save_analysis_result(result, resolved_output_path)
    return result, saved_path
