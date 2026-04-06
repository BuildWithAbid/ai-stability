"""Utilities for surfacing output differences."""

from __future__ import annotations

from difflib import SequenceMatcher

from ai_stability.models import DiffResult


def _tokenize(text: str) -> list[str]:
    return text.split()


def build_inline_diff(reference_text: str, compared_text: str) -> str:
    """Build a compact word-level diff with inline markers."""
    reference_tokens = _tokenize(reference_text)
    compared_tokens = _tokenize(compared_text)

    matcher = SequenceMatcher(None, reference_tokens, compared_tokens)
    segments: list[str] = []

    for opcode, ref_start, ref_end, comp_start, comp_end in matcher.get_opcodes():
        ref_chunk = " ".join(reference_tokens[ref_start:ref_end]).strip()
        comp_chunk = " ".join(compared_tokens[comp_start:comp_end]).strip()

        if opcode == "equal" and comp_chunk:
            segments.append(comp_chunk)
        elif opcode == "insert" and comp_chunk:
            segments.append(f"[+ {comp_chunk} +]")
        elif opcode == "delete" and ref_chunk:
            segments.append(f"[- {ref_chunk} -]")
        elif opcode == "replace":
            if ref_chunk:
                segments.append(f"[- {ref_chunk} -]")
            if comp_chunk:
                segments.append(f"[+ {comp_chunk} +]")

    return " ".join(segment for segment in segments if segment).strip()


def build_reference_diffs(outputs: list[str], reference_run: int = 1) -> list[DiffResult]:
    """Compare each run against the selected reference output."""
    if len(outputs) < 2:
        return []

    reference_index = reference_run - 1
    reference_text = outputs[reference_index]
    diffs: list[DiffResult] = []

    for compared_run, compared_text in enumerate(outputs, start=1):
        if compared_run == reference_run:
            continue

        diffs.append(
            DiffResult(
                reference_run=reference_run,
                compared_run=compared_run,
                diff_text=build_inline_diff(reference_text, compared_text),
            )
        )

    return diffs
