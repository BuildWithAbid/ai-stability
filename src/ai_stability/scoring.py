"""Stability scoring logic."""

from __future__ import annotations

import itertools
import re
from difflib import SequenceMatcher

from ai_stability.models import PairwiseSimilarity


def normalize_text(text: str) -> str:
    """Normalize whitespace for fairer text comparisons."""
    return re.sub(r"\s+", " ", text).strip()


def similarity_ratio(text_a: str, text_b: str) -> float:
    """Return a similarity ratio between 0.0 and 1.0."""
    normalized_a = normalize_text(text_a)
    normalized_b = normalize_text(text_b)
    return SequenceMatcher(None, normalized_a, normalized_b).ratio()


def compute_pairwise_similarities(outputs: list[str]) -> list[PairwiseSimilarity]:
    """Compute similarity for each output pair."""
    if len(outputs) < 2:
        raise ValueError("At least two outputs are required to score stability.")

    similarities: list[PairwiseSimilarity] = []
    indexed_outputs = list(enumerate(outputs, start=1))

    for (run_a, text_a), (run_b, text_b) in itertools.combinations(indexed_outputs, 2):
        similarities.append(
            PairwiseSimilarity(
                run_a=run_a,
                run_b=run_b,
                similarity=similarity_ratio(text_a, text_b),
            )
        )

    return similarities


def average_similarity(pairwise_scores: list[PairwiseSimilarity]) -> float:
    """Average pairwise similarity across all runs."""
    if not pairwise_scores:
        raise ValueError("Pairwise similarity scores cannot be empty.")

    total = sum(item.similarity for item in pairwise_scores)
    return total / len(pairwise_scores)


def stability_score_from_similarity(similarity: float) -> int:
    """Convert a 0-1 similarity value to a 0-100 score."""
    clamped = max(0.0, min(1.0, similarity))
    return int(round(clamped * 100))


def stability_label(score: int) -> str:
    """Map a numeric score to a stability label."""
    if score >= 80:
        return "High stability"
    if score >= 50:
        return "Medium stability"
    return "Low stability"
