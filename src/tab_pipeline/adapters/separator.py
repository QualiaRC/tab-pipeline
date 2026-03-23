from pathlib import Path
from typing import Protocol


class Separator(Protocol):
  name: str

  def separate_stems(
    self,
    input_path: Path,
    output_dir: Path,
    requested_stems: list[str],
  ) -> dict[str, Path]:
    ...