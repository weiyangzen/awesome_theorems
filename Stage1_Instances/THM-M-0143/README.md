# THM-M-0143: Nakajima quiver varieties

## Status

This is a rev-5.6 `planned` intake. The repository gloss, "construction of moduli spaces of
quiver representations," describes a mathematical construction rather than a uniquely quantified
theorem. The exact-statement gate is therefore open (`H5 / M4 / R3`), and the untrusted historical
"verified" label supplies no proof credit.

## Scope

The discovery scope is Nakajima's quiver-variety construction introduced in the 1994 paper
identified in the source crosswalk. The construction depends on quiver and dimension data,
moment-map equations, a stability choice, and a quotient convention. None is specified by the
repository metadata. This target is not silently merged with adjacent `THM-M-0142`, "Nakajima
geometry." See [scope_map.md](scope_map.md) and
[source_statement_crosswalk.md](source_statement_crosswalk.md).

## Open task DAG

1. `S56-M-0143-STATEMENT`: select and pinpoint an exact source proposition; freeze its complete
   construction data, binders, hypotheses, conclusion, boundary cases, and Lean expression.
2. `S56-M-0143-ANCHOR_AUDIT`: audit pinned mathlib and external Lean candidates after statement
   selection.
3. `S56-M-0143-OBLIGATION_TREE`: freeze typed obligation and provenance graphs.
4. `S56-M-0143-PROOF`: implement or pin/import exact proof bodies.
5. `S56-M-0143-VALIDATION`: run kernel, trust, provenance, and replay gates.
6. `S56-M-0143-RELEASE`: reconcile accepted evidence; only the integration lane may accept it.

No dependent task has proof credit. The first blocker is that the metadata names a construction,
not an exact proposition.
