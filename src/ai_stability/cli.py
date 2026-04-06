"""CLI entrypoint."""

from __future__ import annotations

from pathlib import Path

import typer

from ai_stability.exceptions import AIStabilityError
from ai_stability.output import render_report
from ai_stability.runner import run_analysis


app = typer.Typer(
    add_completion=False,
    help="Analyze LLM output stability by repeating the same prompt multiple times.",
    no_args_is_help=True,
)


@app.callback()
def main_callback() -> None:
    """Root command group for ai-stability."""


@app.command()
def run(
    prompt_file: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to the prompt text file.",
    ),
    n: int = typer.Option(5, "--n", min=2, help="Number of repeated runs."),
    provider: str = typer.Option("openai", "--provider", help="Model provider to use."),
    model: str = typer.Option(..., "--model", help="Model name to call."),
    temperature: float = typer.Option(
        1.0,
        "--temperature",
        min=0.0,
        help="Sampling temperature passed to the provider.",
    ),
    out: Path | None = typer.Option(
        None,
        "--out",
        help="Optional JSON output file or directory.",
    ),
) -> None:
    """Run the same prompt repeatedly and analyze output stability."""
    try:
        result, result_path = run_analysis(
            prompt_path=prompt_file,
            run_count=n,
            provider_name=provider,
            model=model,
            temperature=temperature,
            output_path=out,
        )
    except AIStabilityError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    render_report(result, result_path)


def main() -> None:
    """Run the CLI."""
    app()


if __name__ == "__main__":
    main()
