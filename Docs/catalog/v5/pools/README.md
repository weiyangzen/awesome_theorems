# Stage5 conjecture source-occurrence pools

This directory is an append-only discovery and intake overlay over the frozen
Stage5 `5.6` release. It does not replace `Docs/catalog/v5/Current_Release.json`,
does not allocate `S5-CLM-*` or Stage6 aliases, and does not grant strict
conjecture credit.

The current pool freezes ConjectureBench commit
`357bcb1a1daf93917d42e8206ceaa55645729a09`: 14,865 source occurrences
(302 curated records, 9,342 family instances, and 5,221 extended-catalog
records). These are intake candidates, not 14,865 independently verified,
semantically distinct, currently open conjectures.

`stable_source_key` is the cross-snapshot logical key
`conjecturebench/<kind>/<source_native_id>`. The commit, record path, family
container index and canonical record digest bind the immutable occurrence
version; they never create a second logical source identity by themselves.

The execution order is:

1. bind the exact source occurrence and its rights/status boundary;
2. exactify a truth-apt proposition or a parameterized frontier challenge;
3. independently review current status, importance, rights, and full-catalog
   semantic identity;
4. relate it to an existing Stage5 identity or authorize a future append-only
   catalog/Stage6 migration;
5. only then admit one canonical identity to a proof-resolution TARGET.

Run the deterministic validator with:

```bash
python3 Docs/catalog/v5/tools/build_stage5_conjecture_occurrence_pool.py --check
```
