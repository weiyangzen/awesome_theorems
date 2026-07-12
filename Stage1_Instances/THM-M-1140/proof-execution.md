# Proof-phase execution record

Item: `S56-M-1140-PROOF`  
Base revision: `fcf07b444b4fc685fd4c015fff26d66c7354f325`  
Execution date: 2026-07-12

## Result

`Proof.lean` supplies a kernel-checked proof of the frozen
`ConnectedLevelPropagation` package. The proof works in the subtype topology on the domain: the
target level set is closed by continuity, open by the supplied local-rigidity neighborhoods, and
therefore all of the connected subtype. Its trust report is exactly `propext`,
`Classical.choice`, and `Quot.sound`.

The proof phase is blocked at `M1140-L-MEAN-VALUE` and `M1140-T-LOCAL-PACKAGE`. The pinned mathlib
revision defines general finite-dimensional `HarmonicOnNhd` through the Laplacian, but its
general-dimensional harmonic directory contains no mean-value theorem, unique-continuation
theorem, local rigidity theorem, or strong maximum principle. The available `circleAverage_eq`
result is restricted to functions on the complex plane, so using it would narrow the quantified
dimension and change the frozen theorem. Constructing the missing arbitrary-dimensional analytic
theory is beyond the present pinned API; no external dependency was fetched and no unproved
premise was introduced.

Consequently the exact root remains open at `M3`. This record claims the connected-propagation
proof body only, not completion of the assigned proof node or of the theorem. No worker self-test
manifest is emitted because the assigned phase is not fully closed.

## Commands and exact results

All commands ran in this worker clone and reused the existing pinned Lake artifacts.

| Command | Exit | Result |
|---|---:|---|
| `LEAN_PATH_BASE=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); LEAN_BIN=$(cd Formalizations/Lean && lake env which lean); cd Stage1_Instances/THM-M-1140; LEAN_PATH="$LEAN_PATH_BASE" "$LEAN_BIN" -o Statement.olean Statement.lean; LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean; LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" Proof.lean; rm Statement.olean ObligationTree.olean` | 0 | `connectedLevelPropagation` elaborated; axiom report was `[propext, Classical.choice, Quot.sound]`; temporary oleans were removed |
| `rg -n '^\\s*(sorry|admit|axiom)\\b' Stage1_Instances/THM-M-1140/Proof.lean` | 1 | No prohibited proof declaration or term; exit 1 is ripgrep's expected no-match result |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | Rank 345; planned; L0/rework-required; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1140` | 0 | No scoped whitespace errors |

No `lake update`, `lake build`, dependency clone, dependency fetch, or `.lake` mutation was
performed.
