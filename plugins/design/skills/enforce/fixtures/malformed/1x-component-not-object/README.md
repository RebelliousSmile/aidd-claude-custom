# 1x-component-not-object

components.json: the value of component `btn` is a string, not an object. Untouched, `comp.items()` raises AttributeError and the run exits 1.

Expected: exit 2, naming the file and the field. No release.json: this is a 1.x contract on purpose.
