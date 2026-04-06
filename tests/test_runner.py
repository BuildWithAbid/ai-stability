import json

from ai_stability.runner import run_analysis


class FakeProvider:
    def __init__(self, outputs: list[str]) -> None:
        self._outputs = iter(outputs)

    def generate(self, prompt: str, model: str, temperature: float) -> str:
        return next(self._outputs)


def test_run_analysis_saves_artifact_and_scores(tmp_path, monkeypatch) -> None:
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("Describe software stability in one sentence.", encoding="utf-8")

    outputs = [
        "Software stability means the system behaves predictably under expected conditions.",
        "Software stability means the system behaves predictably under expected conditions.",
        "Software stability means the system behaves reliably under expected conditions.",
    ]

    monkeypatch.setattr(
        "ai_stability.runner.get_provider",
        lambda provider_name: FakeProvider(outputs),
    )

    result, saved_path = run_analysis(
        prompt_path=prompt_file,
        run_count=3,
        provider_name="openai",
        model="demo-model",
        temperature=1.0,
        output_path=tmp_path / "artifacts",
    )

    assert saved_path.exists()
    assert result.stability_score >= 80
    assert result.stability_label == "High stability"
    assert len(result.runs) == 3
    assert len(result.pairwise_similarities) == 3
    assert len(result.diffs) == 2

    artifact = json.loads(saved_path.read_text(encoding="utf-8"))
    assert artifact["model"] == "demo-model"
    assert artifact["requested_runs"] == 3
    assert artifact["result_path"] == str(saved_path)
