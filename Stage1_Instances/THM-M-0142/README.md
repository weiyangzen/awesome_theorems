# THM-M-0142: Nakajima geometry

## Status

This is a rev-5.6 `planned` intake. The repository's source phrase, “moduli spaces of
quiver representations,” denotes a construction/research area, not a uniquely quantified
theorem. Consequently the exact-statement gate is deliberately open (`H5 / M4 / R3`) and no
historical “verified” label is credited.

## Scope

The discovery scope is Nakajima's 1994 quiver-variety construction and its principal results.
It does not silently substitute the adjacent target `THM-M-0143`, nor does it choose one of the
construction, smoothness, representation, or homology results without source-level adjudication.
See [scope_map.md](scope_map.md) and [source_statement_crosswalk.md](source_statement_crosswalk.md).

## Open task DAG

1. `S56-M-0142-STATEMENT`: select and pinpoint one exact proposition from the primary source;
   freeze binders, hypotheses, conclusion, and degenerate cases; elaborate its Lean expression.
2. `S56-M-0142-ANCHOR_AUDIT`: search pinned mathlib and external Lean projects only after the
   statement is frozen.
3. `S56-M-0142-OBLIGATION_TREE`: freeze typed obligation and provenance graphs.
4. `S56-M-0142-PROOF`: implement or pin/import exact proof bodies.
5. `S56-M-0142-VALIDATION`: run kernel, trust, provenance, and replay gates.
6. `S56-M-0142-RELEASE`: reconcile accepted evidence; integration lane alone decides acceptance.

No child task presently has proof credit. The first blocking condition is identification of an
exact theorem rather than a broad mathematical topic.
