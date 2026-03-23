import shutil
from pathlib import Path


class StubSeparator:
  name = "stub"

  def separate_stems(
    self,
    input_path: Path,
    output_dir: Path,
    requested_stems: list[str],
  ) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, Path] = {}

    for stem in requested_stems:
      stem_path = output_dir / f"{stem}.wav"
      shutil.copy2(input_path, stem_path)
      outputs[stem] = stem_path

    return outputs