# TODO: SQLite read/write operations.
# - ensure_schema(conn) — create tables if not exist (inline CREATE TABLE IF NOT EXISTS, no migration files)
# - add_receipt(record: dict) -> bool — insert or skip (SHA-256 dedup), returns True if inserted
# - list_receipts(filters: dict) -> list[dict] — query with optional vendor/since/until filters
# See CLAUDE.md Conventions section for deduplication rules.
# No network calls in this file.
