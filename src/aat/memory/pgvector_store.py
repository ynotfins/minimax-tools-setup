r"""AAT pgvector memory client — **READ-ONLY MODE**.

This is the hardened copy of the pgvector client shipped under
D:\minimax-tools-setup (system-tools project, not a product project).
Per the operator's current rules, all database interaction from this
project is **read-only** until the team-write rules are formally
published in docs/MEMORY_RULES.md. The write methods (insert_embedding,
log_telemetry, self_check) are kept in the module so the underlying
schema and contract stays identical to the runtime copy at
D:\github\advanced-agent-team\src\aat\memory\pgvector_store.py — but
they raise PermissionError if anyone tries to call them from this
project without first setting AGENT_CORE_READ_ONLY=false in the
process environment.

Connection details come from `aat.settings`, which reads the
`AGENT_CORE_PG*` Windows env vars (see `docs/ENVIRONMENT.md`).

Public API (read-only):

- `ping() -> dict`  — version + extensions + row counts
- `similarity_search(...) -> list[MemoryHit]` — HNSW cosine search
- `read_settings() -> dict` — current connection settings, redacted
- `is_read_only() -> bool` — convenience

Write API (raises unless `AGENT_CORE_READ_ONLY=false`):

- `insert_embedding(...)` — guarded
- `log_telemetry(...)` — guarded
- `self_check()` — guarded
"""
from __future__ import annotations

import json
import os
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Sequence

# Read settings (no-op write side-effects). Note we deliberately do NOT
# import `aat.settings` here — we read env vars directly so this module
# can also be used from a one-off Python process without installing the
# `aat` package. Mirror the field defaults in `aat.settings.Settings`.


def _read_env() -> dict:
    return {
        "host": os.environ.get("AGENT_CORE_PGHOST", "127.0.0.1"),
        "port": int(os.environ.get("AGENT_CORE_PGPORT", "55432")),
        "dbname": os.environ.get("AGENT_CORE_PGDATABASE", "agent_core"),
        "user": os.environ.get("AGENT_CORE_PGUSER", "postgres"),
        "password": os.environ.get("AGENT_CORE_PGPASSWORD"),
        "vector_dim": int(os.environ.get("AGENT_CORE_VECTOR_DIM", "1536")),
    }


def is_read_only() -> bool:
    """True unless `AGENT_CORE_READ_ONLY=false` is explicitly set.

    Default = read-only. The flag is opt-out (not opt-in) so a fresh
    shell inherits the safe policy.
    """
    flag = os.environ.get("AGENT_CORE_READ_ONLY", "true").strip().lower()
    return flag not in {"false", "0", "no", "off"}


def _connect():
    import psycopg2
    env = _read_env()
    return psycopg2.connect(
        host=env["host"],
        port=env["port"],
        dbname=env["dbname"],
        user=env["user"],
        password=env["password"],
    )


@contextmanager
def _cursor():
    import psycopg2.extras
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
    finally:
        conn.close()


def _guard_write(op: str) -> None:
    if is_read_only():
        raise PermissionError(
            f"{op}() is blocked because AGENT_CORE_READ_ONLY is true. "
            "This project (minimax-tools-setup) is in read-only mode "
            "until docs/MEMORY_RULES.md is published. To override for "
            "this process only, run with AGENT_CORE_READ_ONLY=false in "
            "the environment."
        )


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MemoryHit:
    id: uuid.UUID
    agent_signature: str
    associated_project_path: str
    document_source: str
    content_chunk: str
    metadata: dict
    cosine_similarity: float


# ---------------------------------------------------------------------------
# Public API — read-only
# ---------------------------------------------------------------------------


def ping() -> dict:
    """Return server version + vector extension status + row counts."""
    with _cursor() as cur:
        cur.execute("SELECT version() AS version")
        version = cur.fetchone()["version"]
        cur.execute(
            "SELECT extname, extversion FROM pg_extension "
            "WHERE extname IN ('vector', 'pgcrypto') ORDER BY extname"
        )
        extensions = {row["extname"]: row["extversion"] for row in cur.fetchall()}
        cur.execute(
            "SELECT (SELECT count(*) FROM global_vector_memory_store) AS vector_rows, "
            "       (SELECT count(*) FROM agent_cross_project_telemetry) AS telemetry_rows"
        )
        counts = cur.fetchone()
    env = _read_env()
    return {
        "version": version,
        "extensions": extensions,
        "vector_rows": counts["vector_rows"],
        "telemetry_rows": counts["telemetry_rows"],
        "host": env["host"],
        "port": env["port"],
        "database": env["dbname"],
        "read_only": is_read_only(),
    }


def read_settings() -> dict:
    """Return the current connection settings, with password redacted."""
    env = _read_env()
    if env["password"]:
        env["password"] = "***REDACTED***"
    env["read_only"] = is_read_only()
    return env


