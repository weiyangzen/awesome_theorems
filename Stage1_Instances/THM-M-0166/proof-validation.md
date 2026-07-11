# THM-M-0166 proof-phase validation

Item: `S56-M-0166-PROOF`

## Implemented bodies

`Proof.lean` supplies a genuine proof of the frozen
`M0166-L-SUBSEGMENT` package: on a connected extended metric space, a smooth
path that realizes the distance between its endpoints realizes the distance
on every ordered subsegment. The proof explicitly uses path-length
additivity, three distance lower bounds, two triangle inequalities, and
finite-distance cancellation. It also supplies checked direct composition
from the still-open global-minimizer package to the exact all-subsegments
Hopf-Rinow conclusion.

The critical `M0166-C-PROPER` and `M0166-L-EXISTENCE` bodies remain open: the
pinned mathlib revision contains the Riemannian distance/path substrate but no
forward Hopf-Rinow minimizer-existence theorem. Consequently the exact root
is not asserted, root machine debt remains `M2`, and theorem completion is
false.

## Commands and exact results

Base revision: `866c817e777d76fcdeab5d8c94051cb1c8e8c5b5`.
Validation ran on 2026-07-12 Asia/Shanghai.

| command | exit | result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0166` | 0 | rank 122, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0166/check_proof.sh)` | 0 | both declarations elaborated; each axiom report was exactly `propext`, `Classical.choice`, `Quot.sound`; forbidden-token scan was empty |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-0166` | 0 | no whitespace errors |

No `lake update`, `lake build`, clone, fetch, network access, or `.lake`
mutation was performed. The pre-existing untracked `.lake` link is outside
this item's owned path.

## Remaining boundary

This is a self-tested partial proof-phase result pending master acceptance.
It claims closure only of `M0166-L-SUBSEGMENT`, not validation, release, H0,
R0, audit completion, or theorem completion. The exact remaining machine cut
set is `M0166-C-PROPER` and `M0166-L-EXISTENCE`.

