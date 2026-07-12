# Statement validation record

Item: `S56-M-1008-STATEMENT`  
Base revision: `bd7798793e8cb0e4120b2ac26910a457207b30d4`

## Frozen target

`Stage1Instances.THM_M_1008.HewittSavageZeroOneTarget` formalizes the intake's path-space
statement. The probability measure, mutual independence, common coordinate law, product-measurable
event, and invariance under every finite-support permutation are explicit. The conclusion is the
zero-or-one probability of the event pulled back along the sample-path map.

The sole direct import is `Mathlib.Probability.IdentDistribIndep`.
`target_iff_expandedSourceShape` kernel-checks the direct expansion. Finite support uses
`Set.Finite {n | sigma n != n}`, avoiding the unrelated `Equiv.Perm.support` API that requires a
finite coordinate type.

## Commands and results

Lean commands ran from `Formalizations/Lean` with the existing pinned `.lake` symlink; no Lake
dependency operation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1008/Statement.lean` | 0 | target, direct expansion, four mutations, and identity-permutation boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1008/check_statement.py` | 0 | expression SHA-256 `2d9e3c...b76c`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-1008/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `95e22d...ebf6`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1008` | 0 | rank 288, planned, L0/rework-required, theorem incomplete |

## Mutation and status boundary

The validator compares explicit elaborated expressions and distinguishes removal of independence,
an `Int` rather than `Nat` coordinate domain, existential rather than universal process scope, and
invariance under all rather than finite-support permutations. The checked identity case confirms
that the symmetry quantifier includes its degenerate permutation boundary.

This is self-tested statement evidence pending master acceptance. Primary-source pinpointing and
independent source-convention review remain for anchor audit. No proof, audit completion, or theorem
completion is claimed.
