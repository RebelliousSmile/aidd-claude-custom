#!/usr/bin/env sh
# design:harness selftest — proves the --contract exit-code space and the option-C
# stylesheet inlining. Runs harness.py against the scaffold path and the five fixtures,
# asserting each exit code, the inlined banner, the single no-stylesheet warning, and the
# absence of any @media. Exit 0 iff every assertion holds.
#
# Usage:  cd plugins/design && bash tools/harness-selftest.sh
set -u

DIR=$(CDPATH= cd "$(dirname "$0")/.." && pwd)
HARNESS="$DIR/adapters/harness/harness.py"
FIX="$DIR/adapters/harness/fixtures"
OUT=$(mktemp -d)
trap 'rm -rf "$OUT"' EXIT
fail=0

check() {  # name expected_code contract_dir(optional)
  name=$1; want=$2; contract=${3:-}
  if [ -n "$contract" ]; then
    python "$HARNESS" --out "$OUT/o.html" --contract "$contract" >"$OUT/out" 2>"$OUT/err"
  else
    python "$HARNESS" --out "$OUT/o.html" >"$OUT/out" 2>"$OUT/err"
  fi
  got=$?
  if [ "$got" -ne "$want" ]; then
    echo "FAIL $name: exit $got, expected $want"; cat "$OUT/err"; fail=1
  else
    echo "ok   $name: exit $got"
  fi
}

check "scaffold"            0
check "2x"                  0 "$FIX/2x"
check "2x-no-stylesheet"    0 "$FIX/2x-no-stylesheet"
check "2x-missing-artifact" 2 "$FIX/2x-missing-artifact"
check "2x-bad-release"      2 "$FIX/2x-bad-release"
check "1x"                  3 "$FIX/1x"

# --contract on the 2.x fixture must inline the generated stylesheet banner.
python "$HARNESS" --out "$OUT/c.html" --contract "$FIX/2x" >/dev/null 2>&1
if grep -q "GENERATED from tokens.json" "$OUT/c.html"; then
  echo "ok   2x: stylesheet inlined"
else
  echo "FAIL 2x: stylesheet banner not inlined"; fail=1
fi

# The no-stylesheet contract must emit exactly one stderr warning.
python "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-no-stylesheet" 2>"$OUT/err" >/dev/null
n=$(grep -c "Warning" "$OUT/err")
if [ "$n" -eq 1 ]; then echo "ok   2x-no-stylesheet: one warning"; else echo "FAIL warning count $n"; fail=1; fi

# No @media anywhere — the device model is class-based samples only.
python "$HARNESS" --out "$OUT/s.html" >/dev/null 2>&1
if grep -q "@media" "$OUT/s.html" "$OUT/c.html"; then
  echo "FAIL @media present in generated output"; fail=1
else
  echo "ok   no @media in scaffold or coupled output"
fi

# The bad-release message must name release.json; missing-artifact must name generate.py;
# 1x must name migrate-contract.py.
python "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-bad-release" 2>"$OUT/err" >/dev/null || true
grep -q "release.json" "$OUT/err" || { echo "FAIL bad-release: message omits release.json"; fail=1; }
python "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-missing-artifact" 2>"$OUT/err" >/dev/null || true
grep -q "tools/generate.py" "$OUT/err" || { echo "FAIL missing-artifact: message omits generate.py"; fail=1; }
python "$HARNESS" --out "$OUT/o.html" --contract "$FIX/1x" 2>"$OUT/err" >/dev/null || true
grep -q "migrate-contract.py" "$OUT/err" || { echo "FAIL 1x: message omits migrate-contract.py"; fail=1; }

if [ "$fail" -eq 0 ]; then echo "ALL GREEN"; exit 0; else echo "SELFTEST FAILED"; exit 1; fi
