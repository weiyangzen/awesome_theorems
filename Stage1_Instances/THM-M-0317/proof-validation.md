# THM-M-0317 proof-phase validation

Item: `S56-M-0317-PROOF`

Validation date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

## Implemented bodies

`Proof.lean` implements the compactness/separation half of the frozen proof
architecture. `zero_mem_closure_displacement_image` turns displacement in
every zero neighbourhood into zero membership in the closure of the
displacement image. `isClosed_displacement_image` proves that image closed by
compactness, continuity, and Hausdorff separation. `compactnessLimitPackage`
combines the two and inhabits the exact `CompactnessLimitPackage` interface.

This provisionally closes `M0317-N-NEIGHBORHOODS`,
`M0317-L-COMPACT-LIMIT`, and `M0317-T-LIMIT`. It does not implement
`ApproximationPackage`: the finite cover, subordinate partition, finite-rank
barycentric map, finite-dimensional Brouwer theorem, and approximation
transfer remain open. Consequently `M0317-T-APPROX` and the exact root remain
open, with proposed machine classification `M2`, not `M0`.

## Commands and results

All commands reused the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or `.lake` mutation
was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0317/check_proof.sh` | 0 | Isolated `--trust=0` elaboration of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` passed; the four axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` was absent; the structural receipt checker passed |
| `python3 Stage1_Instances/THM-M-0317/check_obligation_tree.py` | 0 | Frozen registry/graph consistency passed; it correctly retains the pre-proof open limit branch pending master reconciliation |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0317` | 0 | rank 683, planned, legacy artifacts unaccepted, theorem incomplete |
| Prohibited-device scan over `Proof.lean` | 0 | No `sorry`, `admit`, `sorryAx`, bodyless `axiom`/`constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` |
| Bounded exact-topic scan of pinned mathlib and repository Lean | 0 | No compatible finite-dimensional compact-convex Brouwer, Schauder, or Tychonoff fixed-point terminal body was materialized; hits were unrelated terminology or open neighboring dossiers |
| JSON syntax checks for receipt, blocker, and worker packet | 0 | All three artifacts parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0317 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The pinned environment is Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The canonical `.lake` symlink
is automation-provided and untracked, so this is nonrelease worker evidence.

## Boundary

This is a self-tested partial proof contribution proposed as `[_]` for
integration-lane review. It does not claim `ApproximationPackage`, the proof
item as a whole, the exact root, accepted state, validation/release completion,
or theorem completion. Full source fidelity and the duplicate relationship
with `THM-M-0638` also remain downstream review concerns.
