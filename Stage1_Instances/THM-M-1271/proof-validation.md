# THM-M-1271 proof-phase validation

Item: `S56-M-1271-PROOF`

Validation date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `799262a53af4c03d919b758421e149ffc158d472`

## Implemented bodies

`Proof.lean` now separately proves the frozen `M1271-C-PATH-MAX`
construction. `pathHeight_attained` identifies `PathHeight Phi gamma` with
an attained value `Phi (gamma t)` on the compact interval for every
admissible path. The earlier barrier proof needed only boundedness and an
`sSup` inequality, so it did not close this exact attainment obligation.

`exists_valueSequence_at_mountainPassLevel` then uses the nonempty,
bounded-below set of admissible path heights, `exists_seq_tendsto_sInf`, and
the new attained maxima to construct points whose functional values tend to
`MountainPassLevel Phi e`. This is genuine progress inside
`M1271-C-PS-SEQUENCE`, but it is only the value-convergence half.

The derivative norms of those points are not proved to tend to zero. Thus
`M1271-C-PS-SEQUENCE`, `M1271-T-CRITICAL`, and the exact root remain open.
The proposed root machine classification is `M2`, not `M0`; the accepted
registry and graph state remain unchanged pending master review.

## Commands and results

All commands reused the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or `.lake` mutation
was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1271/check_proof.sh` | 0 | Isolated trust-zero statement, obligation-tree, and proof elaboration passed; all eight axiom reports were confined to `propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` was absent; the structural receipt checker passed |
| `python3 Stage1_Instances/THM-M-1271/check_obligation_tree.py` | 0 | 13 obligations and 25 typed edges; denominator `2f6d1a3dc9064aff967ba0cf8443ff438e9cb99e0b2d34994252e6410d2d75bc`; frozen graph still records its pre-proof open M3 boundary |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1271` | 0 | rank 164, planned, legacy artifacts unaccepted, theorem incomplete |
| Prohibited-device scan over owned Lean sources | 0 | No `sorry`, `admit`, `sorryAx`, bodyless `axiom`/`constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` |
| Pinned dependency theorem-family scan | 1, expected | Empty output; no compatible Mountain Pass, Palais-Smale, Ekeland, Caristi, deformation-lemma, or minimax-critical source was materialized |
| JSON syntax checks for receipt, blocker, and worker packet | 0 | All three artifacts parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-1271 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The pinned environment is Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The canonical `.lake` symlink
is automation-provided and untracked, so this is nonrelease worker evidence.

## Boundary

This is a self-tested partial proof contribution. It proposes `[_]` only for
integration-lane review of the changed proof-phase packet. It does not claim
the full Palais-Smale sequence, the proof item as a whole, the exact root,
accepted state, validation/release completion, or theorem completion.
