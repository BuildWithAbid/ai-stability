# Launch Kit

## One-line pitch

`ai-stability` is a Python CLI that runs the same prompt multiple times, scores LLM output consistency, and shows where responses vary.

## Short post

I shipped `ai-stability`, a CLI-first tool for measuring how stable an LLM is on the same prompt.

- install: `pipx install ai-stability`
- GitHub: https://github.com/BuildWithAbid/ai-stability
- PyPI: https://pypi.org/project/ai-stability/

Useful for prompt testing, model comparison, and debugging flaky AI behavior.

## X / Twitter post

Shipped `ai-stability` today.

A small Python CLI that runs the same prompt multiple times, compares the outputs, scores consistency, and shows diffs.

Useful for prompt testing and debugging flaky LLM behavior.

`pipx install ai-stability`

GitHub: https://github.com/BuildWithAbid/ai-stability
PyPI: https://pypi.org/project/ai-stability/

## LinkedIn post

I built `ai-stability`, a CLI-first Python tool for checking how stable an LLM is on repeated runs of the same prompt.

The tool:

- runs the same prompt multiple times
- compares response similarity
- assigns a simple stability score
- highlights where outputs drift
- saves a local JSON artifact for replay and debugging

This is useful when you are testing prompts, comparing model behavior, or trying to understand whether “randomness” is minor wording noise or real behavior variance.

Install:

`pipx install ai-stability`

Project:

- GitHub: https://github.com/BuildWithAbid/ai-stability
- PyPI: https://pypi.org/project/ai-stability/

## Show HN

### Title

Show HN: ai-stability – CLI tool to measure LLM output stability

### Body

I built a small Python CLI called `ai-stability`.

It runs the same prompt multiple times against the same model, compares the outputs, computes a simple stability score, shows diffs between runs, and saves a local JSON artifact.

It is aimed at developers testing prompts, comparing model behavior, or debugging unstable AI output.

Install:

`pipx install ai-stability`

Repo:

https://github.com/BuildWithAbid/ai-stability

PyPI:

https://pypi.org/project/ai-stability/
