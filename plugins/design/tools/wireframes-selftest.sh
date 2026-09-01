#!/usr/bin/env bash
set -u
export PYTHONUTF8=1

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
ANALYZE="$ROOT/tools/wireframes-analyze.py"
REVIEW="$ROOT/tools/wireframes-review.py"
HANDOFF="$ROOT/tools/wireframes-handoff.py"
HARNESS_GEN="$ROOT/adapters/harness/harness.py"
HARNESS_APPLY="$ROOT/tools/harness-apply.py"
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

source_hash=$($PY -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$FIX/normalize-document.html")
if "$PY" "$ANALYZE" "$FIX/normalize-document.html" --out "$OUT/document-inventory.json" >/dev/null &&
   "$PY" "$ANALYZE" "$FIX/normalize-fragment.html" --out "$OUT/fragment-inventory.json" >/dev/null &&
   "$PY" "$ANALYZE" "$FIX/normalize-states.html" --out "$OUT/normalize-states.json" >/dev/null &&
   grep -q '"classification": "html-document"' "$OUT/document-inventory.json" &&
   grep -q '"classification": "html-fragment"' "$OUT/fragment-inventory.json" &&
   grep -q '"classification": "canonical-wireframe"' "$OUT/normalize-states.json"; then ok "normalization classifies documents, fragments and canonical boards"
else bad "normalization classification"; fi

"$PY" "$ANALYZE" "$FIX/normalize-ambiguous.html" --out "$OUT/ambiguous-inventory.json" >/dev/null
got=$?
if [ "$got" -eq 1 ] && grep -q 'unit-and-state-mapping' "$OUT/ambiguous-inventory.json"; then ok "ambiguous normalization stops after inventory"
else bad "ambiguous normalization"; fi

if "$PY" "$ANALYZE" "$FIX/normalize-annotation-heavy.html" --out "$OUT/annotation-inventory.json" >/dev/null &&
   grep -q '"annotations": 3' "$OUT/annotation-inventory.json" && grep -q 'resource-dependency-omission' "$OUT/annotation-inventory.json"; then ok "analysis inventories annotations and missing dependencies"
else bad "annotation/dependency inventory"; fi

if grep -q 'annotation-contract-risk' "$OUT/annotation-inventory.json" && grep -q '"index"' "$OUT/annotation-inventory.json"; then ok "annotation citing a commit hash or file path is flagged as a contract risk"
else bad "annotation contract risk detection"; fi

if "$PY" "$ANALYZE" "$FIX/normalize-tabbed.html" --out "$OUT/tabbed-inventory.json" >/dev/null &&
   grep -q 'section.app-view' "$OUT/tabbed-inventory.json" && grep -q '"trigger"' "$OUT/tabbed-inventory.json" && ! grep -q 'div.container' "$OUT/tabbed-inventory.json"; then
  ok "structurally similar toggled siblings populate unitCandidates and transitionCandidates, generic classes do not"
else bad "structural sibling grouping"; fi

"$PY" -c 'import json,sys; p=sys.argv[1]; x=json.load(open(p)); [b.update(disposition="preserved") for b in x["inventory"]["blocks"]]; open(p,"w").write(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+"\n")' "$OUT/document-inventory.json"
if "$PY" "$APPLY" --shell "$OUT/shell.html" --payload "$FIX/payload-valid.json" --inventory "$OUT/document-inventory.json" --out "$OUT/normalized.html" >/dev/null &&
   "$PY" "$LINT" "$OUT/normalized.html" --report "$OUT/normalized-static.json" >/dev/null &&
   [ "$source_hash" = "$($PY -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$FIX/normalize-document.html")" ]; then ok "reviewed inventory rebuilds without changing source"
else bad "reviewed normalization application"; fi

fake_render() {
  "$PY" -c 'import json,os,sys; p=os.path.realpath(sys.argv[1]); json.dump({"schemaVersion":1,"file":p,"static":{"status":"passed"},"rendered":{"status":"passed","errors":[]},"review":{"status":"required"},"summary":{"validCandidate":True,"errorCount":0}},open(sys.argv[2],"w"),indent=2,sort_keys=True)' "$1" "$2"
}

PAGE="$FIX/normalize-states.html"
"$PY" "$LINT" "$PAGE" --report "$OUT/page-static.json" >/dev/null
fake_render "$PAGE" "$OUT/page-rendered.json"
if "$PY" "$REVIEW" accept --artifact "$PAGE" --static-report "$OUT/page-static.json" --rendered-report "$OUT/page-rendered.json" --reviewer selftest --out "$OUT/receipt.json" >/dev/null; then ok "explicit review writes detached receipt"
else bad "review receipt"; fi

for policy in desktop-derived mobile-derived defer; do
  if "$PY" "$HANDOFF" --artifact "$PAGE" --static-report "$OUT/page-static.json" --rendered-report "$OUT/page-rendered.json" --receipt "$OUT/receipt.json" --tablet-policy "$policy" --out-dir "$OUT/handoff-$policy" >/dev/null &&
     grep -q "\"tabletPolicy\": \"$policy\"" "$OUT/handoff-$policy/handoff.json"; then ok "handoff tablet policy $policy"
  else bad "handoff tablet policy $policy"; fi
done
if grep -q '"invokeHarness": false' "$OUT/handoff-defer/handoff.json" && grep -q '"invokeHarness": true' "$OUT/handoff-desktop-derived/handoff.json"; then ok "defer never claims harness creation"
else bad "tablet policy invocation boundary"; fi

if "$PY" "$HARNESS_GEN" --out "$OUT/harness-shell.html" --pages-json "$OUT/handoff-desktop-derived/pages.json" >/dev/null &&
   "$PY" "$HARNESS_APPLY" --harness "$OUT/harness-shell.html" --payload "$OUT/handoff-desktop-derived/migration-payload.json" --out "$OUT/harness.html" >/dev/null &&
   grep -q 'Votre casier' "$OUT/harness.html"; then ok "non-deferred bundle uses official harness interfaces"
else bad "official harness handoff"; fi

"$PY" "$REVIEW" revoke --receipt "$OUT/receipt.json" --out "$OUT/revoked.json" >/dev/null
"$PY" "$HANDOFF" --artifact "$PAGE" --static-report "$OUT/page-static.json" --rendered-report "$OUT/page-rendered.json" --receipt "$OUT/revoked.json" --tablet-policy defer --out-dir "$OUT/revoked-handoff" >/dev/null 2>&1
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/revoked-handoff" ]; then ok "revoked receipt blocks handoff"
else bad "revoked receipt handling"; fi

cp "$PAGE" "$OUT/stale.html"
"$PY" "$LINT" "$OUT/stale.html" --report "$OUT/stale-static.json" >/dev/null
fake_render "$OUT/stale.html" "$OUT/stale-rendered.json"
"$PY" "$REVIEW" accept --artifact "$OUT/stale.html" --static-report "$OUT/stale-static.json" --rendered-report "$OUT/stale-rendered.json" --reviewer selftest --out "$OUT/stale-receipt.json" >/dev/null
printf '\n<!-- changed after review -->\n' >> "$OUT/stale.html"
"$PY" "$HANDOFF" --artifact "$OUT/stale.html" --static-report "$OUT/stale-static.json" --rendered-report "$OUT/stale-rendered.json" --receipt "$OUT/stale-receipt.json" --tablet-policy defer --out-dir "$OUT/stale-handoff" >/dev/null 2>&1
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/stale-handoff" ]; then ok "stale receipt blocks handoff"
else bad "stale receipt handling"; fi

cp "$OUT/page-rendered.json" "$OUT/changed-rendered.json"
"$PY" "$REVIEW" accept --artifact "$PAGE" --static-report "$OUT/page-static.json" --rendered-report "$OUT/changed-rendered.json" --reviewer selftest --out "$OUT/report-receipt.json" >/dev/null
printf '\n' >> "$OUT/changed-rendered.json"
"$PY" "$HANDOFF" --artifact "$PAGE" --static-report "$OUT/page-static.json" --rendered-report "$OUT/changed-rendered.json" --receipt "$OUT/report-receipt.json" --tablet-policy defer --out-dir "$OUT/changed-report-handoff" >/dev/null 2>&1
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/changed-report-handoff" ]; then ok "changed report invalidates receipt"
else bad "changed report handling"; fi

"$PY" "$LINT" "$FIX/render-valid.html" --report "$OUT/component-static.json" >/dev/null
fake_render "$FIX/render-valid.html" "$OUT/component-rendered.json"
"$PY" "$REVIEW" accept --artifact "$FIX/render-valid.html" --static-report "$OUT/component-static.json" --rendered-report "$OUT/component-rendered.json" --reviewer selftest --out "$OUT/component-receipt.json" >/dev/null
"$PY" "$HANDOFF" --artifact "$FIX/render-valid.html" --static-report "$OUT/component-static.json" --rendered-report "$OUT/component-rendered.json" --receipt "$OUT/component-receipt.json" --tablet-policy defer --out-dir "$OUT/orphan-handoff" >/dev/null 2>&1
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/orphan-handoff" ]; then ok "orphan component blocks handoff"
else bad "orphan component handling"; fi

"$PY" "$HANDOFF" --artifact "$PAGE" --static-report "$OUT/page-static.json" --rendered-report "$OUT/page-rendered.json" --receipt "$OUT/missing-receipt.json" --tablet-policy defer --out-dir "$OUT/missing-review-handoff" >/dev/null 2>&1
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/missing-review-handoff" ]; then ok "missing review blocks handoff"
else bad "missing review handling"; fi

"$PY" "$HANDOFF" --artifact "$PAGE" --static-report "$OUT/page-static.json" --rendered-report "$OUT/page-rendered.json" --receipt "$OUT/receipt.json" --out-dir "$OUT/missing-tablet-handoff" >/dev/null 2>&1
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/missing-tablet-handoff" ]; then ok "missing tablet policy blocks handoff"
else bad "missing tablet policy handling"; fi

sed 's/"disposition":"reference-only"/"disposition":"unresolved"/' "$PAGE" > "$OUT/unresolved.html"
"$PY" "$LINT" "$OUT/unresolved.html" --report "$OUT/unresolved-static.json" >/dev/null
fake_render "$OUT/unresolved.html" "$OUT/unresolved-rendered.json"
"$PY" "$REVIEW" accept --artifact "$OUT/unresolved.html" --static-report "$OUT/unresolved-static.json" --rendered-report "$OUT/unresolved-rendered.json" --reviewer selftest --out "$OUT/unresolved-receipt.json" >/dev/null
"$PY" "$HANDOFF" --artifact "$OUT/unresolved.html" --static-report "$OUT/unresolved-static.json" --rendered-report "$OUT/unresolved-rendered.json" --receipt "$OUT/unresolved-receipt.json" --tablet-policy defer --out-dir "$OUT/unresolved-handoff" >/dev/null 2>&1
got=$?
if [ "$got" -eq 2 ] && [ ! -e "$OUT/unresolved-handoff" ]; then ok "unresolved state blocks handoff"
else bad "unresolved state handling"; fi

sed 's/"disposition":"reference-only"/"disposition":"omitted"/' "$PAGE" > "$OUT/omitted.html"
"$PY" "$LINT" "$OUT/omitted.html" --report "$OUT/omitted-static.json" >/dev/null
fake_render "$OUT/omitted.html" "$OUT/omitted-rendered.json"
"$PY" "$REVIEW" accept --artifact "$OUT/omitted.html" --static-report "$OUT/omitted-static.json" --rendered-report "$OUT/omitted-rendered.json" --reviewer selftest --out "$OUT/omitted-receipt.json" >/dev/null
if "$PY" "$HANDOFF" --artifact "$OUT/omitted.html" --static-report "$OUT/omitted-static.json" --rendered-report "$OUT/omitted-rendered.json" --receipt "$OUT/omitted-receipt.json" --tablet-policy defer --out-dir "$OUT/omitted-handoff" >/dev/null && grep -q '"disposition": "omitted"' "$OUT/omitted-handoff/handoff.json"; then ok "omitted state stays in handoff inventory"
else bad "omitted state disposition"; fi

"$PY" -c 'import sys; p=sys.argv[1]; s=open(sys.argv[2]).read(); old="{\"disposition\":\"reference-only\",\"reason\":\"État conservé comme référence d’intégration\",\"state\":\"confirmed\"}"; new="{\"afterRender\":\"root.dataset.confirmed=\\\"true\\\";\",\"disposition\":\"retained-interactive\",\"state\":\"confirmed\"}"; assert old in s; open(p,"w").write(s.replace(old,new))' "$OUT/interactive.html" "$PAGE"
"$PY" "$LINT" "$OUT/interactive.html" --report "$OUT/interactive-static.json" >/dev/null
fake_render "$OUT/interactive.html" "$OUT/interactive-rendered.json"
"$PY" "$REVIEW" accept --artifact "$OUT/interactive.html" --static-report "$OUT/interactive-static.json" --rendered-report "$OUT/interactive-rendered.json" --reviewer selftest --out "$OUT/interactive-receipt.json" >/dev/null
if "$PY" "$HANDOFF" --artifact "$OUT/interactive.html" --static-report "$OUT/interactive-static.json" --rendered-report "$OUT/interactive-rendered.json" --receipt "$OUT/interactive-receipt.json" --tablet-policy defer --out-dir "$OUT/interactive-handoff" >/dev/null && grep -q 'root.dataset.confirmed' "$OUT/interactive-handoff/migration-payload.json"; then ok "retained state maps to afterRender"
else bad "retained interactive disposition"; fi

if [ "$fail" -eq 0 ]; then echo "ALL GREEN — wireframes static selftest"; exit 0; fi
echo "SELFTEST FAILED" >&2
exit 1
