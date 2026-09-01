# Sourcing HTML from a published Claude Artifact

When the source for `normalize` is the raw HTML of a claude.ai Artifact (view-page source, saved file, or `Artifact` `read`), the bytes are not the author's document alone. claude.ai wraps the published content in its own viewer chrome — navigation, styling, and JS the viewer needs to render and version the page — before the author's own head/body begins.

## Preamble shape

The file opens with the viewer's own markup (its `<!doctype html>`, `<head>`, scripts, and styling), then the author's actual document starts partway through: a `<meta charset` tag and/or a small CSS reset introduce the author's own `<head>` content, immediately followed by the viewer-inserted `</head><body>` boundary and the author's `<body>` content.

## Delimitation heuristic

Locate the author's `<meta charset` tag (or, if absent, the small reset-CSS block that plays the same role) — this is where the viewer chrome ends and the author's own `<head>` begins. Keep everything from that point onward, through the `</head><body>` boundary and the rest of the document. Discard everything before it.

## Why this stays manual

The viewer chrome is third-party markup: unversioned, not part of any contract this plugin governs, and free to change shape between claude.ai releases. An automated strip would guess at a boundary pattern that can silently fail in either direction — leaving chrome in the extracted content (which `normalize`/`lint` would then have to reason about as if the author wrote it), or cutting into the author's own head/body (silently truncating real content). Neither failure trips a validator; `wireframes-analyze.py` sees well-formed HTML either way. A human doing the cut visually confirms the boundary once, which no tool in this plugin does automatically.

## Manual extraction recipe

Confirm the `<meta charset` (or reset-CSS) line by eye, then cut from there to end of file. A one-liner, run once per source before feeding it to `wireframes-analyze.py`:

```
python -c "
import sys
text = open(sys.argv[1], encoding='utf-8').read()
marker = '<meta charset'
index = text.index(marker)
open(sys.argv[2], 'w', encoding='utf-8').write(text[index:])
" artifact-raw.html artifact-source.html
```

Inspect `artifact-source.html` before running `normalize` on it — confirm it starts at the author's own `<head>` content and that no author markup was cut.
