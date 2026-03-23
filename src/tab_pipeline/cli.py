from pathlib import Path

import typer

from tab_pipeline.core.runner import bootstrap_run

app = typer.Typer(
  help="Local staged audio-to-tab pipeline.",
  no_args_is_help=True,
)


@app.callback()
def main() -> None:
  """
  Local staged audio-to-tab pipeline.
  """
  return None


@app.command()
def run(input_path: Path) -> None:
  """
  Register a pipeline run for an input audio file.
  """
  run_dir = bootstrap_run(input_path)
  typer.echo(f"Run created: {run_dir}")


if __name__ == "__main__":
  app()