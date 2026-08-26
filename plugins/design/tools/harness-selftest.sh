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

# Same treatment for node, which runs the runtime check below. No escape hatch: the only
# caller of this selftest is tools/eval/design-harness.mjs, itself running under node — a
# SKIP would cover no real case and would reopen the green-without-checking door that the
# runtime check exists to close.
NODE=${HARNESS_SELFTEST_NODE:-}
if [ -z "$NODE" ]; then NODE=$(command -v node || true); fi
if [ -z "$NODE" ] || ! command -v "$NODE" >/dev/null 2>&1; then
  echo "SELFTEST FAILED: no usable node (tried '${NODE:-node}')."
  echo "  Install node, or point HARNESS_SELFTEST_NODE at an interpreter."
  exit 1
fi
RUNTIME="$DIR/tools/harness-runtime-check.mjs"

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
# The stylesheet is inlined verbatim: a declared artifact reaching outside the contract
# directory, or one carrying a </style>, is a refusal — not something to sanitise.
check "2x-artifact-escape"  2 --contract "$FIX/2x-artifact-escape"
check "2x-style-breakout"   2 --contract "$FIX/2x-style-breakout"
check "1x"                  3 --contract "$FIX/1x"

# ─── Pages path — every malformed input is a 2, never a traceback ────────────
printf '%s' '{{{ not json' >"$OUT/bad.json"
printf '%s' '["home","contact"]' >"$OUT/strings.json"
printf '%s' '{"pages":[{"key":"home","label":"Accueil","theme":42}]}' >"$OUT/bad-meta.json"
check "pages-json-absent"     2 --pages-json "$OUT/does-not-exist.json"
check "pages-json-not-json"   2 --pages-json "$OUT/bad.json"
check "pages-json-strings"    2 --pages-json "$OUT/strings.json"
check "pages-json-bad-meta"   2 --pages-json "$OUT/bad-meta.json"
check "pages-duplicate-key"   2 --pages "home:A,home:B"
check "pages-fn-collision"    2 --pages "my-page:A,my_page:B"
check "pages-url-path"        2 --pages "/contact/:C"

# ─── Generated HTML ──────────────────────────────────────────────────────────
"$PY" "$HARNESS" --out "$OUT/c.html" --contract "$FIX/2x" >/dev/null 2>&1
"$PY" "$HARNESS" --out "$OUT/s.html" >/dev/null 2>&1
"$PY" "$HARNESS" --out "$OUT/m.html" --pages "home:Accueil,contact:Contact" >/dev/null 2>&1
"$PY" "$HARNESS" --out "$OUT/x.html" --pages "p1:Fiche <b>x</b>" >/dev/null 2>&1
printf '%s' '{"pages":[{"key":"home","label":"Accueil","route":"/","source":"pages/index.vue"},{"key":"companies","label":"Entreprises","route":"/entreprises","source":"pages/entreprises/index.vue","theme":"entreprise"}]}' >"$OUT/meta.json"
"$PY" "$HARNESS" --out "$OUT/meta.html" --contract "$FIX/2x" --pages-json "$OUT/meta.json" >/dev/null 2>&1

if grep -q "GENERATED from tokens.json" "$OUT/c.html"; then
  echo "ok   2x: stylesheet inlined"
else
  echo "FAIL 2x: stylesheet banner not inlined"; fail=1
fi

if grep -q "route: /entreprises" "$OUT/meta.html" &&
   grep -q "source: pages/entreprises/index.vue" "$OUT/meta.html" &&
   grep -q "theme: entreprise" "$OUT/meta.html"; then
  echo "ok   page grounding copied into the LLM framing"
else
  echo "FAIL page route/source/theme missing from LLM framing"; fail=1
fi
if grep -q "\[fixture-icons\] Use the declared icon set" "$OUT/meta.html"; then
  echo "ok   frozen usage rule copied into the LLM framing"
else
  echo "FAIL frozen usage rule missing from LLM framing"; fail=1
fi
if grep -q "AUTHOR PAGE STYLES" "$OUT/meta.html" &&
   grep -q "Modifie uniquement les deux zones auteur" "$OUT/meta.html"; then
  echo "ok   LLM edit scope names both author-owned regions"
