# S56-M-0527-PROOF blocker

Verdict: `blocked`; no proof closure or item completion is claimed.

## First failed gate

The frozen root requires construction, for every subgroup of the fundamental
group of an arbitrary path-connected, locally path-connected, semilocally
simply connected space, of a connected covering whose induced subgroup is
exactly that subgroup. The pinned mathlib revision has no such construction.
The strongest relevant declaration,
`IsCoveringMap.existsUnique_continuousMap_lifts_of_range_le`, starts from two
already-constructed covering spaces and therefore cannot discharge the
root-critical cut set `M0527-EX-COVER` and `M0527-EX-RANGE`.

This is not a missing import or a theorem-name mismatch. Implementing the
missing construction requires the path-class quotient, its topology,
representative-independent evenly-covered charts, connectedness, and both
subgroup-range inclusions frozen as open obligations in
`obligation-registry.json`. No placeholder-free implementation of those
objects exists in this clone or the pinned dependency closure. The external
candidate recorded in `anchor-audit.md` has a literal `by sorry` body and is
inadmissible.

## Attempted narrow route

I attempted the dependency-legal fiber-injectivity route using the pinned
lifting criterion: equal subgroup ranges should provide lifts between two
existing covers, uniqueness should make the lifts inverse, and the two
continuous maps should form a homeomorphism. This exposed two additional
nontrivial bridge obligations already anticipated by the frozen graph:

1. derive `LocPathConnectedSpace P.E` for a cover over a locally
   path-connected base, since the lifting theorem requires that instance and
   `PointedConnectedCover` does not store it;
2. reconcile the range of `FundamentalGroup.map p P.e0` used by the lifting
   criterion with the transported range of `FundamentalGroup.mapOfEq` used by
   the frozen `inducedSubgroup` definition.

The experiment did not elaborate and was deleted. It is not retained or
credited as proof content. Closing only this route would still leave the
surjectivity/construction half of the exact root open.

## Commands and exact results

Commands ran from the worker clone on 2026-07-12 at base revision
`e1e156a5ecde6311a98efe69be284ba9e7d11414`.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` (15 assurance groups, 1546 uniform-L0 Lean 4 targets) |
| `python3 scripts/stage1_target.py check` | 0 | `ok` (1546 unique targets, ranks 1..1546, all L0/rework-required) |
| `python3 scripts/stage1_target.py show THM-M-0527` | 0 | rank 584, lifecycle `planned`, theorem incomplete |
| `rg -n -i 'classification|subgroup.*fundamental|covering.*subgroup' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology` | 0 | no exact classification or arbitrary-subgroup cover construction found; only quotient-cover special cases |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0527/Proof.lean)` | 1 | experimental fiber proof failed at local path-connectedness and `map`/`mapOfEq` range transport; file deleted |

No `lake update`, build, clone, fetch, or `.lake` mutation was performed. Retry
requires a placeholder-free implementation of the construction cut set (or a
pinned exact external proof with audited terminal bodies), followed by the
fiber bridge lemmas above and exact root composition. Because the assigned
proof phase is not self-tested or complete, no `.stage1-worker-selftest.json`
is emitted.
