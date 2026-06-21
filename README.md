# minimax-tools-setup

System tools and tuning for the MiniMax agent stack on Windows. Hardened
mirror of pgvector runtime + ops scripts + docs. This repo is the
**between-projects workspace** for system tooling, scheduled tasks, and
AI agent tuning — not a runtime app.

- **Repo:** <https://github.com/ynotfins/minimax-tools-setup>
- **Companion runtime:** `D:\github\advanced-agent-team` (read-only here)
- **OpenClaw (locked, do not touch):** <https://github.com/ynotfins/openclaw>

---

## Overview

This repo contains:

| Path | Purpose |
|---|---|
| `src/aat/` | Read-only CLI: `aat-doctor`, `aat-ping` |
| `configs/` | Templates: `.env.example`, `pgvector.conf.example` |
| `docs/` | RUNBOOK, BACKUP, DISASTER_RECOVERY, DB_README, MCP_SETUP |
| `scripts/` | `pg_dump_backup.ps1`, `env_audit.ps1`, `db_ping_readonly.ps1`, `frequent_commit.ps1` |
| `references/handoff-docs/` | Cross-project handoff notes |
| `.cursor/rules/` | AI agent rules (auto-applied in Cursor / MiniMax) |

---

## Quick Start

```powershell
# From the repo root (D:\minimax-tools-setup)
uv sync                      # one-time, uses uv.lock
uv run aat-doctor            # prints pgvector version + read-only flag
uv run aat-ping              # prints vector / telemetry row counts
pwsh scripts\env_audit.ps1   # audit Windows env vars (masked)
```

Both CLIs must return JSON containing `"read_only": true`.

---

## Project Structure

```
minimax-tools-setup/
├── src/aat/                    # Main package (aat CLI tools)
│   ├── cli.py                  # Command-line interface
│   ├── settings.py             # Pydantic settings (read-only defaults)
│   └── memory/                 # pgvector store (read-only wrapper)
├── configs/
│   ├── .env.example            # Template — never copy real values
│   └── pgvector.conf.example   # pgvector server config template
├── docs/
│   ├── RUNBOOK.md              # Day-to-day operations
│   ├── BACKUP.md               # Data backup procedures
│   ├── DISASTER_RECOVERY.md    # Recovery procedures
│   ├── DB_README.md            # Database schema + access notes
│   └── MCP_SETUP.md            # Global MCP server config (read this first)
├── scripts/
│   ├── pg_dump_backup.ps1      # pg_dump to D:\backups\agent_core
│   ├── env_audit.ps1           # Audit Windows env vars (masked)
│   ├── db_ping_readonly.ps1    # Read-only DB ping
│   └── frequent_commit.ps1     # Commit + push helper
├── references/
│   └── handoff-docs/           # Cross-project handoff notes (manual)
├── .cursor/
│   └── rules/
│       └── minimax-tools-setup.mdc  # AI agent rules
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## Environment Variables

All credentials live in **Windows environment variables** (no `.env` in
this repo). See [`docs/MCP_SETUP.md`](docs/MCP_SETUP.md) for the full list
and `scripts/env_audit.ps1` to audit them locally (values are masked).

For this repo's CLIs, the most relevant vars are:

| Variable | Default | Purpose |
|---|---|---|
| `AGENT_CORE_PGHOST` | `127.0.0.1` | pgvector host |
| `AGENT_CORE_PGPORT` | `55432` | pgvector port |
| `AGENT_CORE_PGDATABASE` | `agent_core` | db name |
| `AGENT_CORE_PGUSER` | `postgres` | |
| `AGENT_CORE_PGPASSWORD` | _(unset)_ | read from env at runtime; never commit |
| `AGENT_CORE_READ_ONLY` | `True` | **keep `True` in this repo** |
| `PG_DUMP_BACKUP_DIR` | `D:\backups\agent_core` | `pg_dump_backup.ps1` output |
| `GIT_AUTHOR_NAME` | `R3lentless_Grind` | |
| `GIT_AUTHOR_EMAIL` | `ynotfins@gmail.com` | |

AI / dev credentials (also in Windows env vars):

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GITHUB_TOKEN` / `GITHUB_PERSONAL_ACCESS_TOKEN`
- `GITHUB_TOOLSETS`

---

## Documentation

- [Runbook](docs/RUNBOOK.md) — Day-to-day operations
- [Backup Guide](docs/BACKUP.md) — Data backup procedures
- [Disaster Recovery](docs/DISASTER_RECOVERY.md) — Recovery procedures
- [DB README](docs/DB_README.md) — Database schema + access notes
- [MCP Setup](docs/MCP_SETUP.md) — **Global MCP servers, env vars, troubleshooting**

---

## Hard Rules (every session, every agent)

1. **Database is read-only.** `agent_core_read_only = True` is the default.
   Never write to `agent_core` from this repo.
2. **No secrets in git.** `.env`, `*.pem`, `*.key` are gitignored. Real API
   keys live in Windows env vars only.
3. **No destructive ops.** No `rm -rf`, no `Remove-Item -Recurse -Force`,
   no `git push --force`, no `git reset --hard`. Use the Trash tool.
4. **PowerShell only** in shells. No `cmd.exe`, no `bash` heredocs.
5. **OpenClaw is locked.** Do not modify anything related to OpenClaw
   from this repo.
6. **Use `uv`** for Python in this repo (project has `uv.lock`).

See [`.cursor/rules/minimax-tools-setup.mdc`](.cursor/rules/minimax-tools-setup.mdc)
for the full machine-readable ruleset.

---

## Git Workflow

- Branch: `main`
- Remote: `https://github.com/ynotfins/minimax-tools-setup.git`
- Commit messages: `type: short description`
- After every meaningful change:

  ```powershell
  pwsh D:\minimax-tools-setup\scripts\frequent_commit.ps1 -Message "docs: add MCP setup"
  ```

  Or manually:

  ```powershell
  git add -A
  git commit -m "docs: add MCP setup"
  git push
  ```

---

## License

MIT
