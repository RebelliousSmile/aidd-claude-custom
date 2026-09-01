#!/usr/bin/env bash
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PY=${WIREFRAMES_SELFTEST_PYTHON:-}
if [ -z "$PY" ]; then
  if command -v python3 >/dev/null 2>&1; then PY=python3
  elif command -v python >/dev/null 2>&1; then PY=python
  else echo "FAIL wireframes-selftest: python introuvable" >&2; exit 1
  fi
fi
if ! command -v "$PY" >/dev/null 2>&1; then echo "FAIL wireframes-selftest: interpréteur inutilisable: $PY" >&2; exit 1; fi

GEN="$ROOT/adapters/wireframes/wireframes.py"
APPLY="$ROOT/tools/wireframes-apply.py"
LINT="$ROOT/tools/wireframes-lint.py"
FIX="$ROOT/adapters/wireframes/fixtures"
OUT=$(mktemp -d)
trap 'rm -rf "$OUT"' EXIT
fail=0

ok() { echo "ok   $1"; }
bad() { echo "FAIL $1" >&2; fail=1; }

if "$PY" "$GEN" --manifest "$FIX/manifest-valid.json" --out "$OUT/shell.html" >/dev/null &&
   "$PY" "$APPLY" --shell "$OUT/shell.html" --payload "$FIX/payload-valid.json" --out "$OUT/board.html" >/dev/null &&
   "$PY" "$LINT" "$OUT/board.html" --report "$OUT/report.json"; then ok "canonical generation/application/static lint"
else bad "canonical generation/application/static lint"; fi

if "$PY" "$GEN" --manifest "$FIX/manifest-valid.json" --out "$OUT/shell-2.html" >/dev/null && cmp -s "$OUT/shell.html" "$OUT/shell-2.html"; then
  ok "generation is deterministic"
else bad "generation is not deterministic"; fi

"$PY" "$GEN" --manifest "$FIX/manifest-invalid.json" --out "$OUT/invalid.html" >/dev/null 2>"$OUT/err"
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/invalid.html" ] && grep -q 'unknown manifest field' "$OUT/err"; then ok "invalid manifest writes nothing"
else bad "invalid manifest handling"; fi

sed '0,/<article class="locker-card"/s//<aside data-wireframe-annotation>Un texte suffisamment long pour dépasser très largement les soixante caractères autorisés<\/aside><article class="locker-card"/' "$OUT/board.html" >"$OUT/annotation.html"
"$PY" "$LINT" "$OUT/annotation.html" --report "$OUT/annotation.json"
got=$?
if [ "$got" -eq 1 ] && grep -q 'annotation-length' "$OUT/annotation.json"; then ok "annotation limits fail closed"
else bad "annotation limits"; fi

sed '0,/<\/head>/s//<link rel="stylesheet" href="https:\/\/example.test\/x.css"><\/head>/' "$OUT/board.html" >"$OUT/external.html"
"$PY" "$LINT" "$OUT/external.html" --report "$OUT/external.json"
got=$?
if [ "$got" -eq 1 ] && grep -q 'external-resource' "$OUT/external.json"; then ok "external resources fail closed"
else bad "external resource lint"; fi

sed '0,/data-wireframe-element="heading"/s///' "$OUT/board.html" | sed '0,/<h4 >/s//<h4 id="heading">/' >"$OUT/fixable.html"
"$PY" "$LINT" "$OUT/fixable.html" --fix --fix-out "$OUT/fixed.html" --report "$OUT/fixed.json"
got=$?
if [ "$got" -eq 0 ] && grep -q 'data-wireframe-element:locker-card:available:desktop:heading' "$OUT/fixed.json"; then ok "safe mechanical fix is re-linted"
else bad "safe mechanical fix"; fi

if cmp -s "$FIX/canonical.html" "$OUT/board.html"; then ok "canonical fixture matches generator"
else bad "canonical fixture drift"; fi

if [ "$fail" -eq 0 ]; then echo "ALL GREEN — wireframes static selftest"; exit 0; fi
echo "SELFTEST FAILED" >&2
exit 1
