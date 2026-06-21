# MCP Server Setup (Global)

This document captures the **global MCP (Model Context Protocol) server
configuration** that is available to every project in MiniMax on this Windows
machine. It mirrors the two handoff docs that were added when the MiniMax
agent team was set up in the newer MiniMax app.

> **TL;DR** — All MCP servers listed below are configured at the MiniMax
> app level (not per-project). They are reachable from any project opened
> inside MiniMax. The credentials they need are stored in **Windows
> environment variables** (no `.env` files in this repo).

---

## 1. Server Inventory

| Server | Purpose | Auth source | Status |
|---|---|---|---|
| `mcp__matrix__bash` | Run shell commands (PowerShell on Windows) | OS user | ✅ working |
| `mcp__matrix__read` / `write` / `edit` | File system read/write | OS user | ✅ working |
| `mcp__matrix__glob` / `grep` | Code search | OS user | ✅ working |
| `mcp__matrix__web_search` / `extract` | Web research | n/a (no key) | ✅ working |
| `mcp__matrix__image_synthesize` / `images_understand` | Image generation + vision | `OPENAI_API_KEY` | ✅ working |
| `mcp__matrix__gen_videos` / `batch_image_to_video` | Video generation | `OPENAI_API_KEY` | ✅ working |
| `mcp__matrix__gen_audios` / `batch_text_to_audio` / `tts` | Audio + TTS | `OPENAI_API_KEY` | ✅ working |
| `mcp__matrix__batch_text_to_music` | Music generation | `OPENAI_API_KEY` | ✅ working |
| `mcp__matrix__create_cron_job` | Scheduled tasks | MiniMax scheduler | ✅ working |
| `mcp__matrix__deploy` / `deploy_html_presentation` | Static site + slide deploys | MiniMax host | ✅ working |
| `mcp__matrix__html_to_pdf` / `pdf` tools | PDF generation | n/a | ✅ working |
| `mcp__matrix__render_mermaid` | Diagrams | n/a | ✅ working |
| `mcp__matrix__stocks_*` | Market data | `STOCKS_API_KEY` (optional) | ✅ working |
| `mcp__matrix__flights_search` / `hotels_search` | Travel | n/a | ✅ working |
| `mcp__matrix__twitter_*` | Twitter / X | `TWITTER_BEARER_TOKEN` (optional) | ✅ working |
| `mcp__matrix__extract_pdfs_*` | PDF parsing | n/a | ✅ working |

> **Out of scope here** — Supabase tools and any per-project MCP servers.
> Those are configured when a new project is created.

---

## 2. Environment Variables (Windows)

All credentials live in **Windows environment variables**, not in this repo.
Set them once in:

```
System Properties → Advanced → Environment Variables…
```

### Required for AI features

| Variable | Used by | Notes |
|---|---|---|
| `OPENAI_API_KEY` | `image_synthesize`, `gen_videos`, `gen_audios`, `batch_text_to_music`, embeddings | sk-… |
| `ANTHROPIC_API_KEY` | Claude (if a project uses Anthropic) | sk-ant-… |

### Required for code/dev

| Variable | Used by | Notes |
|---|---|---|
| `GITHUB_TOKEN` | `git push` from scripts | Personal access token (PAT) |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Same as above (alias) | |
| `GITHUB_TOOLSETS` | MiniMax GitHub tools | comma-separated: `repos,issues,pull_requests,actions,code_security` |

### Required for pgvector tooling (this repo)

| Variable | Default | Notes |
|---|---|---|
| `AGENT_CORE_PGHOST` | `127.0.0.1` | pgvector host |
| `AGENT_CORE_PGPORT` | `55432` | pgvector port |
| `AGENT_CORE_PGDATABASE` | `agent_core` | db name |
| `AGENT_CORE_PGUSER` | `postgres` | |
| `AGENT_CORE_PGPASSWORD` | _(unset)_ | read from env at runtime; never commit |
| `AGENT_CORE_READ_ONLY` | `True` | this repo is read-only |
| `PG_DUMP_BACKUP_DIR` | `D:\backups\agent_core` | where `pg_dump_backup.ps1` writes |
| `GIT_AUTHOR_NAME` | `R3lentless_Grind` | |
| `GIT_AUTHOR_EMAIL` | `ynotfins@gmail.com` | |

### Quick audit

Run `scripts/env_audit.ps1` from this repo to print which of the variables
above are set (values are **masked**). The script does not write to disk.

```powershell
pwsh D:\minimax-tools-setup\scripts\env_audit.ps1
```

---

## 3. Verifying MCP Is Working

From any MiniMax session, ask the agent:

> "List the MCP tools you have access to."

You should see the full list in §1. To smoke-test a few:

```python
# In a MiniMax chat:
# - Ask for a Mermaid diagram (uses render_mermaid)
# - Ask for a stock quote (uses stocks_price)
# - Ask for a web search (uses batch_web_search)
```

For this repo specifically:

```powershell
cd D:\minimax-tools-setup
uv run aat-doctor   # prints pgvector connection + version + read-only flag
uv run aat-ping     # prints vector/telemetry row counts
```

Both must return JSON containing `"read_only": true`.

---

## 4. Global vs Per-Project

The MCP servers in §1 are **app-level**: once configured in MiniMax, they
work in every project on this machine. The credentials in §2 are also
**app-level** (Windows env vars). They are read by every tool automatically.

When you start a new project (e.g., a new agent team), you typically do
**not** need to reconfigure MCP. You only need to:

1. Create the project folder.
2. `cd` into it from MiniMax.
3. Add project-specific secrets (if any) as new Windows env vars.

---

## 5. Troubleshooting

| Symptom | Fix |
|---|---|
| `aat-doctor` says it cannot connect | Check `AGENT_CORE_PGHOST` / `AGENT_CORE_PGPORT`; verify the pgvector service is running |
| `OPENAI_API_KEY not set` | Set it in Windows env vars, then **restart MiniMax** so the new process inherits it |
| Git push fails 401 | Regenerate `GITHUB_TOKEN` and update Windows env var |
| MCP tools missing | Open MiniMax settings → MCP servers, re-enable the ones you need |
| `git push` asks for credentials | Use the PAT in `GITHUB_TOKEN`; never type a password |

---

## 6. What This Repo Does NOT Touch

- **OpenClaw** — locked, do not modify from this repo. Repo:
  <https://github.com/ynotfins/openclaw>
- **Supabase projects** — created per-project, not globally
- **The pgvector schema/data** — read-only here; owned by the runtime
  project at `D:\github\advanced-agent-team`
