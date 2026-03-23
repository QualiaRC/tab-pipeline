from datetime import datetime, UTC
from pathlib import Path

from pydantic import BaseModel, Field


class RunInput(BaseModel):
  source_path: str
  source_name: str


class RunManifest(BaseModel):
  run_id: str
  created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
  input: RunInput

  @classmethod
  def create(cls, input_path: Path, run_id: str) -> "RunManifest":
    return cls(
      run_id=run_id,
      input=RunInput(
        source_path=str(input_path.resolve()),
        source_name=input_path.name,
      ),
    )