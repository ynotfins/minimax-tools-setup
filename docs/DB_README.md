# Database Reference

## Connection Details

| Setting | Value |
|---------|-------|
| Host | localhost |
| Port | 5432 |
| Database | vector_db |
| User | postgres |

## Drive Locations

| Component | Location |
|-----------|----------|
| PostgreSQL data | E:\\postgres_data |
| pgvector extension | F:\\pgvector_ext |

## Schema

### Tables

#### `pgvector_read` (Primary vector table)
- Stores embeddings for semantic search
- Columns: id, content, metadata, embedding (vector), created_at

#### `telemetry_events` (Optional)
- Tracks usage events
- Columns: id, event_type, event_data, timestamp

## Vector Operations

### Search
```sql
SELECT id, content, 1 - (embedding <=> '[embedding_vector]') AS similarity
FROM pgvector_read
ORDER BY embedding <=> '[embedding_vector]'
LIMIT 5;
```

### List all vectors
```sql
SELECT COUNT(*) FROM pgvector_read;
SELECT id, LEFT(content, 50) as preview FROM pgvector_read;
```

## Security Notes

- Database is configured for **read-only** access by default
- Write operations require explicit `READ_ONLY_MODE=false`
- All operations are logged

## Performance Tuning

See `configs/pgvector.conf.example` for recommended settings.
