from tab_pipeline.config import load_config


def test_load_default_config() -> None:
  config = load_config()

  assert config.pipeline.instrument == "bass"
  assert config.normalize.sample_rate == 44100
  assert config.normalize.channels == 1
  assert config.separation.backend == "stub"
  assert config.separation.requested_stems == ["bass", "guitar"]


def test_load_override_config(tmp_path) -> None:
  config_file = tmp_path / "override.yaml"
  config_file.write_text(
    '''
normalize:
  sample_rate: 48000
  channels: 2

separation:
  requested_stems:
    - bass
'''.strip(),
    encoding="utf-8",
  )

  config = load_config(config_file)

  assert config.normalize.sample_rate == 48000
  assert config.normalize.channels == 2
  assert config.separation.backend == "stub"
  assert config.separation.requested_stems == ["bass"]