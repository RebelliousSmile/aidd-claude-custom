#!/usr/bin/env bash
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PY=${WIREFRAMES_SELFTEST_PYTHON:-python3}
CHROMIUM=${WIREFRAMES_CHROMIUM:-}
if ! "$PY" -c 'import playwright' >/dev/null 2>&1; then
  echo "Error: Playwright 1.60.0 is required; install adapters/measure/requirements.txt" >&2
  exit 2
fi
if [ -z "$CHROMIUM" ] || [ ! -x "$CHROMIUM" ]; then
  echo "Error: WIREFRAMES_CHROMIUM must name an executable Chromium" >&2
  exit 2
fi
export WIREFRAMES_CHROMIUM="$CHROMIUM"
"$PY" -m unittest discover -s "$ROOT/adapters/wireframes/tests" -p 'test_*.py'
