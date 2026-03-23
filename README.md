# tab-pipeline

Local Python pipeline for staged audio-to-tab transcription workflows.

## Overview

`tab-pipeline` is a CLI-first Python project for building an audio transcription pipeline in small, inspectable stages.

The long-term direction is:

- full-song audio input
- source separation
- instrument-focused processing
- transcription and cleanup
- fretboard or tab mapping
- digital tab export

The current implementation is intentionally narrower. The project now has a working staged pipeline foundation with input ingest, audio normalization, and multi-stem separation plumbing.

## Current progress

Implemented so far:

- project scaffold with `uv`, Python 3.11, and `src/` layout
- CLI entrypoint with explicit `run` subcommand
- per-run workspace creation under `data/runs/`
- run manifest generation
- ingest stage with input validation and file hashing
- normalize stage using `ffmpeg`
- structured per-run workspace paths
- typed config models with YAML defaults and override support
- separation stage with a pluggable adapter interface
- stub separation backend for fast local testing
- real `audio-separator` backend integration path
- multi-stem separation support for:
  - bass
  - guitar

## Current pipeline stages

At the moment, a pipeline run performs these stages:

1. **ingest**
   - validates the input path
   - resolves the source file
   - computes SHA-256
   - records source metadata in the run manifest

2. **normalize**
   - converts the source file into a canonical WAV
   - currently targets a mono working file
   - records output metadata in the run manifest

3. **separate**
   - separates requested stems into canonical workspace paths
   - currently supports `bass` and `guitar`
   - can run with either:
     - `stub`
     - `audio_separator`

## Current repository layout

```text
tab-pipeline/
  pyproject.toml
  README.md
  .python-version
  .gitignore

  configs/
    local-audio-separator.yaml

  src/
    tab_pipeline/
      cli.py
      config.py
      paths.py

      config/
        defaults.yaml

      core/
        hashing.py
        manifest.py
        paths.py
        runner.py

      models/
        config.py
        context.py
        run.py

      stages/
        ingest.py
        normalize.py
        separate.py

      adapters/
        audio_separator_backend.py
        ffmpeg.py
        separator.py
        stub_separator.py

  data/
    inputs/
    runs/
    cache/
    exports/

  tests/
    test_config.py
    test_smoke.py
```

## Runtime requirements

### System dependencies

The project currently depends on:

- **Python 3.11**
- **uv** for Python environment and dependency management
- **ffmpeg**
- **ffprobe**

`ffprobe` is typically installed alongside `ffmpeg`.

### Python dependencies

The project uses:

- `typer`
- `pydantic`
- `pyyaml`
- `audio-separator` for the real separation backend

### Verify installed tools

```bash
python3 --version
uv --version
ffmpeg -version
ffprobe -version
```

Expected Python version:

```text
3.11
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPO_URL>
cd tab-pipeline
```

### 2. Install `uv`

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For other install methods, refer to the official `uv` documentation.

### 3. Install `ffmpeg`

#### macOS (Homebrew)

```bash
brew install ffmpeg
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows

Install `ffmpeg` using your preferred package manager or the official binaries, then ensure both `ffmpeg` and `ffprobe` are available on your `PATH`.

### 4. Sync project dependencies

```bash
uv sync --extra dev
```

This installs runtime and development dependencies into the local `.venv`.

## Development setup

You can use `uv run ...` directly, which is the simplest workflow.

If you want to activate the environment manually:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## Configuration model

The project uses a two-layer config approach:

- `src/tab_pipeline/config/defaults.yaml`
  - packaged application defaults
- `configs/*.yaml`
  - local or environment-specific override files

The loader always reads packaged defaults first, then optionally deep-merges an override file supplied at runtime.

### Current default config shape

```yaml
pipeline:
  instrument: bass

normalize:
  sample_rate: 44100
  channels: 1
  codec: pcm_s16le

separation:
  backend: stub
  requested_stems:
    - bass
    - guitar
  model_filename: htdemucs_6s.yaml
  model_file_dir: data/models/audio-separator
```

## Running the pipeline

### Stub backend

The default backend is `stub`, which is useful for local structure and test validation.

Run with defaults:

```bash
uv run tab-pipeline run /path/to/real-audio-file.wav
```

### Real audio-separator backend

A local override config can switch the backend to `audio_separator`.

Example override file:

```yaml
separation:
  backend: audio_separator
  requested_stems:
    - bass
    - guitar
  model_filename: htdemucs_6s.yaml
  model_file_dir: data/models/audio-separator
```

Run with the real backend:

```bash
uv run tab-pipeline run /path/to/real-audio-file.wav --config configs/local-audio-separator.yaml
```

## Important input note

The pipeline now invokes `ffmpeg` during normalization, so the input must be a **real audio file**.

This will **not** work:

```bash
touch scratch/test.wav
```

That only creates an empty file with a `.wav` extension.

A quick way to generate a valid silent test WAV is:

```bash
mkdir -p scratch
ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 scratch/test.wav
uv run tab-pipeline run scratch/test.wav
```

## Current run output shape

A typical run currently produces something like:

```text
data/runs/<run-id>/
  run.json
  workspace/
    normalize/
      normalized.wav
    separate/
      bass.wav
      guitar.wav
```

## Manifest behavior

Each run writes a `run.json` manifest containing:

- run ID
- creation time
- effective config snapshot
- input metadata
- stage records

Current stage records include timing and per-stage details such as output paths and artifact sizes.

## Testing

Run the test suite with:

```bash
uv run pytest
```

The tests currently use the `stub` separation backend so they remain lightweight and deterministic.

## Design principles

The project is being built around a few constraints:

- **stage-by-stage development**
- **inspectable run outputs**
- **deterministic structure**
- **clear filesystem boundaries**
- **CLI-first execution**
- **pluggable adapter seams for heavier backends**

## Current boundaries

What the project does now:

- staged audio preparation
- basic artifact creation
- bass and guitar stem generation plumbing

What it does **not** do yet:

- stem conditioning
- note transcription
- onset or pitch cleanup
- fretboard mapping
- tablature export
- persistent content-addressed caching
- rich failure/retry state handling

## Near-term next steps

Likely next areas of work:

- artifact modeling for stage outputs
- better failure handling and manifest status updates
- stem conditioning
- note transcription
- downstream bass-first processing
- later guitar-specific experimentation

## Notes on generated data

Generated runtime artifacts under `data/` are intended to remain local and are ignored by git except for placeholder files used to preserve directory structure.

Typical generated outputs include:

- run directories
- normalized audio
- separated stems
- future cache artifacts

