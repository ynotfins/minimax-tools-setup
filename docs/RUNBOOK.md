# Operations Runbook

## Daily Operations

### Health Check
```bash
# Run system diagnostics
aat-doctor

# Ping vector database
aat-ping
```

### Environment Verification
```bash
# Check environment variables are set correctly
aat-env
```

## Common Tasks

### Viewing Vector Data
The database is in **read-only mode** by default. To query:
```python
from aat.memory import VectorStore
store = VectorStore()
results = store.search("your query", top_k=5)
```

### Monitoring Disk Space
- Database drive (E:): `Get-PSDrive E`
- Extensions drive (F:): `Get-PSDrive F`

## Troubleshooting

### pgvector Connection Issues
1. Check PostgreSQL service is running: `Get-Service postgresql*`
2. Verify connection: `aat-ping`
3. Check firewall rules for port 5432

### Vector Search Returns No Results
1. Verify embeddings exist: Check `pgvector_read` table row count
2. Check logs in `logs/` directory
3. Verify environment variables are correct

## Maintenance Windows

Schedule weekly:
- Backup verification
- Log rotation
- Disk space audit
