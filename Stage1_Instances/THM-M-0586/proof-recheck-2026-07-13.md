# THM-M-0586 proof-phase recheck

Item: `S56-M-0586-PROOF`  
Attempt date: 2026-07-13  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Verdict

`blocked`. This retry found no new proof-bearing declaration and added no proof
body. The existing `proof-blocker.json` remains accurate: the frozen root needs
both `M0586-T-FIVE` and `M0586-T-STABLE`, while the repository and pinned
dependency closure contain neither package.

Pinned mathlib's apparent declaration
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` is still a
`proof_wanted` source marker. A direct expected-failure Lean probe reports
`Unknown constant`, so it cannot be imported or wrapped. The bounded pinned
source search found only that marker, not an h-cobordism, s-cobordism, surgery,
or high-dimensional sphere-homeomorphism proof. The already audited immutable
external candidate still closes only dimension zero.

The local theorem
`highDimensionalPoincare_of_dimension_packages` re-elaborates, with an axiom
report of only `propext`, `Classical.choice`, and `Quot.sound`. It is a valid
child-to-parent composition certificate, but its two arguments are exactly the
missing mathematical bodies. Crediting it as an unconditional root proof would
hide unresolved premises and violate the exact-target gate.

## Validation evidence

All commands used the existing pinned `.lake` artifacts. No Lake update/build,
dependency clone/fetch, or `.lake` mutation was performed. Temporary source and
object files were placed under `/tmp`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | Rank 117, lifecycle `planned`, baseline `L0/rework_required`, `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | `PASS`: 18 obligations, 38 typed edges, denominator `bbeb74...07b3e`; root open at M3 and both dimension packages M4 |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | Pinned inventory, `proof_wanted` boundary, eight probes, and immutable revisions agree |
| compile `Statement.lean` to `/tmp/thm-m-0586-proof-current/Statement.olean`, then elaborate `ObligationTree.lean` with the pinned `lake env which lean` and `LEAN_PATH` | 0 | Exact target and conditional composition elaborated; the composition's axiom report is `[propext, Classical.choice, Quot.sound]` |
| expected-failure file importing `Mathlib.Geometry.Manifold.PoincareConjecture` and checking `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` via `lake env lean` | 1 | `Unknown constant ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` |
| `rg -n -i 'nonempty_homeomorph_sphere\|generalized[ -]poincar\|high[ -]dimensional[ -]poincar\|h[- ]cobord\|s[- ]cobord\|smale' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | Only mathlib's Poincare statement comments and `proof_wanted` markers matched |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-0586 --glob '*.lean'` | 1 | Expected no-match result: no forbidden Lean proof escape in the owned sources |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-0586/proof-blocker.json` | 0 | Existing structured blocker record remains valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0586` | 0 | No whitespace errors |

The first failed gate remains terminal proof-body availability for
`M0586-T-FIVE` and `M0586-T-STABLE`; together they remain the minimal root cut
set. Retry only after placeholder-free local implementations of the frozen
puncture, disk, cobordism, h-/s-cobordism, and gluing route, or after an
immutable compatible Lean 4 proof is available for exact-type pinned
integration and provenance checking.

This is blocker evidence, not a proof receipt. It does not satisfy the proof
item or claim M0, validation, release, theorem completion, or master acceptance.
Because the assigned phase is not genuinely self-tested as complete, no
`.stage1-worker-selftest.json` is emitted.
