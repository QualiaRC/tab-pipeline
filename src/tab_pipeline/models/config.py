from typing import Literal

from pydantic import BaseModel


class PipelineSection(BaseModel):
  instrument: Literal["bass", "guitar"] = "bass"


class NormalizeSection(BaseModel):
  sample_rate: int = 44100
  channels: int = 1
  codec: str = "pcm_s16le"


class SeparationSection(BaseModel):
  backend: Literal["stub"] = "stub"
  target_stem: Literal["bass"] = "bass"


class PipelineConfig(BaseModel):
  pipeline: PipelineSection = PipelineSection()
  normalize: NormalizeSection = NormalizeSection()
  separation: SeparationSection = SeparationSection()