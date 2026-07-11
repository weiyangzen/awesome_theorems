# THM-M-0450 proof-phase blocker

Item: `S56-M-0450-PROOF`  
Base revision: `17cf20b536c091d5d475ce44aee76d6d8e96196d`  
Attempt date: 2026-07-12

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body for
the exact target was added, and no worker self-test receipt is issued.

Pinned mathlib provides `AddCommGroup.fg_of_descent'`, and the existing
`ObligationTree.lean` kernel-checks the composition from two explicitly assumed
packages. It does not construct either package. The exact root still requires:

1. finite index of doubling on `E.toJacobian.Point` for every elliptic curve
   over every number field (`M0450-B-WEAKMW`, including the Kummer map and
   finite descent quotient);
2. a nonnegative real height on the same point model with Northcott and the
   bounded approximate parallelogram law (`M0450-H-HEIGHT`);
3. any model transport needed by those arithmetic constructions.

The repo-local and pinned-mathlib search found no theorem constructing these
inputs or proving the exact Mordell-Weil root. The previously audited external
Lean 4 candidate is conditional on weak Mordell-Weil, targets a different point
model and toolchain, and is not a pinned dependency. Importing it would neither
close the frozen target nor constitute valid pinned validation. Implementing
the missing arithmetic developments from scratch is beyond a truthful bounded
proof-phase execution attempt; replacing them by assumptions, `sorry`, or an
axiom is prohibited.

## Commands and exact results

All commands below ran from the worker-clone root unless a command contains an
explicit `cd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0450` | 0 | rank 92; `planned`; `L0`; `rework_required: true`; `theorem_complete: false` |
| `git rev-parse HEAD` | 0 | `17cf20b536c091d5d475ce44aee76d6d8e96196d` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0450/ObligationTree.lean` | 0 | conditional declaration elaborated; axiom report was exactly `[propext, Classical.choice, Quot.sound]` |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -n -i -E 'mordell.?weil\|weakMW_implies_MW' HEAD -- '*.lean'` | 0 | only the Mordell-Weil explanatory comment at `Mathlib/GroupTheory/Descent.lean:42-43`; no exact or weak-Mordell-Weil proof declaration |
| `rg -n -i -e 'mordell.?weil' -e 'weakMW_implies_MW' -e 'weakmordell' --glob '*.lean' . Formalizations/Lean/.lake/packages/mathlib` | 0 | repo hits were audit/comment/conditional-wrapper material; no terminal exact-root body |
| `git diff --check -- Stage1_Instances/THM-M-0450` | 0 | no whitespace errors before this record was added |

The only match from `rg -n '(sorry|admit|axiom|unsafe)'
Stage1_Instances/THM-M-0450 --glob '*.lean'` was the benign command
`#print axioms root_of_descent_packages` in `ObligationTree.lean`; there is no
placeholder declaration in the target's Lean files.

## Status boundary

The existing conditional composition remains useful checked evidence, but it
does not prove `ExactTarget`. Machine status remains `M3`, theorem completion
remains false, and the first failed proof gate is construction of the frozen
weak-Mordell-Weil and height packages. Because the assigned phase is not
complete, `.stage1-worker-selftest.json` must remain absent.
