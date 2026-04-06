# ai-stability

[![Tests](https://github.com/buildwithabid/ai-stability/actions/workflows/tests.yml/badge.svg)](https://github.com/buildwithabid/ai-stability/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/ai-stability.svg)](https://pypi.org/project/ai-stability/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

`ai-stability` is a CLI-first LLM stability analyzer for developers who want to measure output consistency, detect prompt variance, and inspect unstable model behavior locally.

It runs the same prompt multiple times against the same model, compares the responses, computes a simple stability score, and saves a local JSON artifact for replay and debugging.

## Why It Exists

LLM outputs often vary even when the prompt, model, and calling code stay the same. That makes it harder to:

- evaluate prompt reliability
- spot regressions during model upgrades
- understand whether output drift is minor wording variance or meaningful behavior change
- build confidence in AI-powered developer tooling

`ai-stability` is intentionally narrow and local-first:

- one prompt file in
- repeated model calls
- simple, explicit similarity scoring
- readable terminal output
- JSON artifact saved locally for replay and debugging

## Features

- CLI-first workflow with no database, dashboard, or hosted backend
- repeated prompt execution against the same model
- explicit pairwise similarity and aggregate stability scoring
- run-by-run output review
- inline reference-vs-run diffing for fast variance inspection
- local JSON artifact saving for debugging and replay
- provider abstraction with OpenAI implemented first

## Requirements

- Python 3.11+
- An OpenAI API key in `OPENAI_API_KEY`

## Install

### Recommended for end users

```bash
pipx install ai-stability
```

### For development

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .[dev]
```

## Configure

Set your API key in the shell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

You can copy `.env.example` for reference, but the CLI reads the key from the environment.

## Quick Start

Create a prompt file:

Example `prompt.txt`:

```text
Explain the tradeoffs between unit tests and integration tests in five bullet points.
```

Run the analyzer:

```bash
ai-stability run prompt.txt --n 5 --provider openai --model gpt-4.1-mini
```

If you want to invoke it through the module instead of the installed script:

```bash
python -m ai_stability run prompt.txt --n 5 --provider openai --model gpt-4.1-mini
```

Example with a custom JSON output path:

```bash
ai-stability run prompt.txt --n 5 --provider openai --model gpt-4.1-mini --out results\sample-run.json
```

## CLI Command

```bash
ai-stability run PROMPT_FILE --n 5 --provider openai --model MODEL_NAME
```

Current options:

- `--n`: number of repeated runs, minimum `2`
- `--provider`: currently `openai`
- `--model`: target model name
- `--temperature`: sampling temperature, default `1.0`
- `--out`: optional output file or output directory for the JSON artifact

## How Scoring Works

The v1 scoring heuristic is intentionally simple and inspectable:

1. normalize whitespace in each output
2. compute pairwise text similarity with Python's `difflib.SequenceMatcher`
3. average all pairwise similarity scores
4. convert the average to a `0-100` stability score

Stability labels:

- `80-100`: High stability
- `50-79`: Medium stability
- `0-49`: Low stability

## What the CLI Prints

- summary first
- average and pairwise similarity
- final stability score and label
- each run output
- a simple reference-vs-run diff for variation review

## JSON Artifact

By default, results are written to `results/ai-stability-YYYYMMDD-HHMMSS.json`.

The JSON artifact includes:

- prompt metadata
- provider and model
- all collected outputs
- pairwise similarities
- stability score and label
- human-readable diffs

## Example Workflow

```bash
ai-stability run prompt.txt --n 5 --provider openai --model gpt-4.1-mini
```

Use this when you want to compare how stable a model is for a fixed prompt before shipping a prompt change, swapping models, or debugging flaky output behavior.

## Run Tests

```bash
python -m pytest
```

## Repository Structure

```text
src/ai_stability/
  cli.py
  runner.py
  scoring.py
  diffing.py
  output.py
  storage.py
  providers/
    base.py
    openai_provider.py
tests/
  test_scoring.py
  test_runner.py
```

## Release Process

`ai-stability` is published on PyPI:

- https://pypi.org/project/ai-stability/

Future releases are intended to be published from GitHub Actions with PyPI Trusted Publishing.

Typical release flow:

1. update the version in `pyproject.toml` and `src/ai_stability/__init__.py`
2. commit and push the release commit
3. create and push a Git tag like `v0.1.1`
4. let the `publish.yml` workflow run tests, build distributions, and upload them to PyPI automatically
5. optionally create a GitHub release for changelog and downloadable artifacts

PyPI Trusted Publishing still requires one-time configuration on PyPI for this repository before automated publishing will succeed.

Example:

```bash
git tag v0.1.1
git push origin v0.1.1
```

## Files to Review First

- `src/ai_stability/cli.py`
- `src/ai_stability/runner.py`
- `src/ai_stability/scoring.py`
- `src/ai_stability/providers/openai_provider.py`

## Roadmap Notes

- V1 runs requests sequentially on purpose.
- Only OpenAI is implemented, but the provider boundary is small and ready for Anthropic later.
- The scoring heuristic is intentionally simple and inspectable rather than statistically sophisticated.
