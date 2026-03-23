from dataclasses import dataclass

from tab_pipeline.core.paths import RunPaths
from tab_pipeline.models.config import PipelineConfig


@dataclass(frozen=True)
class RunContext:
  run_id: str
  paths: RunPaths
  config: PipelineConfig