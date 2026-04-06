"""Terminal rendering for ai-stability."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ai_stability.models import AnalysisResult


console = Console()


def render_report(result: AnalysisResult, result_path: Path) -> None:
    """Render a clean summary and detailed outputs."""
    summary = Table(show_header=False, box=None, pad_edge=False)
    summary.add_column(style="bold cyan")
    summary.add_column()
    summary.add_row("Prompt", result.prompt_path)
    summary.add_row("Provider", result.provider)
    summary.add_row("Model", result.model)
    summary.add_row("Runs", str(result.requested_runs))
    summary.add_row("Average similarity", f"{result.average_similarity * 100:.2f}%")
    summary.add_row("Stability score", f"{result.stability_score}/100")
    summary.add_row("Stability label", result.stability_label)
    summary.add_row("Saved JSON", str(result_path))

    console.rule("[bold]Summary[/bold]")
    console.print(summary)

    similarity_table = Table(title="Pairwise Similarity", show_lines=False)
    similarity_table.add_column("Run A", justify="right")
    similarity_table.add_column("Run B", justify="right")
    similarity_table.add_column("Similarity", justify="right")
    for item in result.pairwise_similarities:
        similarity_table.add_row(str(item.run_a), str(item.run_b), f"{item.similarity * 100:.2f}%")
    console.print(similarity_table)

    console.rule("[bold]Run Outputs[/bold]")
    for run in result.runs:
        console.print(
            Panel(
                Text(run.output_text),
                title=f"Run {run.run_index}",
                border_style="green",
            )
        )

    if result.diffs:
        console.rule("[bold]Variation Diff[/bold]")
        for diff in result.diffs:
            title = f"Reference Run {diff.reference_run} vs Run {diff.compared_run}"
            console.print(
                Panel(
                    Text(diff.diff_text or "No visible differences."),
                    title=title,
                    border_style="yellow",
                )
            )
