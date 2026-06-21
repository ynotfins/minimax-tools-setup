r"""minimax-tools-setup CLI.

Only read-only commands are exposed here. The full CLI (with writes)
lives in D:\github\advanced-agent-team\src\aat\cli.py.
"""
from __future__ import annotations

import json
import sys

import typer

from aat.memory import is_read_only, ping, read_settings, similarity_search

app = typer.Typer(help="minimax-tools-setup CLI (read-only)")


@app.command()
def doctor() -> None:
    """Read-only health probe for the pgvector memory layer."""
    info = ping()
    typer.echo(json.dumps(info, indent=2, default=str))
    if not info["extensions"].get("vector"):
        typer.echo("ERROR: pgvector extension is missing", err=True)
        sys.exit(2)


@app.command()
def ping_cmd() -> None:
    """Same as `doctor` but a one-liner."""
    info = ping()
    typer.echo(
        f"PG {info['version'].split(',')[0]} | "
        f"pgvector {info['extensions'].get('vector', 'missing')} | "
        f"vec_rows={info['vector_rows']} tel_rows={info['telemetry_rows']} | "
        f"read_only={info['read_only']}"
    )


@app.command()
def env() -> None:
    """Show the (redacted) connection settings + read-only flag."""
    typer.echo(json.dumps(read_settings(), indent=2))


@app.command()
def read_only_flag() -> None:
    """Print the current AGENT_CORE_READ_ONLY state (true/false)."""
    typer.echo("true" if is_read_only() else "false")


if __name__ == "__main__":
    app()
