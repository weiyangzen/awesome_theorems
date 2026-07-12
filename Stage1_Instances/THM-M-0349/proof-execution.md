# THM-M-0349 proof execution

Item: `S56-M-0349-PROOF`  
Date: `2026-07-12`  
Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`

## Result

The requested proof phase is blocked and is not self-tested as complete. `Proof.lean` adds a real,
placeholder-free proof body for the one-mode part of frozen construction obligation
`M0349-C-POLYNOMIAL`: it constructs the conjugate Fourier mode and proves its coefficient identity.
This is strictly partial proof progress and does not close `M0349-C-POLYNOMIAL`, either root package,
or `ConjugateFunctionTheoremTarget`.

The first mathematical blocker is frozen obligation `M0349-L-WEAK11`. The pinned mathlib tree at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains Fourier density and `L2` Fourier-series
infrastructure, but the scoped source search found no periodic Hilbert/conjugate transform, weak
type `(1,1)` estimate, or Marcinkiewicz interpolation result. Consequently there is no legal proof
body from which to derive the required uniform strong `Lp` bound. No moving dependency was fetched.

Root machine debt remains `M3`; the minimal open root cut remains
`M0349-P-EXISTENCE` and `M0349-P-BOUND`. No theorem-completion credit is claimed, and no
`.stage1-worker-selftest.json` is emitted.

## Validation

All commands used the existing pinned Lake environment. The temporary `Statement.olean` needed for
the narrow module import was removed after checking.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0349` | 0 | rank 842; `planned`; `theorem_complete: false` |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0349 ../../Stage1_Instances/THM-M-0349/Statement.lean -o ../../Stage1_Instances/THM-M-0349/Statement.olean && LEAN_PATH=../../Stage1_Instances/THM-M-0349 lake env lean -R ../../Stage1_Instances/THM-M-0349 ../../Stage1_Instances/THM-M-0349/Proof.lean` | 0 | both local declarations elaborated; each printed exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n -i 'hilbert transform|hilbert_transform|conjugate function|conjugate_function|marcel riesz|weak type|weak-type|marcinkiewicz|riesz.thorin|riesz_thorin|interpolation' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | only unrelated interpolation mentions; no required analytic result |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0349 -g '*.lean'` | 1, expected | no prohibited proof placeholder or declared axiom |
| `git diff --check -- Stage1_Instances/THM-M-0349` | 0 | no whitespace errors |

## Unblock condition

Implement the frozen weak-type estimate and the required interpolation/extension infrastructure in
Lean, or identify an immutable compatible Lean 4 upstream containing those exact bodies and pin,
import, and kernel-check it. Only then can the two root packages be constructed without assumptions.
