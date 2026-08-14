# TODO: Deterministic CSV emitter.
# - report_month(month: str) -> str — return CSV string for YYYY-MM
# - Header: date,vendor,category,amount,currency,source_file
# - Sort: (date ASC, source_file ASC)
# - Use csv.writer with default dialect — must be byte-identical across runs
# See PRD.md Determinism contract section.
# No network calls in this file.
