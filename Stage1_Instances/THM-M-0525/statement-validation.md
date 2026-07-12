# Statement-phase validation record

Item: `S56-M-0525-STATEMENT`. Base revision:
`61f7b7dcf859725be90a66069022323d5a8903e2`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed for 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets and ranks 1..1546. |
| `python3 scripts/stage1_target.py show THM-M-0525` | 0 | Rank 582, planned, L0/rework-required, theorem incomplete. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0525/Statement.lean)` | 0 | Exact declaration, definitional carrier witness, and `PUnit` boundary target elaborated. Printed signature is `(X : Type u) -> [TopologicalSpace X] -> X -> Prop`. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0525/MutationRemovedTopology.lean)` | 1 expected | Failed to synthesize `TopologicalSpace X`. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0525/MutationChangedDomain.lean)` | 1 expected | Rejected `x : Y` where `x : X` was required. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0525/MutationBinderScope.lean)` | 1 expected | Rejected use of `X` before its binder. |

The import is the smallest mathlib module that declares `FundamentalGroup`; it publicly imports the
path quotient and groupoid machinery required by the exact operation equations. The scheduler's
existing `.lake` symlink was used read-only. No update, build, fetch, or clone was run.

The negative mutation files intentionally do not elaborate and are test inputs, not project source
modules. Their diagnostics contain Lean's recovery term `sorry`; no source artifact contains a
proof escape. Proof, anchor, source, trust, hermetic validation, and master-acceptance gates remain
open, so neither audit completion nor theorem completion is claimed.
