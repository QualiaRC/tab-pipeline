# tab-pipeline

Local Python pipeline for staged audio-to-tab transcription workflows.

## Current scope

Early bootstrap only:
- register a run
- create a run directory
- write a run manifest

## Development

```bash
uv sync --extra dev
uv run tab-pipeline run path/to/song.wav
uv run pytest
```