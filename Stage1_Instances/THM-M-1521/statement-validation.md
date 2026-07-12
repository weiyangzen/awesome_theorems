# Statement validation record

Item: `S56-M-1521-STATEMENT`  
Base revision: `04422fd72f342b905dbd4fb4a5a4035cfae56e6e`

## Frozen target

`Stage1Instances.THM_M_1521.PoincareRecurrenceTarget` is the exact intake-selected claim over an
arbitrary measurable-space type, a discrete self-map, and a finite measure preserved by that map.
For every null-measurable set, almost every point starting in it returns infinitely often. Its sole
direct import is `Mathlib.Dynamics.Ergodic.Conservative`.

The historical candidate is checked by the definitional iff
`poincareRecurrenceTarget_iff_pinnedCandidateSourceShape`. The stronger conservative-system
encoding implies the root through the checked
`poincareRecurrenceTarget_of_conservativeRecurrenceTarget`; no reverse implication is credited.

## Commands and results

Commands ran in this worker clone. Lean commands used the existing pinned `.lake` artifacts and did
not update or fetch dependencies.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1521/Statement.lean` | 0 | canonical target, two checked transports, four mutations, and empty-set boundary elaborated; explicit target expression printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1521/check_statement.py` | 0 | expression SHA-256 `3d7c202adf1f52ae3dbcdb46e7726395600cb0d89d93220d70d42b9b837f6c06`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && sha256sum ../../Stage1_Instances/THM-M-1521/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `2345be...139`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard reports 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1521` | 0 | rank 180, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares explicitly elaborated expressions. It distinguishes removal of finiteness,
specialization of the arbitrary domain to `Nat`, relocation of the set binder inside the
almost-everywhere binder, and exclusion of the null-set boundary. A kernel-checked example confirms
that the empty-set case remains present and vacuous. The identity map and other finite or degenerate
models are not excluded by extra premises.

This is statement-only evidence pending master acceptance. It supplies no proof credit and does not
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
