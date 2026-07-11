# Statement validation record

Item: `S56-M-0417-STATEMENT`  
Base revision: `1371ca5a74c6cbc303b18e97c518ffe32b24e9ef`

## Frozen target

`Stage1Instances.THM_M_0417.Statement` freezes the strict Minkowski convex body target selected at
intake. The ambient object is a finite-dimensional real normed vector space with a Borel measurable
structure and additive Haar measure. The lattice-facing data are a countable additive subgroup and
an explicit additive fundamental domain `F`; `mu F` is the covolume term. A convex set symmetric
about zero whose measure strictly exceeds `mu F * 2 ^ finrank Real E` must contain a nonzero point
of the subgroup.

The sole direct import is `Mathlib.MeasureTheory.Group.GeometryOfNumbers`. An explicitly typed
`#check` confirms that the pinned mathlib declaration has the selected local hypotheses and
conclusion. This locates a candidate exact anchor but does not claim proof integration in the
statement phase.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean` with
the existing pinned Lake environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0417/Statement.lean` | 0 | canonical target, exact-type mathlib fixture, and four structural mutations elaborated; explicit expressions printed |
| `python3 ../../Stage1_Instances/THM-M-0417/check_statement.py` | 0 | canonical expression SHA-256 `9d911a547ec729d286676982e8bd570bc5ee0790fb6a557062f3c0a4cf8beba5`; all four mutations have distinct expressions |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0417/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `fc5125...56fe`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-0417/statement.json >/dev/null` | 0 | structured statement record parses |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0417` | 0 | rank 72, planned, legacy artifacts unaccepted, theorem incomplete |
| prohibited-token scan of the new statement artifacts | 1, expected empty | no prohibited Lean proof escape or unsafe declaration occurs |
| `git diff --check -- Stage1_Instances/THM-M-0417` | 0 | no whitespace errors |

## Mutation and boundary policy

The validator fingerprints removal of symmetry, removal of convexity, replacement of `<` by `<=`
without the extra compact-boundary hypotheses, and removal of the nonzero witness condition. The
zero-dimensional and trivial ambient cases are not silently removed by a `Nontrivial E` instance;
they remain governed by feasibility of the strict measure premise. Equality belongs to the separate
compact boundary form and is not accepted as interchangeable. A `ZLattice`/covolume formulation
still needs a later checked object-model transport.

This is self-tested statement evidence pending master acceptance. It does not advance the anchor
audit, obligation tree, proof, validation, or release phases, and it does not claim theorem
completion.
