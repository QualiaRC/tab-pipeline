import json
from pathlib import Path

from tab_pipeline.models.run import RunManifest


def write_manifest(path: Path, manifest: RunManifest) -> None:
  path.write_text(
    json.dumps(manifest.model_dump(mode="json"), indent=2),
    encoding="utf-8",
  )