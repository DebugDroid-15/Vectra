# Security Architecture & Policies

1. **Execution Model**: Vectra scripts execute inside local Python processes.
2. **Local Diagnostics**: System logs and crash tracebacks are written strictly to local user directories (`~/.vectra/logs/`). No data is transmitted remotely without explicit user consent.
