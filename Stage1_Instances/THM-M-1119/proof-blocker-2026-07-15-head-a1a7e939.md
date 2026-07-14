# THM-M-1119 proof attempt: blocked

Item: `S56-M-1119-PROOF`  
Attempt: 2026-07-15 (Asia/Shanghai)  
Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`  
Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

The assigned proof phase is **blocked**. No proof body was added, no frozen obligation was closed,
and the root remains `[H2, M4, R4]`. Because the phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains `[ ]`.

The exact target is `Stage1Instances.THM_M_1119.KestenTarget`, stating that the critical
probability for independent bond percolation on the nearest-neighbor square lattice is `1/2`.
`kestenTarget_of_threshold_bounds` is a real checked composition body, but it is conditional on
two open premises:

- `M1119-T-SUBCRITICAL`: `(1 / 2 : NNReal) <= criticalProbability`;
- `M1119-T-SUPERCRITICAL`: `criticalProbability <= (1 / 2 : NNReal)`.

Neither premise has an inhabitant. The open upstream packages are `M1119-N-MONOTONE`,
`M1119-C-RECTANGLES`, `M1119-L-DUALITY`, `M1119-L-RSW`, `M1119-L-RUSSO`, and
`M1119-L-SHARP`: monotone coupling and infimum reduction; finite measurable crossing, pivotal, and
dual-circuit events; planar duality; RSW; Russo's formula; and sharp-threshold estimates. Assuming
one of these packages, or replacing the root with a finite, site-percolation, different-lattice, or
critical-endpoint statement, would be a prohibited placeholder or theorem substitution.

The repository-local search found only the exact statement and conditional composition. Pinned
mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the general product-measure,
graph-reachability, and order substrate, but no relevant percolation, duality, RSW, Russo, pivotal,
sharp-threshold, critical-probability, or Kesten proof declaration. The prerequisite immutable
anchor audit likewise found no eligible external proof body to pin or wrap.

## Validation

All commands ran in this worker clone and reused the automation-provided canonical `.lake` symlink
read-only. No dependency update, build, clone, fetch, or mutation was performed.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | Rank 559; `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1119/check_obligation_tree.py` | 0 | Passed 15 frozen obligations, five typed graphs, step budgets, and exact conditional composition. |
| Temporary copied `Statement.lean` and `ObligationTree.lean`; `lake env lean --trust=0` compiled the statement to a temporary olean and checked the conditional composition with temporary `LEAN_PATH`; temporary files removed | 0 | Exact target and conditional body elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`; no threshold proof was created. |
| Scoped source scan in pinned mathlib for percolation, infinite cluster, critical probability, square lattice, Kesten, Russo, sharp threshold, pivotal, and RSW | 0 | Only unrelated substring matches occurred; no relevant infrastructure or terminal declaration was found. |
| Token-anchored scan for `sorry`, `admit`, axiom declarations, and `sorryAx` in the owned Lean files | 1 | Expected no-match exit: no prohibited device was found. |
| `git diff --check -- Stage1_Instances/THM-M-1119 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The source hashes and full structured result are in
`proof-blocker-2026-07-15-head-a1a7e939.json`. The pre-existing untracked `.lake` symlink makes
this nonrelease evidence.

## Reopen Condition

Resume after placeholder-free bodies exist for the frozen finite-event, planar-duality, RSW,
Russo, sharp-threshold, and infinite-volume obligations, or after an immutable compatible Lean 4
proof is available for pinned exact-type integration and provenance audit. Until then the minimal
open root cut remains `M1119-T-SUBCRITICAL` plus `M1119-T-SUPERCRITICAL`, and
`S56-M-1119-PROOF` cannot truthfully receive `[_]` credit.
