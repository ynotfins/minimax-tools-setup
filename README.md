# minimax-tools-setup

System tools and tuning for the MiniMax agent stack on Windows. Hardened mirror of pgvector runtime + ops scripts + docs.

## Overview

This repo contains:
- **aat** (Agent Agent Tools): Read-only CLI utilities for interacting with the pgvector knowledge base
- **configs**: Environment and runtime configuration templates
- **docs**: Operational runbooks, backup procedures, and disaster recovery guides
- **scripts**: Automation scripts for maintenance and deployment
- **references**: Architecture and handoff documentation

## Quick Start

```bash
# Install dependencies
pip install -e "."

# Run diagnostics
aat-doctor

# Ping the vector database
aat-ping
```

## Project Structure

```
minimax-tools-setup/
├── src/aat/           # Main package (aat CLI tools)
│   ├── cli.py         # Command-line interface
│   ├── settings.py    # Pydantic settings
│   └── memory/        # Vector store integration
├── configs/           # Configuration templates
├── docs/              # Operational documentation
├── scripts/           # Automation scripts
└── references/        # Architecture docs
```

## Environment Variables

Required environment variables (see `configs/` for templates):
- `PGVECTOR_*`: PostgreSQL/pgvector connection settings
- `OPENAI_*`: API keys for embeddings (if using OpenAI)
- `ANTHROPIC_*`: API keys for Claude (if using Anthropic)

## Documentation

- [Runbook](docs/RUNBOOK.md) - Day-to-day operations
- [Backup Guide](docs/BACKUP.md) - Data backup procedures
- [Disaster Recovery](docs/DISASTER_RECOVERY.md) - Recovery procedures

## License

MIT
