# 1x-root-not-object

components.json: the 1.x manifest root is an array, not an object. Untouched, `manifest.get("mode")` raises AttributeError and the run exits 1.

Expected: exit 2, naming the file and the field. No release.json: this is a 1.x contract on purpose.
