"""minimax-tools-setup — pgvector read-only memory client."""
from aat.memory.pgvector_store import (
    MemoryHit,
    insert_embedding,
    is_read_only,
    log_telemetry,
    ping,
    read_settings,
    self_check,
    similarity_search,
)

__all__ = [
    "MemoryHit",
    "insert_embedding",  # guarded
    "is_read_only",
    "log_telemetry",     # guarded
    "ping",
    "read_settings",
    "self_check",        # guarded
    "similarity_search",
]
