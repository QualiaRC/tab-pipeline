from pathlib import Path

from tab_pipeline.core.runner import bootstrap_run


def test_bootstrap_run(tmp_path, monkeypatch) -> None:
  input_file = tmp_path / "example.wav"
  input_file.write_bytes(b"fake-audio")

  runs_dir = tmp_path / "runs"

  monkeypatch.setattr("tab_pipeline.paths.RUNS_DIR", runs_dir)
  monkeypatch.setattr("tab_pipeline.core.runner.RUNS_DIR", runs_dir)

  run_dir = bootstrap_run(input_file)

  assert run_dir.exists()
  assert (run_dir / "run.json").exists()