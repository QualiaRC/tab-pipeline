from dataclasses import dataclass

from tab_pipeline.core.paths import RunPaths


@dataclass(frozen=True)
class RunContext:
  run_id: str
  paths: RunPaths