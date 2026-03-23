from pathlib import Path

from audio_separator.separator import Separator


class AudioSeparatorBackend:
  name = "audio_separator"

  def __init__(
    self,
    model_filename: str,
    model_file_dir: Path,
    sample_rate: int = 44100,
  ) -> None:
    self.model_filename = model_filename
    self.model_file_dir = model_file_dir
    self.sample_rate = sample_rate

  def separate_stems(
    self,
    input_path: Path,
    output_dir: Path,
    requested_stems: list[str],
  ) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    self.model_file_dir.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, Path] = {}

    for stem in requested_stems:
      stem_label = self._to_backend_stem_label(stem)

      separator = Separator(
        output_dir=str(output_dir),
        model_file_dir=str(self.model_file_dir),
        output_single_stem=stem_label,
        sample_rate=self.sample_rate,
      )

      separator.load_model(model_filename=self.model_filename)

      output_files = separator.separate(str(input_path))
      resolved_file = self._resolve_stem_file(
        output_files=output_files,
        output_dir=output_dir,
        stem=stem,
      )

      canonical_path = output_dir / f"{stem}.wav"
      if resolved_file.resolve() != canonical_path.resolve():
        resolved_file.replace(canonical_path)

      outputs[stem] = canonical_path

    return outputs

  @staticmethod
  def _to_backend_stem_label(stem: str) -> str:
    mapping = {
      "bass": "Bass",
      "guitar": "Guitar",
    }

    try:
      return mapping[stem]
    except KeyError as exc:
      raise ValueError(f"Unsupported requested stem: {stem}") from exc

  @staticmethod
  def _resolve_stem_file(
    output_files: list[str],
    output_dir: Path,
    stem: str,
  ) -> Path:
    candidates: list[Path] = []

    for value in output_files:
      path = Path(value)
      if not path.is_absolute():
        path = output_dir / path
      candidates.append(path)

    for path in candidates:
      if stem in path.name.lower():
        return path

    raise RuntimeError(
      f"Audio separator did not return a recognizable {stem} stem. "
      f"Output files: {output_files}"
    )