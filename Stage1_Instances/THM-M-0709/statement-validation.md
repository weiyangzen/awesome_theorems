# Statement validation record

Item: `S56-M-0709-STATEMENT`  
Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`

## Frozen target

`Stage1Instances.THM_M_0709.PostCorrespondenceUndecidable` states that semantic solvability of
finite PCP instances over the fixed binary alphabet is not a `ComputablePred`. An instance is a
finite ordered list of pairs of finite Boolean words. A witness is one nonempty list of valid
indices, used in the same order for both concatenations. The input is already a structured
`Primcodable` value, so there are no malformed external codes. The sole direct import is
`Mathlib.Computability.Halting`.

`postCorrespondenceUndecidable_iff_expanded` kernel-checks the full expansion and fixes negation
scope. This node does not prove undecidability or claim a source review.

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` artifacts;
no dependency update, fetch, or build was performed. The pre-existing `.lake` link makes this
nonrelease worker evidence.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0709/Statement.lean` | 0 | exact target, expanded iff, four mutations, and empty-instance boundary theorem elaborated |
| `python3 ../../Stage1_Instances/THM-M-0709/check_statement.py` | 0 | expression SHA-256 `5d375802e054a1c87b9fe6c8c24b728e9bcf8bfa20025ebe987d461545926d03`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0709/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `354a0a...9121`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0709` | 0 | rank 750, planned, L0/rework-required, theorem incomplete |

## Mutation and boundary policy

The validator distinguishes allowing an empty witness, substituting a unary alphabet, bounding
witness length, and permitting separate upper/lower index sequences. The kernel-checked boundary
theorem proves that an empty tile instance has no solution. Empty component words, repeated tiles,
and repeated indices remain deliberately in scope.

This is statement-only evidence pending master acceptance. The primary-source pinpoint review
remains H1, and no anchor, proof-body, theorem-completion, or release credit follows.
