# THM-M-1056 proof recheck (slot 35)

Item: `S56-M-1056-PROOF`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

Attempt date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. No proof body was added, no frozen obligation was closed, and no
state change or receipt is proposed. The structured proof graph still reports
the root at `[H1, M3, R3]`, with `M1056-T-CORE` at M4. Older intake and README
projections still display root M4; this recheck does not edit those authorities
or silently reconcile the existing projection disagreement.

`.stage1-worker-selftest.json` is deliberately absent because the assigned
proof phase is not self-tested complete.

## First failed proof gate

The first failed gate remains `M1056-T-CORE`: there is no placeholder-free
inhabitant of `OseledetsCorePackage` in the repository or pinned dependency
closure. That package is definitionally the complete universal target, so
`root_of_oseledetsCorePackage` checks only conditional composition.
`SanityInstance.lean` constructs an admissible one-point identity cocycle and
its splitting. It rules out a vacuity or inconsistent-hypothesis shortcut but
does not prove the universal theorem.

## New repository-local Kingman evidence

The earlier claim that no repository-local Kingman theorem exists is now
obsolete. `Stage1_Instances/THM-M-1057` contains a Lean 4.29 port with:

- `ErgodicTheory.tendsto_kingman` in `KingmanCore.lean`;
- `ErgodicTheory.tendsto_kingman_ergodic` in `KingmanCore.lean`;
- `ErgodicTheory.tendsto_kingman_ergodic_means` in `KingmanMeans.lean`;
- `Stage1Instances.THM_M_1057.kingmanTarget` in `Proof.lean`.

Its proof receipt reports fresh trust-zero elaboration of the eight vendored
Kingman modules and the exact THM-M-1057 proof, with only `propext`,
`Classical.choice`, and `Quot.sound`. This materially improves the available
subadditive-ergodic layer. It does not supply the forward/backward Lyapunov
filtrations, transversality, splitting, or this target's projection structure.

## Immutable Oseledets candidate and port result

The immutable candidate
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
contains the substantive theorem `ErgodicTheory.oseledets_splitting` at
`ErgodicTheory/TwoSided/SplittingAssembly.lean:657`. Its recorded axiom audit is
`[propext, Classical.choice, Quot.sound]`. Upstream pins Lean `4.30.0-rc2` and
mathlib `34f7a6cd150fd7a166958d989d5abab56e9e3d15`; this worker pins Lean 4.29.0
and mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

A read-only scratch backport has 17 of the candidate's 62 transitive modules
elaborated under the worker toolchain, including the now-available Kingman
stack and `Lyapunov.ForwardMeasurable`. Module 18,
`Lyapunov/ExteriorNorm/Basic.lean`, fails before an Oseledets theorem is
available. The failure is substantive rather than a single rename: it includes
real-inner-product normalization goals, missing
`AlternatingMap.map_smul_univ`, failed Euclidean-coordinate and adjoint
rewrites, unavailable downstream `compoundMatrix_mul`, and heartbeats at the
pinned default. The captured failure log has SHA-256
`151abf89848940b9e0ccaa5b9cd715de5d54129cc3e333a2c68f5aebf5a70a55`.
Scratch sources and outputs are outside the owned artifact and are not proof
credit or a dependency installation.

Even a complete 62-module backport would not directly inhabit the frozen
target. A checked exact wrapper must still:

- choose a continuous linear equivalence from arbitrary `E` to
  `EuclideanSpace Real (Fin (Module.finrank Real E))` and conjugate `A`;
- transport strong measurability, determinant/inversion, both positive-log
  integrability assumptions, and the cocycle recurrence;
- convert upstream measurable internal submodules into strongly measurable
  oblique component projections. Orthogonal projections alone do not satisfy
  pairwise annihilation for a nonorthogonal direct sum. A candidate is
  `Q_i = P_i.comp (sum_j P_j)^-1`, whose invertibility, measurability,
  idempotence, disjointness, sum, nonzero, and equivariance laws remain open;
- derive positive exponent count and transport vector growth through the
  non-isometric equivalence using uniform logarithmic norm bounds;
- bridge target `logPlus x = max (Real.log x) 0` with upstream
  `Real.posLog x = max 0 (Real.log x)`.

Importing only the matrix/submodule theorem would therefore be a narrower
substituted theorem, not exact root closure.

## Fresh commands and exact results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; `rework_required: true`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | The frozen 19-obligation, 49-edge graph passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3 and core M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to fresh `/tmp`; run `lake env lean` with the existing canonical package `LEAN_PATH`, `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, and fresh output oleans; remove the directory | 0 | All three modules elaborated. Only unused-variable warnings occurred. `#print axioms` reported `[propext, Classical.choice, Quot.sound]` for the conditional composer and sanity result. Temporary olean SHA-256 values were `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...8b7`; all temporary artifacts were removed. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| Search the THM-M-1057 Kingman modules for the four declarations listed above | 0 | All four repository-local declarations were found. |
| Search repository targets and pinned mathlib for `oseledets_splitting` or an exact root proof | 0 | Only target statement/interface files were found locally; no kernel-checked Oseledets terminal theorem was found. |
| Count scratch closure oleans and inspect module 18 failure log | 0 / compile failure | 17 of 62 modules have scratch oleans; module 18 has the incompatibilities summarized above. |
| `python3 -m json.tool` on `obligation-registry.json`, `typed-graphs.json`, and `validation-specs.json` | 0 | All three structured artifacts parsed. |

The pre-existing untracked `Formalizations/Lean/.lake` is an automation-provided
symlink to the scheduler's canonical pinned cache. This worker used it
read-only and did not run `lake update`, `lake build`, dependency clone, or
dependency fetch.

## Retry condition

Resume after the immutable Oseledets closure is compatibly ported or equivalent
placeholder-free local bodies exist, and after kernel-checked coordinate,
integrability, measurable-oblique-projection, equivariance, count-positivity,
growth, exact-type, provenance, and trust bridges are implemented.

## Status boundary

This is a proof-phase blocker record, not a proof receipt. Lifecycle remains
`planned -> planned`; the minimal open root cut is `M1056-T-CORE`; accepted
receipt IDs are empty; audit completion and theorem completion are false; the
item cannot truthfully receive `[_]`.
