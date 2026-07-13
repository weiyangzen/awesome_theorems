# THM-M-0041 formal anchor audit

Item: `S56-M-0041-ANCHOR_AUDIT`

## Exact pinned candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Matrix.aeval_self_charpoly` is an exact candidate for the frozen target. Mathlib defines
`Matrix.charmatrix A` as `scalar n X - A.map C` and `Matrix.charpoly A` as its determinant.
`AnchorAudit.lean` checks by `rfl` that this is the dossier's expanded
`det (X I - A)` polynomial, then kernel-checks the entire quantified target through a local
wrapper. The scoped validator also composes `Statement.lean` and `AnchorAudit.lean` in one temporary
Lean module and checks both a definitional equality to the actual statement declaration and a
wrapper having that declaration as its type. The scope includes arbitrary commutative rings, empty
finite index types, and zero rings.

The terminal proof body is in pinned mathlib, not this repository. It applies the adjugate identity,
transports the polynomial matrix identity through `matPolyEquiv`, and evaluates the right factor
`X - C A` at `A`. Lean reports `[propext, Classical.choice, Quot.sound]` for both the upstream
declaration and audit wrapper. The route would be `M0-W` only after release-grade `E1` and master
acceptance. This provisional worker check therefore retains machine status `M3` until the integration
lane and downstream composition, trust, and release gates accept it.

## Related and external candidates

`LinearMap.aeval_self_charpoly` is not a second proof. It concerns finite free modules, chooses a
basis, and terminates at `Matrix.aeval_self_charpoly`; it is retained only as a related encoding.

Bounded public searches found no independent exact Lean 4 terminal body. Atlas has a placeholder-
free entrywise theorem for `2 x 2` matrices over `ZMod n`, but that strict special case cannot
replace the universal target. Automath uses mathlib's theorem to derive a complex trace recurrence
and likewise contributes no independent Cayley-Hamilton body. Neither external project was fetched,
installed, or credited. Exact revisions, source hashes, toolchains, manifests, licenses, query
hashes, and access limitations are recorded in `anchor-audit.json`.

## Boundary

The frozen four-record inventory is classified, not globally exhaustive. The statement prerequisite
and this node await master acceptance. A canonical obligation registry, proof-node composition,
full transitive provenance and TCB closure, primary-source `H0`, readable `R0`, hermetic replay,
independent verification, `AUDIT-Z`, and theorem completion all remain open.
