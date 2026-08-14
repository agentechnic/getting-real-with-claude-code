#!/usr/bin/env bash
# verify-links.sh — sanity check that every viewer.html?file=... link in index.html
# points to a markdown file that actually exists on disk.
#
# Usage: bash scripts/verify-links.sh
# Exit:  0 if all good, 1 if any link is broken.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f index.html ]]; then
  echo "error: index.html not found at $ROOT" >&2
  exit 2
fi

missing=0
checked=0

# Extract every file=... value from viewer.html links in index.html
# Matches both single and double quoted hrefs.
while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  checked=$((checked + 1))
  if [[ -f "$path" ]]; then
    printf '  ok  %s\n' "$path"
  else
    printf '  MISS %s\n' "$path"
    missing=$((missing + 1))
  fi
done < <(grep -hoE 'viewer\.html\?file=[^"'"'"' ]+' index.html archive.html | sed 's|viewer\.html?file=||' | sort -u)

echo
echo "checked: $checked link(s)"
echo "missing: $missing"

if [[ $missing -gt 0 ]]; then
  echo "FAIL: some links are broken." >&2
  exit 1
fi

echo "OK: all links resolve."
