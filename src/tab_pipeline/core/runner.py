from datetime import datetime, UTC
from pathlib import Path

from tab_pipeline.core.manifest import write_manifest
from tab_pipeline.models.run import RunManifest
from tab_pipeline.paths import RUNS_DIR, ensure_directories


def _build_run_id() -> str:
  timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
  return timestamp


def bootstrap_run(input_path: Path) -> Path:
  if not input_path.exists():
    raise FileNotFoundError(f"Input file does not exist: {input_path}")

  ensure_directories()

  run_id = _build_run_id()
  run_dir = RUNS_DIR / run_id
  run_dir.mkdir(parents=True, exist_ok=False)

  manifest = RunManifest.create(input_path=input_path, run_id=run_id)
  write_manifest(run_dir / "run.json", manifest)

  return run_dir