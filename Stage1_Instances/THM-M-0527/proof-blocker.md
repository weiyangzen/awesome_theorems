# S56-M-0527-PROOF boundary

Verdict: substantive partial proof self-tested; the exact root remains blocked
and no accepted state or theorem completion is claimed.

## Implemented branch

`Proof.lean` now proves the complete fiber criterion for two existing pointed
connected covers. It derives local path-connectedness of covering total
spaces, applies the subgroup-range lifting criterion in both directions,
uses lift uniqueness to obtain mutual inverses, builds the homeomorphism over
the base, and proves the reverse implication through an explicit induced-map
naturality square and subgroup-range calculation.

The exact theorem `inducedSubgroup_eq_iff_isomorphic` matches the frozen
`M0527-FIB` formal target. Nevertheless, all ten fiber obligation
fingerprints remain planned signatures with no predecessor composition
receipt. This worker therefore claims partial progress toward those nodes and
zero complete frozen obligations pending integration reconciliation.

## First failed gate

`M0527-EX-COVER` remains open. The exact root requires, for every subgroup of
the fundamental group, a connected covering whose induced subgroup is that
subgroup. Pinned mathlib has no arbitrary-subgroup construction. The strongest
relevant lifting declaration starts with an already-constructed cover and
cannot build the path-class quotient, its topology, representative-independent
evenly-covered charts, or connectedness. `M0527-EX-RANGE` consequently also
remains open.

The Atlas candidate audited at an immutable revision contains a literal
`by sorry`. A separately inspected placeholder-free universal-cover project
constructs only the universal/bottom-subgroup case and has no quotient by an
arbitrary subgroup. Neither is an admissible exact root proof.

## Retry condition

Implement the arbitrary-subgroup path-class covering and both induced-range
inclusions without placeholders, or integrate an immutable exact external
proof with audited terminal bodies. Then reconcile exact obligation
fingerprints and composition receipts before validation or release. The
predecessor typed graph remains an immutable snapshot and still lists
`M0527-FIB` in its cut set; it was not edited by this proof worker.

Validation details and exact commands are in `proof-validation.md`. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.
