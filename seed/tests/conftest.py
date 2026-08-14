"""Shared test setup.

Two things matter here.

1. **The tests never call the Claude API.** `extract.py` must check for the
   `RECEIPTS_FIXTURE_DIR` environment variable and, when it is set, read the
   recorded JSON for a receipt from that folder instead of calling Claude.
   That contract is written down in CLAUDE.md and PRD.md. It is what makes the
   suite fast, free, and identical on every run.

2. **The tests run the CLI as a subprocess**, not by importing it. That way
   `pytest --collect-only` works before a single line of `src/receipts/` has
   been written — you can see the three tests waiting for you on day one.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SEED_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = SEED_ROOT / "tests" / "fixtures" / "extractions"
GOLDEN_DIR = SEED_ROOT / "tests" / "golden"


@pytest.fixture
def workspace(tmp_path):
    """A throwaway copy of inbox/ with its own empty ledger."""
    shutil.copytree(SEED_ROOT / "inbox", tmp_path / "inbox")
    return tmp_path


@pytest.fixture
def run_receipts(workspace):
    """Run the receipts CLI inside the workspace, with the API stubbed out."""

    def _run(*args, expect_success=True):
        env = {
            **os.environ,
            "RECEIPTS_FIXTURE_DIR": str(FIXTURE_DIR),
            "RECEIPTS_DB": str(workspace / "ledger.db"),
        }
        result = subprocess.run(
            [sys.executable, "-m", "receipts.cli", *args],
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True,
        )
        if expect_success and result.returncode != 0:
            pytest.fail(
                f"receipts {' '.join(args)} exited {result.returncode}\n"
                f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
            )
        return result

    return _run


@pytest.fixture
def golden_may():
    return (GOLDEN_DIR / "may.csv").read_text()