else
  echo "FAIL LLM edit scope is missing or contradictory"; fail=1
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
# The escape message must print the RESOLVED path — the raw "../…" is what the contract
# claims, the resolved one is what proves the escape.
"$PY" "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-artifact-escape" 2>"$OUT/err" >/dev/null || true
grep -q "policies.json" "$OUT/err" || { echo "FAIL artifact-escape: message omits policies.json"; fail=1; }
grep -q "\.\./2x" "$OUT/err" && { echo "FAIL artifact-escape: message prints the raw path, not the resolved one"; fail=1; }
"$PY" "$HARNESS" --out "$OUT/o.html" --contract "$FIX/2x-style-breakout" 2>"$OUT/err" >/dev/null || true
grep -q "adapters.tokens.css" "$OUT/err" || { echo "FAIL style-breakout: message omits the stylesheet"; fail=1; }
# A refusal precedes the write; it does not repair one. Nothing produced may carry the payload.
if grep -rq "__PWNED" "$OUT" 2>/dev/null; then
  echo "FAIL the style-breakout payload reached a produced file"; fail=1
else
  echo "ok   the style-breakout payload reaches no output"
fi

# ─── Runtime ─────────────────────────────────────────────────────────────────
# Everything above asserts on the TEXT of the generated file. A generator emitting a
# syntactically dead <script> satisfies all of it: measured on a copy with an unbalanced
# brace in setViewport, this selftest printed ALL GREEN / exit 0 while the produced file
# answered `typeof setPage === "undefined"` in a browser. The JS is now executed.
for f in m.html c.html s.html meta.html; do
  case "$f" in
    m.html) args="--expect-pages home,contact" ;;
    meta.html) args="--expect-pages home,companies" ;;
    *)      args="" ;;
  esac
  # shellcheck disable=SC2086
  if "$NODE" "$RUNTIME" "$OUT/$f" $args; then :; else
    echo "FAIL runtime check on $f"; fail=1
  fi
done

# ─── Three-branch page-key invariant ─────────────────────────────────────────
# Registry, <option value> and the oracle's reference_page are one set written by three
# hands. Asserting only that a conformant file passes proves nothing: each branch is
# mutated in turn and the check must go RED. A green that no mutation can turn red is
# the defect this whole file exists against.
printf '%s' '{"reference_page":"contact","targets":[]}' >"$OUT/oracle-ok.json"
printf '%s' '{"reference_page":"nowhere","targets":[]}' >"$OUT/oracle-bad.json"
printf '%s' '{"reference_page":null,"targets":[]}'      >"$OUT/oracle-null.json"

# The registry key is renamed alone — the <option> still offers "contact".
sed 's/^    "contact": pageContact,/    "contactez": pageContact,/' "$OUT/m.html" >"$OUT/mut-registry.html"
# The <option> value is renamed alone — the registry still declares "contact".
sed 's/<option value="contact">/<option value="contacts">/' "$OUT/m.html" >"$OUT/mut-option.html"

invariant() {  # name expect(pass|fail) <runtime args…>
  name=$1; want=$2; shift 2
  if "$NODE" "$RUNTIME" "$@" >/dev/null 2>"$OUT/err"; then got=pass; else got=fail; fi
  if [ "$got" = "$want" ]; then
    echo "ok   invariant $name: $got"
  else
    echo "FAIL invariant $name: $got, expected $want"; cat "$OUT/err"; fail=1
  fi
}

# Each mutation must actually differ from the source, or the test asserts on a no-op.
cmp -s "$OUT/m.html" "$OUT/mut-registry.html" && { echo "FAIL registry mutation is a no-op"; fail=1; }
cmp -s "$OUT/m.html" "$OUT/mut-option.html"   && { echo "FAIL option mutation is a no-op"; fail=1; }

invariant "conformant"        pass "$OUT/m.html"
invariant "registry-renamed"  fail "$OUT/mut-registry.html"
invariant "option-renamed"    fail "$OUT/mut-option.html"
invariant "oracle-known"      pass "$OUT/m.html" --oracle-config "$OUT/oracle-ok.json"
invariant "oracle-unknown"    fail "$OUT/m.html" --oracle-config "$OUT/oracle-bad.json"
invariant "oracle-null"       pass "$OUT/m.html" --oracle-config "$OUT/oracle-null.json"
invariant "oracle-absent"     fail "$OUT/m.html" --oracle-config "$OUT/no-such-config.json"

if [ "$fail" -eq 0 ]; then echo "ALL GREEN"; exit 0; else echo "SELFTEST FAILED"; exit 1; fi
