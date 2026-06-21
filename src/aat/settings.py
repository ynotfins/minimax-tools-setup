"""Settings for the read-only minimax-tools-setup tooling.

Mirrors the layout of `D:\github\advanced-agent-team\src\aat\settings.py`
but only reads env vars — never writes secrets into the repo. The
`agent_core_read_only` flag defaults to True so a fresh shell inherits
the safe policy. Set `AGENT_CORE_READ_ONLY=false` in the process
environment to allow write operations (used by the runtime project
in `D:\github\advanced-agent-team`, NOT by this tooling project).
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---- Connection to the agent_core pgvector cluster (F: engine / E: data) ----
    agent_core_pghost: str = "127.0.0.1"
    agent_core_pgport: int = 55432
    agent_core_pgdatabase: str = "agent_core"
    agent_core_pguser: str = "postgres"
    agent_core_pgpassword: str | None = None
    agent_core_vector_dim: int = 1536
    agent_core_read_only: bool = True  # SAFE DEFAULT for tooling project

    # ---- Backup location (used by scripts/pg_dump_backup.ps1) ----
    pg_dump_backup_dir: str = r"D:\backups\agent_core"

    # ---- Operator identity ----
    git_author_name: str = "R3lentless_Grind"
    git_author_email: str = "ynotfins@gmail.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
