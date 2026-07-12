# Statement validation record

Item: `S56-M-0729-STATEMENT`  
Base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`

## Frozen target

`Stage1Instances.THM_M_0729.PCPTheorem` is the equality of binary languages in the dossier's
verifier-based `InNP` and `InPCPLogConst`. The latter uses a polynomial-time nonadaptive binary
oracle checker, eventual `O(log n)` random bits, a uniform constant query bound, perfect
completeness, and soundness `1/2`. Soundness is an exact finite-cardinality inequality, so the sole
direct import is `Mathlib.Computability.TuringMachine.Computable`.

The checked theorem `pcpTheorem_iff_expandedTarget` fixes set extensionality and both inclusions.
This is an exact elaborated target, not a proof of the PCP theorem. The repository sources supply
only the familiar shorthand, so primary-source pinpoint fidelity and H0 review remain explicitly
open rather than being manufactured by this statement node.

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` artifacts.
No update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0729/Statement.lean` | 0 | target, definitions, extensional transport, four mutations, and zero-randomness boundary elaborated |
| `python3 ../../Stage1_Instances/THM-M-0729/check_statement.py` | 0 | expression SHA-256 `2a3d6c...7bbc5`; all four mutations distinguished; pinned mathlib revision reported |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0729/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `f875ab...5cee`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | rank 766, planned, L0/rework-required, theorem incomplete |

## Mutation and boundary policy

The validator distinguishes losing one inclusion, weakening logarithmic randomness to polynomial,
removing the constant query bound, and removing soundness. The kernel-checked boundary theorem
confirms that zero random bits still has one possible random string. Empty inputs, zero queries,
repeated queries, and finitely many small-input exceptions remain in scope.

This is statement-only worker evidence pending master acceptance. No proof, anchor, source-review,
audit-completion, or theorem-completion credit follows.
