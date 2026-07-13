# THM-M-1055 proof-phase validation

Item: `S56-M-1055-PROOF`  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Result

The proof phase now has a placeholder-free, kernel-elaborated proof of the exact
`Stage1Instances.THM_M_1055.BirkhoffErgodicTarget`. The analytic bodies are a narrow port of
`marcmorningstar/lean4-ergodic-theory` at immutable commit
`ed3fa6b8a30594eeb791160563942ba115581aa0`. The port vendors only the maximal inequality and
pointwise theorem modules. Relative to upstream, `MaximalErgodic.lean` changes the renamed mathlib
identifier `integrable_finsetSum` to `integrable_finset_sum`; `Birkhoff.lean` changes only its local
import path. The upstream Apache-2.0 license is included byte-for-byte.

`Proof.lean` instantiates the frozen `InvariantLimitPackage` with the external exact ergodic
corollary and consumes it through the already checked `root_of_invariantLimitPackage` composition.
This supplies bodies for the pointwise-limit, measurability, invariance, ergodic constancy,
integral-identification, invariant-limit, assembly, and exact-root semantics without changing the
canonical statement, registry denominator, or typed graph.

There is one fail-closed architecture mismatch. The frozen
`M1055-A-EXTERNAL-INTEGRATION` node names the earlier
`lua-vr/pointwise-birkhoff@fc06094c...` route, whereas the successful exact proof uses the later
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8...` route. The worker cannot silently rewrite the
frozen obligation registry. Consequently the exact canonical root is kernel inhabited, but the
frozen graph remains open at `M1055-A-EXTERNAL-INTEGRATION` until the integration lane accepts a
registry v2 or append-only route delta. Separately, `M1055-S-FOUNDATION` remains open because this
proof-phase run provides scoped axiom and hygiene evidence, not the complete transitive trust
certificate assigned to downstream validation.

## Obligation Map

| Frozen semantic node | Implementing declaration/body |
|---|---|
| `M1055-A-EXTERNAL-INTEGRATION` | route mismatch: vendored `External/MaximalErgodic.lean` and `External/Birkhoff.lean` are an exact alternative integration, not the frozen `lua-vr` artifact |
| `M1055-L-POINTWISE-LIMIT` | `ErgodicTheory.tendsto_birkhoffAverage_ae` |
| `M1055-L-LIMIT-MEASURABLE` | `stronglyMeasurable_condExp` in the final corollary |
| `M1055-L-LIMIT-INVARIANT` | `ErgodicTheory.condExp_invariants_comp_self` |
| `M1055-L-ERGODIC-CONSTANCY` | `Ergodic.ae_eq_const_of_ae_eq_comp_ae` in `tendsto_birkhoffAverage_ae_integral` |
| `M1055-L-INTEGRAL-IDENTIFICATION` | `integral_condExp`, `integral_congr_ae`, and probability normalization in the final corollary |
| `M1055-T-INVARIANT-LIMIT` | `Stage1Instances.THM_M_1055.invariantLimitPackage_proof` |
| `M1055-T-ASSEMBLE` / `M1055-ROOT` | `root_of_invariantLimitPackage` and `birkhoffErgodicTarget` |

## Provenance

| Artifact | SHA-256 |
|---|---|
| immutable upstream archive | `3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52` |
| upstream `ErgodicTheory/Ergodic/MaximalErgodic.lean` | `6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc` |
| local `External/MaximalErgodic.lean` | `b310154abc8a2407785ddc42dc3c1d4a1e45643cca47c9a2ff77fda7999298d4` |
| upstream `ErgodicTheory/Ergodic/Birkhoff.lean` | `bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a` |
| local `External/Birkhoff.lean` | `de397519e3d49a8362270695ee860365ee1f6b41fd1d13829562d0cf752c0f12` |
| upstream/local `LICENSE` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |

Upstream recorded Lean `4.30.0-rc2` and mathlib
`34f7a6cd150fd7a166958d989d5abab56e9e3d15`. This proof receipt instead comes from direct
source elaboration under this repository's pinned Lean `4.29.0` and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; no upstream build artifact receives proof credit.

## Commands And Results

All commands ran in the worker clone. The existing canonical `.lake` artifacts were reused; no
update, build, dependency clone/fetch, or `.lake` mutation command was run.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1055/check_proof.sh` | 0 | all five source modules elaborated; exact root type checked; five declarations reported sorry-free; seven axiom reports were exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-1055/check_proof.py` | 0 | exact statement, frozen graph, source hashes, immutable revision, port delta, mathlib pin, receipt, and worker packet passed; checker reported the frozen graph dependency-open at the route mismatch |
| `python3 Stage1_Instances/THM-M-1055/check_obligation_tree.py` | 0 | frozen 14-obligation registry and 30 typed edges passed; its pre-proof closure projection remains intentionally unchanged |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1055` | 0 | rank 247, planned, L0/rework-required, theorem-complete false |
| forbidden-mechanism scan over `Proof.lean` and both vendored modules | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom/constant/unsafe declaration, oracle, or native decision shortcut |
| `git diff --check -- Stage1_Instances/THM-M-1055 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status Boundary

This receipt records a self-tested proof attempt and proposes only proof-node state `[_]` pending
master acceptance and route reconciliation. The exact machine root is kernel closed in the current
pinned environment, but the frozen proof graph is not closed because its external-integration node
names a different artifact. The generated pre-proof registry and graph remain immutable inputs
rather than worker-edited state. Validation/release, complete transitive
provenance and trust closure, human-source H0 review, readable reconstruction, hermetic replay, and
independent acceptance remain downstream. `audit_complete` and `theorem_complete` are both false.
