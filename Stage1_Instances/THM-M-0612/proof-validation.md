# THM-M-0612 proof-phase attempt

Item: `S56-M-0612-PROOF`  
Date: `2026-07-12`  
Base revision: `aa8a8afff8eb3496c9223c57b562cceb553f8a74`

## Verdict

`blocked`: no eligible proof body for the exact nonsqueezing target exists in
the repository or pinned dependency closure. The immediate root cut remains
`M0612-T-SQUARED`, the geometric conclusion `r ^ 2 <= R ^ 2`. The first
substantive unavailable package is `M0612-C-CAPACITY`: neither the canonical
local-domain model nor pinned mathlib has a constructed symplectic capacity
with the required invariance, monotonicity, ball, and cylinder theorems. The
alternative frozen route also lacks compatible almost-complex structures,
pseudoholomorphic-curve existence and compactness, energy identities, and the
monotonicity estimate.

`ObligationTree.lean` contains two real but nonterminal proof bodies.
`radius_le_of_sq_le` proves the elementary ordered-field transport, and
`root_of_radiusSquaredObstruction` checks exact composition after accepting
`RadiusSquaredObstruction` as a premise. It does not construct that premise.
Consequently these bodies do not close the root and do not advance its `M3`
classification.

No source was added because any short local declaration of the missing
geometric package would necessarily be an axiom, bodyless declaration, or
unproved premise. No weaker, conditional, or differently encoded theorem was
substituted. Because the assigned proof deliverable is not complete, this
attempt deliberately leaves `.stage1-worker-selftest.json` absent.

## Narrow validation evidence

All commands ran in the worker clone and reused the existing canonical pinned
Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; baseline L0; lifecycle planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | 26 obligations and 58 typed edges pass; denominator `2cad29b7c0b54afdec80a5d7ac1940a49cccfacdab64c1b75c27e140dd7a4bc8`; root open M3 because the radius-squared package remains M4. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0612/Statement.lean` | 0 | The exact canonical target elaborates under Lean 4.29.0. |
| Compile `Statement.lean` to a temporary local `Statement.olean`, then run `ObligationTree.lean` with the pinned `lake env which lean` and `lake env printenv LEAN_PATH`; remove the temporary olean | 0 | Both local bodies elaborate. `#print axioms` reports `[propext, Classical.choice, Quot.sound]` for each body and no admitted geometry. |
| `rg -n -i 'non.?squeez\|gromov.?width\|symplectic.?capacity\|pseudoholomorphic\|pseudo.?holomorphic' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Hits are dossier/legacy statement-boundary material and elementary Gromov-width interface lemmas; no terminal nonsqueezing, capacity-computation, or pseudoholomorphic proof body is present in pinned mathlib. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |

The statement SHA-256 is
`2de623b53340de741e2b691d81a0e1a9f0a6f74bbdeb133f7ebcc5a20d97f919`.
The checked conditional-composition source SHA-256 is
`0392a18a80b7cea4fcbba89e23941228ff861cd6406345bf134ef4b857773007`.

## Reopen condition

Resume only after either a placeholder-free local implementation of
`M0612-T-SQUARED` and its frozen nonlinear dependencies, or discovery of an
eligible immutable Lean 4 proof that can be pinned, exact-type transported,
and checked in the repository closure. Until then `root_closed=false`, the
root remains `[H2, M3, R4]`, and theorem completion remains false.
