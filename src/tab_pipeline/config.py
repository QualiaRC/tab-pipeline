from pathlib import Path
from typing import Any

import yaml

from tab_pipeline.models.config import PipelineConfig


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
  result = dict(base)

  for key, value in override.items():
    if (
      key in result
      and isinstance(result[key], dict)
      and isinstance(value, dict)
    ):
      result[key] = _deep_merge(result[key], value)
    else:
      result[key] = value

  return result


def load_config(config_path: Path | None = None) -> PipelineConfig:
  defaults_path = Path(__file__).resolve().parent / "config" / "defaults.yaml"
  defaults_data = yaml.safe_load(defaults_path.read_text(encoding="utf-8")) or {}

  if config_path is None:
    return PipelineConfig.model_validate(defaults_data)

  override_data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
  merged = _deep_merge(defaults_data, override_data)

  return PipelineConfig.model_validate(merged)