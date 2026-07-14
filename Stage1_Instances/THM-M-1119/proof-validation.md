# THM-M-1119 proof-phase validation

Item: `S56-M-1119-PROOF`

Date: `2026-07-15T06:31:46+08:00`

Base revision: `9584b263a758e0dbab59344389554570dcf2e535`

Base tree: `d4ea7039d087ff41783f81c4f1b35c2817dd6a1b`

## Implemented bodies

`Proof.lean` adds placeholder-free local graph, measurability, and endpoint bodies. It proves that
the open graph and the rooted unbounded-reachability event are increasing in the open bonds, maps
open square-lattice walks to open-graph reachability, and proves that the rooted infinite-cluster
event is measurable. It also checks the degenerate Bernoulli endpoints: at `p = 0` the event has
probability zero; at `p = 1` the event has probability one, the positive-parameter set is nonempty,
and `criticalProbability <= 1`.

These bodies are genuine partial progress toward `M1119-S-DEFINITIONS`, `M1119-S-BOUNDARY`, and
`M1119-N-MONOTONE`. Their frozen targets are broader package-level prose, so zero complete frozen
obligations are claimed closed.

## Open boundary

Neither `(1 / 2 : NNReal) <= criticalProbability` nor
`criticalProbability <= (1 / 2 : NNReal)` is proved. The exact root therefore remains
`[H2, M4, R4]`, `root_closed=false`, and `theorem_complete=false`. Closing it still requires the
finite rectangle, planar duality, RSW, Russo, sharp-threshold, and infinite-volume packages. The
minimal root cut remains `M1119-T-SUBCRITICAL` plus `M1119-T-SUPERCRITICAL`.

## Narrow validation

All successful Lean checks reused the existing canonical pinned `.lake` artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | Rank 559; planned L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1119/check_obligation_tree.py` | 0 | Passed 15 frozen obligations, five typed graphs, step budgets, and exact conditional composition. |
| `LEAN_NUM_THREADS=1 bash Stage1_Instances/THM-M-1119/check_proof.sh` | 0 | Final isolated trust-zero `Statement -> ObligationTree -> Proof` replay passed; all 13 checked proof declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| independent `LEAN_NUM_THREADS=1 bash Stage1_Instances/THM-M-1119/check_proof.sh` | 0 | A second worker independently replayed final source SHA-256 `f20a21a...0b242` and obtained the same axiom closure and PASS result. |
| `rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern)[[:space:]]+' Stage1_Instances/THM-M-1119 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof device occurs in owned Lean sources. |

Several earlier retries were externally terminated while the host had 60-80 concurrent Lean
processes and exhausted swap; those runs receive no proof credit. The final scoped run and the
independent replay both exited zero. The pre-existing untracked `.lake` symlink makes this warm
worker evidence nonrelease.

## Reopen condition

Continue with the missing parameter coupling, rectangle, duality, RSW, Russo, sharp-threshold, and
two exact threshold-bound bodies. No endpoint or measurability result in this module substitutes
for Kesten's equality.
