# Contributing

Thanks for contributing to `ai-stability`.

## Development Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .[dev]
```

Run tests before opening a pull request:

```bash
python -m pytest
```

## Development Guidelines

- Keep the project CLI-first and local-first.
- Prefer small, explicit modules over large abstractions.
- Do not add platform features, databases, dashboards, or background services.
- Keep scoring logic inspectable and easy to reason about.
- Preserve the current user-facing command contract unless there is a strong reason to change it.

## Pull Request Checklist

- Added or updated tests for behavior changes when appropriate.
- Verified `python -m pytest` passes locally.
- Updated README, changelog, or release notes when user-facing behavior changed.
- Kept the change scoped to the CLI workflow and core stability analysis path.

## Release Checklist

1. Update the version in `pyproject.toml` and `src/ai_stability/__init__.py`.
2. Update `CHANGELOG.md`.
3. Run:
   ```bash
   python -m pytest
   python -m build
   python -m twine check --strict dist/*
   ```
4. Commit and push the release commit to `main`.
5. Create and push a version tag:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
6. Confirm the `Publish to PyPI` workflow succeeds.
7. Verify the matching GitHub release and PyPI release page.
8. Advance `main` to the next development version.

## Reporting Issues

Use the GitHub issue templates for bug reports and feature requests. Include the model, provider, CLI command, and a minimal prompt sample whenever possible.