def similarity_search(
    *,
    query_embedding: Sequence[float],
    agent_signature: str | None = None,
    project_path: str | None = None,
    top_k: int = 5,
) -> list[MemoryHit]:
    """Cosine-similarity nearest-neighbour search (read-only)."""
    env = _read_env()
    if len(query_embedding) != env["vector_dim"]:
        raise ValueError(
            f"query_embedding has dimension {len(query_embedding)}, "
            f"expected {env['vector_dim']}"
        )
    embedding_literal = "[" + ",".join(f"{float(x):.8f}" for x in query_embedding) + "]"

    where = []
    params: list = [embedding_literal]
    if agent_signature:
        where.append("agent_signature = %s")
        params.append(agent_signature)
    if project_path:
        where.append("associated_project_path = %s")
        params.append(project_path)
    where_clause = ("WHERE " + " AND ".join(where)) if where else ""

    params.append(embedding_literal)
    params.append(int(top_k))
    sql = f"""
        SELECT id,
               agent_signature,
               associated_project_path,
               document_source,
               content_chunk,
               metadata,
               1 - (embedding <=> %s::vector) AS cosine_similarity
        FROM global_vector_memory_store
        {where_clause}
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """
    with _cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    hits: list[MemoryHit] = []
    for r in rows:
        hits.append(
            MemoryHit(
                id=r["id"],
                agent_signature=r["agent_signature"],
                associated_project_path=r["associated_project_path"],
                document_source=r["document_source"],
                content_chunk=r["content_chunk"],
                metadata=dict(r["metadata"] or {}),
                cosine_similarity=float(r["cosine_similarity"]),
            )
        )
    return hits


# ---------------------------------------------------------------------------
# Write API — guarded
# ---------------------------------------------------------------------------


def insert_embedding(
    *,
    agent_signature: str,
    project_path: str,
    document_source: str,
    content_chunk: str,
    embedding: Sequence[float],
    metadata: dict | None = None,
) -> uuid.UUID:
    """Insert a single embedding. BLOCKED in this project unless the read-only
    flag is explicitly disabled in the process environment."""
    _guard_write("insert_embedding")
    env = _read_env()
    if len(embedding) != env["vector_dim"]:
        raise ValueError(
            f"embedding has dimension {len(embedding)}, expected {env['vector_dim']}"
        )
    embedding_literal = "[" + ",".join(f"{float(x):.8f}" for x in embedding) + "]"
    meta = metadata or {}
    with _cursor() as cur:
        cur.execute(
            """
            INSERT INTO global_vector_memory_store
                (agent_signature, associated_project_path,
                 document_source, content_chunk, embedding, metadata)
            VALUES (%s, %s, %s, %s, %s::vector, %s::jsonb)
            RETURNING id
            """,
            (
                agent_signature,
                project_path,
                document_source,
                content_chunk,
                embedding_literal,
                json.dumps(meta),
            ),
        )
        return cur.fetchone()["id"]


def log_telemetry(
    *,
    agent_name: str,
    project_path: str,
    execution_status: str,
    shared_logs: str | None = None,
) -> uuid.UUID:
    """Insert a telemetry row. BLOCKED in this project unless the read-only
    flag is explicitly disabled."""
    _guard_write("log_telemetry")
    with _cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_cross_project_telemetry
                (agent_name, active_project_path, execution_status, shared_logs)
            VALUES (%s, %s, %s, %s)
            RETURNING run_id
            """,
            (agent_name, project_path, execution_status, shared_logs),
        )
        return cur.fetchone()["run_id"]


def self_check() -> dict:
    """Insert one deterministic vector, query it back, log telemetry.

    BLOCKED in this project unless the read-only flag is explicitly disabled.
    The active write counterpart lives at
    `D:\github\advanced-agent-team\src\aat\memory\pgvector_store.py`.
    """
    _guard_write("self_check")
    env = _read_env()
    embedding = [0.001] * env["vector_dim"]
    row_id = insert_embedding(
        agent_signature="minimax-tools-doctor",
        project_path=os.path.abspath(os.getcwd()),
        document_source="minimax-tools-setup/src/aat/memory/pgvector_store.py::self_check",
        content_chunk="minimax-tools-setup pgvector self-check",
        embedding=embedding,
        metadata={"self_check": True, "dimensions": env["vector_dim"]},
    )
    hits = similarity_search(
        query_embedding=embedding, agent_signature="minimax-tools-doctor", top_k=1
    )
    similarity = hits[0].cosine_similarity if hits else 0.0
    run_id = log_telemetry(
        agent_name="minimax-tools-doctor",
        project_path=os.path.abspath(os.getcwd()),
        execution_status="verified",
        shared_logs=f"self_check row={row_id} similarity={similarity:.6f}",
    )
    return {
        "vector_row_id": str(row_id),
        "telemetry_run_id": str(run_id),
        "cosine_similarity": float(similarity),
    }
