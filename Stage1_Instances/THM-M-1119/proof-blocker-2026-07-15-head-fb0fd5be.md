# THM-M-1119 proof-phase blocker at `fb0fd5be`

Item: `S56-M-1119-PROOF`  
Attempt date: `2026-07-15` (`Asia/Shanghai`)  
Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`  
Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## Verdict

`blocked`: this proof phase is not complete and is not eligible for worker state `[_]`. No proof
body, receipt, obligation closure, graph change, or composition certificate was added, and no
`.stage1-worker-selftest.json` was written.

The exact root remains `Stage1Instances.THM_M_1119.KestenTarget`, namely
`criticalProbability = (1 / 2 : NNReal)` for independent Bernoulli bond percolation on the frozen
nearest-neighbor square lattice. `ObligationTree.lean` checks only the final `le_antisymm`
composition. It requires inhabitants of both
`SubcriticalThresholdBound := (1 / 2 : NNReal) <= criticalProbability` and
`SupercriticalThresholdBound := criticalProbability <= (1 / 2 : NNReal)`; neither inhabitant
exists in the repository or pinned dependency closure.

The first substantive open proof obligation is `M1119-N-MONOTONE`: there is no placeholder-free
Lean monotone coupling and critical-infimum reduction body. The remaining implementation also requires the frozen
finite-rectangle/measurability, planar-duality, RSW, Russo, sharp-threshold, and infinite-volume
packages. The minimal root cut is `M1119-T-SUBCRITICAL` plus `M1119-T-SUPERCRITICAL`.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies only supporting
measure, graph, and order infrastructure. A renewed repository and pinned-mathlib source scan found
no exact Kesten body or percolation/RSW/Russo/sharp-threshold development. The prerequisite anchor
audit's external candidate remains non-equivalent, incompatible, and placeholder-bearing. Thus
there is no legal body to implement, pin, import, or wrap in this bounded attempt. Assuming either
bound, adding an axiom or placeholder, or substituting a finite, site, different-lattice, or
critical-endpoint theorem would violate the frozen target.

## Validation evidence

All commands ran in this worker clone using the existing canonical pinned `.lake` symlink. No
`lake update`, `lake build`, clone, fetch, dependency write, or network-backed proof input was used.
The first failed completion gate is the absent exact proof body for `M1119-T-SUBCRITICAL`; its
companion `M1119-T-SUPERCRITICAL` is also absent.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | Confirmed rank 559, lifecycle `planned`, L0/rework-required, legacy artifacts unaccepted, and `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-1119/check_obligation_tree.py` | 0 | Passed 15 frozen obligations, five typed graphs, the <=100-step ledgers, and exact conditional two-bound composition. |
| Temporary-copy replay with `lake env lean --trust=0`: compile `Statement.lean` to a disposable `Statement.olean`, prepend that directory to the pinned `LEAN_PATH`, then elaborate `ObligationTree.lean` | 0 | The exact statement and conditional composition elaborated; `kestenTarget_of_threshold_bounds` depends only on `[propext, Classical.choice, Quot.sound]`. No threshold inhabitant was produced. |
| Scoped `rg` search over repo-local and pinned mathlib Lean sources for the exact target, bond percolation, square-lattice critical probability, Kesten, Russo, RSW, pivotal, and sharp-threshold terms | 0 | Exact subject matches were confined to this dossier; the sole pinned-infrastructure hit was unrelated pivotal-category text. No eligible terminal body was found. |
| Token-anchored prohibited-device scan over `Stage1_Instances/THM-M-1119/*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, axiom/constant/opaque/unsafe/extern declaration, `implemented_by`, `native_decide`, or `run_tac` token was found. |
| `git diff --check -- Stage1_Instances/THM-M-1119 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The exact temporary Lean replay command, run from the workspace root, was:

```bash
set -euo pipefail
TMP=$(mktemp -d /tmp/thm-m-1119-proof-XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-1119/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-1119/ObligationTree.lean "$TMP/ObligationTree.lean"
cd Formalizations/Lean
lake env lean --trust=0 -R "$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean"
BASE_PATH=$(lake env printenv LEAN_PATH)
LEAN_PATH="$TMP:$BASE_PATH" lake env lean --trust=0 -R "$TMP" "$TMP/ObligationTree.lean"
```

The environment was Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and
mathlib tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Source fingerprints and the
structured command ledger are recorded in the sibling JSON artifact. The pre-existing untracked
`.lake` symlink makes this nonrelease evidence.

## Reopen condition

Retry after placeholder-free bodies exist for the frozen monotonicity, finite-event, duality, RSW,
Russo, sharp-threshold, and both infinite-volume bound obligations, or after an immutable compatible
Lean 4 proof is available for pinned exact-type integration and provenance audit. Until then the
root remains `[H2, M4, R4]`, the proof item remains `[ ]`, and theorem completion is false.
