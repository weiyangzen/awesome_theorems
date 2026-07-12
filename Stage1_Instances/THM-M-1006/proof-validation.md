# THM-M-1006 proof-phase attempt

Item: `S56-M-1006-PROOF`  
Date: `2026-07-12`  
Base revision: `48a1d632cacabc75bca90db155d57ebb777aee3d`

## Verdict

`blocked`: the exact two-sided BDG root remains open. `Proof.lean` supplies real proof bodies for
the algebraic difference-process reconstruction and the horizon-zero boundary. These discharge
substantive parts of `M1006-N-DIFFERENCES` and `M1006-S-BOUNDARY`, but do not prove the directional
packages `M1006-T-LOWER` and `M1006-T-UPPER`.

The first unavailable analytic package is `M1006-L-STOPPED`: pinned mathlib supplies stopping-time,
Doob maximal, and upcrossing infrastructure, but no quantitative stopped-martingale estimates that
yield the frozen good-lambda inequalities. The subsequent good-lambda, layer-cake, all-positive-`p`,
and directional assembly nodes therefore remain open. Introducing those packages as hypotheses
would be a conditional substitute, not a proof of `StatementShape`.

Because the assigned deliverable is not complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Implemented proof bodies

`sum_martingaleDifference` proves finite telescoping. `sum_martingaleDifference_of_zero` reconstructs
the process from its differences when `f 0 = 0`. `quadraticVariation_zero`, `maximalProcess_zero`,
and `boundary_zero` establish the exact horizon-zero behavior. All five declarations elaborate
without `sorryAx`; their printed axiom set is exactly `propext`, `Classical.choice`, and `Quot.sound`.

## Narrow validation evidence

Commands ran in the worker clone using the existing canonical pinned `.lake` symlink. No dependency
update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286; baseline L0; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges pass; denominator `12818dc1f1f77555b23c3fea780e482518d1d5c196dc1390c8175d00914dac6f`; root open M3. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1006/Statement.lean` | 0 | The exact frozen target elaborates. |
| Compile `Statement.lean` to a temporary target-local `Statement.olean`, then invoke the pinned `lake env which lean` with the pinned `LEAN_PATH` on `Proof.lean`; remove temporary artifacts | 0 | All five proof bodies elaborate; `#print axioms` reports `[propext, Classical.choice, Quot.sound]` and no `sorryAx`. |
| `rg -n '\b(sorry\|admit\|axiom)\b\|sorryAx' Stage1_Instances/THM-M-1006/Proof.lean` | 1 | No output, the expected clean negative scan. |
| `git diff --check -- Stage1_Instances/THM-M-1006` | 0 | No output. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

Statement SHA-256: `88f12c854469ebbf6a0d1325d4456838c75a155a430820356ae18b5b2c98d4cd`.
Proof source SHA-256: `08b4daf0e5b8fe530e25d3c3c0ab2c69b6f9af13930165f6d891e6c92d7161bc`.

## Reopen condition

Resume after a placeholder-free implementation of both directional packages and their frozen
analytic dependencies, or an eligible immutable Lean 4 proof that can be pinned, imported, and
exact-type checked. Until then the minimal root cut is `M1006-T-LOWER` plus `M1006-T-UPPER`, the
root remains M3, and theorem completion remains false.
