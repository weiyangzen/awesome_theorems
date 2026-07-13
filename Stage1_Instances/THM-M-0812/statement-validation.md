# THM-M-0812 statement validation

Item: `S56-M-0812-STATEMENT`

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44`

Base tree: `050ab5c6392560337051d2eadd1b82277dbe1c4f`

## Frozen target

`Stage1Instances.THM_M_0812.KonigMatchingCoverTarget` states Konig's equality for finite
bipartite graphs in a two-sorted incidence encoding. `L` and `R` are finite vertex-side types,
`E` is an independently finite edge-identity type, and `left` and `right` give every edge its two
endpoints. This represents parallel edges rather than silently specializing the source to simple
graphs. A matching is a set on which both endpoint maps are injective. The maximum and minimum are
encoded by an attained witness and a universal bound, and matching size counts edges.

The direct imports are `Mathlib.Data.Finite.Card` and `Mathlib.Data.Set.Card`. The canonical
definitions and checked transports elaborate with both; removing either from that fixture fails.
The checked iff
`konigMatchingCoverTarget_iff_expanded` binds the named predicates to their binder-complete
expansion. The checked iff `konigMatchingCoverTarget_iff_simpleRelationKonigTarget` proves that
erasing parallel-edge identity preserves the matching and cover extrema, including across the
fixed edge universe via finite equivalences and `ULift`. The expression fingerprint also hashes a
serialization bundle containing all four support definitions and the credited simple-relation
alternate, so changing a named extremum or alternate body cannot evade the root fingerprint.

## Commands and results

Commands ran in this worker clone on 2026-07-13. Lean reused the automation-provided canonical
pinned `.lake` symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-0812` | 0 | Rank 1371, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0812/Statement.lean` | 0 | Canonical and expanded targets, checked simple-relation iff, four expected exact-type rejections, edgeless and single-edge boundaries, axiom reports, and explicit target expression elaborated; output SHA-256 `49748fb2...b6c5`. |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0812/check_statement.py` | 0 | Root expression SHA-256 `b20dc742...d7b4`; bundle SHA-256 `8b8107e6...c0f1`; four mutations distinguished; deleting either import failed. |
| canonical fixture with either direct import removed | 1 for each | Expected failures, confirming both imports are necessary for the checked statement fixture; diagnostics contain random temporary filenames and receive no stable-output claim. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | Empty output; the pinned dependency worktree remained clean. |

Final validation additionally parses `statement.json` and `statement-receipt.json`, checks source
and environment hashes, validates the exact DAG identity and ownership, scans the Lean source for
prohibited constructs, checks scoped whitespace, and validates the seven-key root worker packet.

## Mutation and boundary policy

The required mutations remove finite-edge scope, count matched vertices instead of matching edges,
move endpoint-map binders inside one common extremal-value existential, and exclude the edgeless case.
Lean rejects each mutation as the canonical exact type, and the checker verifies that their fully
explicit expressions differ. This establishes statement identity, not arbitrary logical
inequivalence.

`edgelessBoundary` covers an empty edge type with arbitrary finite side types, including isolated
vertices, empty sides, and singleton carriers, and proves both extrema are zero. `singleEdgeBoundary`
proves both extrema are one. The checked declarations report only `propext`, `Classical.choice`, and
`Quot.sound`; the simple-relation transport has the same report. No `sorryAx`, custom axiom, unsafe
declaration, oracle, or root proof is present.

## Source and status boundary

The repository gloss and the inspected arXiv translation freeze a finite bipartite graph with two
vertex sides, maximum matching edge count, minimum covering-vertex count, and equality. The
translation does not state whether parallel edges are excluded, so preserving edge identity is the
fail-closed encoding and the checked erasure iff connects it to the simple-relation reading. The
unavailable original Hungarian inspection, translation-fidelity and
errata review, independent source acceptance, library-specific graph transports, anchor audit,
obligation tree, proof, composition, readable reconstruction, hermetic replay, independent
verification, release, and master acceptance remain open.

This is provisional statement-only evidence. Both the intake dependency and this statement node
remain unfinished until dependency-ordered master acceptance. No audit completion or theorem
completion is claimed.
