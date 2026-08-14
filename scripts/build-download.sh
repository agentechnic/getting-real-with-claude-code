#!/usr/bin/env bash
# Rebuild nussaa.zip, the download attendees get instead of cloning the repo.
#
# Run this after ANY change under nussaa/ — a regenerated corpus, an edited
# CLAUDE.md — or the download and the repo will disagree, and half the room
# ends up working from different material to the other half.
#
# Usage: bash scripts/build-download.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

rm -f nussaa.zip
zip -q -r nussaa.zip nussaa -x "*.DS_Store" "*__pycache__*"

# List once. Piping `unzip -l` straight into `grep -q` closes the pipe early,
# and under `pipefail` that reports a missing file that is actually present.
listing="$(unzip -l nussaa.zip)"

size=$(ls -lh nussaa.zip | awk '{print $5}')
files=$(printf '%s\n' "$listing" | tail -1 | awk '{print $2}')
echo "nussaa.zip — $files files, $size"

q1=$(printf '%s\n' "$listing" | grep -c "tickets-q1/ticket-" || true)
q2=$(printf '%s\n' "$listing" | grep -c "tickets-q2/ticket-" || true)
echo "  tickets-q1: $q1 (expect 200)"
echo "  tickets-q2: $q2 (expect 120)"
if [ "$q1" -ne 200 ] || [ "$q2" -ne 120 ]; then
  echo "FAIL: wrong ticket count — did the corpus regenerate?" >&2
  exit 1
fi

for f in nussaa/CLAUDE.md nussaa/README.md \
         nussaa/context/changelog.md nussaa/context/themes-2025-q4.md; do
  printf '%s\n' "$listing" | grep -qF "$f" || { echo "FAIL: missing $f" >&2; exit 1; }
done
echo "  CLAUDE.md, README and context all present"

# The answer key must never reach an attendee.
if printf '%s\n' "$listing" | grep -qiE "answer-key|dry-run|facilitator"; then
  echo "FAIL: facilitator material is inside the download" >&2
  exit 1
fi
echo "  no facilitator material inside"
