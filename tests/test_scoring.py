from ai_stability.scoring import (
    average_similarity,
    compute_pairwise_similarities,
    normalize_text,
    similarity_ratio,
    stability_label,
    stability_score_from_similarity,
)


def test_identical_outputs_score_100() -> None:
    outputs = ["same answer", "same answer", "same answer"]
    pairwise = compute_pairwise_similarities(outputs)
    average = average_similarity(pairwise)
    score = stability_score_from_similarity(average)
    assert score == 100
    assert stability_label(score) == "High stability"


def test_whitespace_normalization_preserves_similarity() -> None:
    assert normalize_text("hello   world\n\nagain") == "hello world again"
    assert similarity_ratio("hello   world", "hello world") == 1.0


def test_different_outputs_score_low() -> None:
    outputs = ["alpha beta gamma", "completely unrelated answer", "42"]
    pairwise = compute_pairwise_similarities(outputs)
    average = average_similarity(pairwise)
    score = stability_score_from_similarity(average)
    assert score < 50
    assert stability_label(score) == "Low stability"


def test_small_variations_land_in_middle_band() -> None:
    outputs = [
        "The system is stable under moderate load.",
        "The system remains stable under moderate load.",
        "The system is stable under most moderate load.",
    ]
    pairwise = compute_pairwise_similarities(outputs)
    average = average_similarity(pairwise)
    score = stability_score_from_similarity(average)
    assert 50 <= score <= 99


def test_label_thresholds() -> None:
    assert stability_label(49) == "Low stability"
    assert stability_label(50) == "Medium stability"
    assert stability_label(79) == "Medium stability"
    assert stability_label(80) == "High stability"
