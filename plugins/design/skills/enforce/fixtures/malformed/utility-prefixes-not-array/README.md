# utility-prefixes-not-array

policies.json: `$utilityPrefixes` is an object, not an array. Untouched, `utilityPrefixes.some(...)` raises under --strict and the run exits 1.

Expected: exit 2, naming the artifact and the field.
