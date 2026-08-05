#!/usr/bin/env sh
# design:harness selftest — proves the exit-code space of the WHOLE program (contract
# path and pages path alike) and the shape of the generated HTML. Every harness.py
# invocation goes through check(), which asserts the expected code AND that the code is
# never 1 — the interdiction, not just the expectation. Exit 0 iff every assertion holds.
#
# POSIX sh only — the shebang is `sh` while the usage line says `bash`, so the script must
# keep running under both: no [[ ]], no arrays, no ${v,,}, no local.
#
# Usage:  cd plugins/design && bash tools/harness-selftest.sh
set -u

DIR=$(CDPATH= cd "$(dirname "$0")/.." && pwd)
HARNESS="$DIR/adapters/harness/harness.py"
FIX="$DIR/adapters/harness/fixtures"
OUT=$(mktemp -d)
trap 'rm -rf "$OUT"' EXIT
fail=0

# The interpreter is resolved, never assumed: Ubuntu 22+ ships `python3` only, and a
# missing `python` returns 127 on every check — an interpreter defect wearing the mask of
# a failed assertion. A proof that only holds where it was written is not a proof.
PY=${HARNESS_SELFTEST_PYTHON:-}
if [ -z "$PY" ]; then PY=$(command -v python3 || command -v python || true); fi
# The override is checked too: an unusable HARNESS_SELFTEST_PYTHON would return 127 on
# every check and reproduce the very defect this guard removes.
if [ -z "$PY" ] || ! command -v "$PY" >/dev/null 2>&1; then
  echo "SELFTEST FAILED: no usable python (tried '${PY:-python3, python}')."
  echo "  Install python3, or point HARNESS_SELFTEST_PYTHON at an interpreter."
  exit 1
fi

check() {  # name expected_code <harness args…>
  name=$1; want=$2; shift 2
  "$PY" "$HARNESS" --out "$OUT/o.html" "$@" >"$OUT/out" 2>"$OUT/err"
  got=$?
  # The interdiction, checked on every branch: 1 is not in the harness code space
  # (0/2/3). Asserting only the expected code is what let a dead file ship green.
  if [ "$got" -eq 1 ]; then
    echo "FAIL $name: exit 1 — harness.py never emits 1 (space is 0/2/3)"; cat "$OUT/err"; fail=1
  elif [ "$got" -ne "$want" ]; then
    echo "FAIL $name: exit $got, expected $want"; cat "$OUT/err"; fail=1
  else
    echo "ok   $name: exit $got"
  fi
}

# ─── Contract path ───────────────────────────────────────────────────────────
check "scaffold"            0
check "2x"                  0 --contract "$FIX/2x"
check "2x-no-stylesheet"    0 --contract "$FIX/2x-no-stylesheet"
check "2x-missing-artifact" 2 --contract "$FIX/2x-missing-artifact"
check "2x-bad-release"      2 --contract "$FIX/2x-bad-release"
check "1x"                  3 --contract "$FIX/1x"

# ─── Pages path — every malformed input is a 2, never a traceback ────────────
printf '%s' '{{{ not json' >"$OUT/bad.json"
printf '%s' '["home","contact"]' >"$OUT/strings.json"
check "pages-json-absent"     2 --pages-json "$OUT/does-not-exist.json"
check "pages-json-not-json"   2 --pages-json "$OUT/bad.json"
check "pages-json-strings"    2 --pages-json "$OUT/strings.json"
check "pages-duplicate-key"   2 --pages "home:A,home:B"
check "pages-fn-collision"    2 --pages "my-page:A,my_page:B"
check "pages-url-path"        2 --pages "/contact/:C"

# ─── Generated HTML ──────────────────────────────────────────────────────────
"$PY" "$HARNESS" --out "$OUT/c.html" --contract "$FIX/2x" >/dev/null 2>&1
"$PY" "$HARNESS" --out "$OUT/s.html" >/dev/null 2>&1
"$PY" "$HARNESS" --out "$OUT/m.html" --pages "home:Accueil,contact:Contact" >/dev/null 2>&1
"$PY" "$HARNESS" --out "$OUT/x.html" --pages "p1:Fiche <b>x</b>" >/dev/null 2>&1

if grep -q "GENERATED from tokens.json" "$OUT/c.html"; then
  echo "ok   2x: stylesheet inlined"
else
  echo "FAIL 2x: stylesheet banner not inlined"; fail=1
fi

# The no-stylesheet contract must emit exactly one stderr warning.
"$PY" "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-no-stylesheet" 2>"$OUT/err" >/dev/null
n=$(grep -c "Warning" "$OUT/err")
if [ "$n" -eq 1 ]; then echo "ok   2x-no-stylesheet: one warning"; else echo "FAIL warning count $n"; fail=1; fi

# No @media anywhere — the device model is class-based samples only.
if grep -q "@media" "$OUT/s.html" "$OUT/c.html"; then
  echo "FAIL @media present in generated output"; fail=1
else
  echo "ok   no @media in scaffold or coupled output"
fi

# The device bezel is painted OUTSIDE the box. As a border it would sit inside
# (box-sizing: border-box) and shrink the content box below the declared sample width —
# measured at 375x812, the oracle's real mobile viewport: content 359 instead of 375,
# and every percentage-derived value charged to a conformant implementation.
if grep -q "outline: 8px" "$OUT/s.html" && grep -q "outline: 10px" "$OUT/s.html"; then
  echo "ok   the device bezel is an outline"
