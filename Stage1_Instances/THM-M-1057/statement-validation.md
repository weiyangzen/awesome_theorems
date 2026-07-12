# Statement validation record

Item: `S56-M-1057-STATEMENT`  
Base revision: `576c57235474883e4ba7de1eb5e5f82bccfc8b20`

## Frozen target

`Stage1Instances.THM_M_1057.KingmanTarget` is the intake-selected ergodic,
real-valued probability-space form. Its conclusion is almost-everywhere
convergence to the infimum of normalized expectations over `Ici 1`. The
kernel-checked `kingmanTarget_iff_expandedSourceShape` expands all local
definitions. The historical `S1_M_249` package is not imported or credited.

The two direct imports are necessary in isolation: the Bochner module supplies
the integral and integrability surface, while the ergodic module supplies the
ergodic transformation interface. Removing the former fails elaboration.

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned
Lake environment. No dependency or `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1057/Statement.lean` | 0 | Exact target, expanded-shape equivalence, mutations, and boundary theorems elaborated; target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1057/check_statement.py` | 0 | Expression SHA-256 `aebaaa6256cc5cb252ff4662647955a625f2ff6f1311dbcea1c04463ab3c03af`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1057/Statement.lean lean-toolchain lake-manifest.json` | 0 | `bdd8ad...1073`, `651c8a...d1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1057` | 0 | Rank 249, planned, L0/rework-required, theorem incomplete |

## Statement boundary

The validator distinguishes removal of the lower-bound premise, replacement of
the real codomain, a binder-scope change, and inclusion of zero in the
infimum. Kernel checks also establish that zero-index normalization is zero and
that index one belongs to the positive-index value set. This is statement-only
evidence pending master acceptance. Source audit, proof construction, and all
theorem-completion gates remain open.