else
  echo "FAIL the device bezel is not an outline"; fail=1
fi
# border-radius stays legitimate; a shorthand `border:` on either device rule does not.
if grep -E "^  \.preview-frame\.(tablet|mobile) \{" "$OUT/s.html" | grep -q "border:"; then
  echo "FAIL a border: came back on a device frame — it shrinks the content box"; fail=1
else
  echo "ok   no border: on the device frames"
fi

# The scaffold honours the heading rule it states. Asserting "an <h1 exists somewhere"
# is not enough — the error block carries one, so a placeholder demoted back to <h2>
# would still pass. Every .ph block must OPEN on an h1.
blocks=$(grep -o "<div class=\"ph[a-z -]*\"><h[0-9]" "$OUT/s.html")
nb=$(printf '%s\n' "$blocks" | grep -c "<h")
bad=$(printf '%s\n' "$blocks" | grep -v "<h1$")
if [ "$nb" -lt 3 ]; then
  echo "FAIL $nb .ph block(s) found, expected the 3 scaffold states"; fail=1
elif [ -n "$bad" ]; then
  echo "FAIL a .ph block opens on something other than h1: $bad"; fail=1
else
  echo "ok   every .ph block opens on an h1"
fi

# Two page keys may never derive the same function name — a duplicate would silently
# shadow a page in the registry. Only the GENERATED declarations count: the LLM framing
# above the registry shows `function pageHome()` as an example, in a comment.
decls=$(grep -o "^  function page[A-Za-z0-9_]*" "$OUT/m.html")
n=$(printf '%s\n' "$decls" | grep -c "function page")
dups=$(printf '%s\n' "$decls" | sort | uniq -d)
if [ "$n" -ne 2 ]; then
  echo "FAIL 2 pages requested, $n page function(s) declared"; fail=1
elif [ -n "$dups" ]; then
  echo "FAIL duplicate page function: $dups"; fail=1
else
  echo "ok   page functions declared once each"
fi

# A label carrying markup must never come back out as a tag, in the <option> or the page.
if grep -q "<b>" "$OUT/x.html"; then
  echo "FAIL markup label re-emitted as a tag"; fail=1
else
  echo "ok   markup label escaped everywhere"
fi

# Chrome named for a screen reader.
if grep "id=\"page-select\"" "$OUT/s.html" | grep -q "aria-label"; then
  echo "ok   #page-select is labelled"
else
  echo "FAIL #page-select has no aria-label"; fail=1
fi
# The attribute, not the setAttribute() that maintains it — hence the trailing quote.
n=$(grep -o "aria-pressed=\"" "$OUT/s.html" | wc -l)
if [ "$n" -eq 3 ]; then echo "ok   3 aria-pressed on the device buttons"; else echo "FAIL aria-pressed count $n, expected 3"; fail=1; fi

# A file sold as standalone issues no third-party request.
if grep -q "preconnect" "$OUT/s.html"; then
  echo "FAIL scaffold still preconnects to a third party"; fail=1
else
  echo "ok   no preconnect in scaffold"
fi

# No %%SENTINEL%% survives into the output. A dropped or misspelled key would otherwise
# ship the literal sentinel in the HTML at exit 0 — a dead file at green, one level up.
if grep -q "%%" "$OUT/s.html" "$OUT/c.html"; then
  echo "FAIL an unfilled %%SENTINEL%% reached the output"; grep -o "%%[A-Za-z_]*%%" "$OUT/s.html" "$OUT/c.html"; fail=1
else
  echo "ok   every sentinel filled"
fi

# decodeURIComponent THROWS on a malformed fragment: outside the try, the URIError
# aborts init() before render() and leaves #page-container empty — blank, no error block.
if grep -B1 "const hash = decodeURIComponent" "$OUT/s.html" | grep -q "try {"; then
  echo "ok   the hash is decoded inside init()'s try"
else
  echo "FAIL decodeURIComponent sits outside init()'s try"; fail=1
fi

# The bad-release message must name release.json; missing-artifact must name generate.py;
# 1x must name migrate-contract.py; an invalid page set must name the offending key.
"$PY" "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-bad-release" 2>"$OUT/err" >/dev/null || true
grep -q "release.json" "$OUT/err" || { echo "FAIL bad-release: message omits release.json"; fail=1; }
"$PY" "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-missing-artifact" 2>"$OUT/err" >/dev/null || true
grep -q "tools/generate.py" "$OUT/err" || { echo "FAIL missing-artifact: message omits generate.py"; fail=1; }
"$PY" "$HARNESS" --out "$OUT/o.html" --contract "$FIX/1x" 2>"$OUT/err" >/dev/null || true
grep -q "migrate-contract.py" "$OUT/err" || { echo "FAIL 1x: message omits migrate-contract.py"; fail=1; }
"$PY" "$HARNESS" --out "$OUT/o.html" --pages "/contact/:C" 2>"$OUT/err" >/dev/null || true
grep -q "/contact/" "$OUT/err" || { echo "FAIL url-path: message omits the offending key"; fail=1; }

if [ "$fail" -eq 0 ]; then echo "ALL GREEN"; exit 0; else echo "SELFTEST FAILED"; exit 1; fi
