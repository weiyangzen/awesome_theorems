# THM-M-1056 proof recheck (slot 35)

Item: `S56-M-1056-PROOF`

Base revision: `31db90baa4fbe82d253d96d2c04347fa3ba0e479`

Base tree: `37889644dada58f207dc688d8211a9ccad73a9fe`

Attempt date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. No exact proof body was added, no frozen obligation was closed, and
no state change or receipt is proposed. The structured proof graph still
reports the root at `[H1, M3, R3]`, with `M1056-T-CORE` at M4. Older intake and
README projections still display root M4; this proof recheck does not alter
those authorities or silently reconcile the existing projection disagreement.

`.stage1-worker-selftest.json` is deliberately absent because the assigned
proof phase is not self-tested complete.

## First failed proof gate

The first failed gate remains `M1056-T-CORE`: neither this repository nor the
pinned dependency closure contains a placeholder-free inhabitant of
`OseledetsCorePackage`. That package is definitionally the complete universal
target, so `root_of_oseledetsCorePackage` checks conditional composition only.

The target is not vacuous. `SanityInstance.lean` simultaneously realizes every
antecedent for the identity cocycle on the one-point probability space with
fiber `Real` and constructs the requested splitting. The unused-binder
warnings for `hE` and `hT` do not erase the corresponding universal premises.
The projection fields also do not offer a shortcut: a nonzero idempotent
projection has a nonzero fixed vector, so the growth clause remains
substantive.

## Available inputs and unresolved body

`Stage1_Instances/THM-M-1057` now supplies a repository-local Lean 4.29 Kingman
implementation, including `ErgodicTheory.tendsto_kingman_ergodic_means`. This
closes an analytic input only. It does not construct the forward/backward
Lyapunov filtrations, transversality, splitting, or complementary projections
required by this target.

The immutable external candidate
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
contains the substantive theorem `ErgodicTheory.oseledets_splitting`, but it
pins Lean 4.30.0-rc2 and mathlib `34f7a6cd...`; this worker pins Lean 4.29.0 and
mathlib `8a178386...`. The existing read-only scratch backport elaborates 17 of
the candidate's 62 transitive modules and stops at
`ErgodicTheory.Lyapunov.ExteriorNorm.Basic`. A fresh probe using `-t0` at the
Lean command line confirmed that compilation still uses the module's own
default heartbeat limit and, independently of those timeouts, reports
compatibility errors in real-inner-product normal forms, exterior
multilinearity, Euclidean coordinate lemmas, adjoint rewrites, and the
unavailable downstream `compoundMatrix_mul`.

Even a complete backport would prove a matrix/Euclidean submodule theorem, not
the frozen exact target. Checked bodies would still be required to:

- choose continuous coordinates for arbitrary finite-dimensional `E` and
  transport measurability, inversion, both log-integrability hypotheses,
  cocycle iteration, and norm growth;
- convert a measurable internal family of generally nonorthogonal submodules
  into strongly measurable oblique component projections;
- prove those projections idempotent, pairwise disjoint, summing to the
  identity, nonzero, equivariant, and compatible with the simultaneous growth
  limit on one conull set;
- derive positive exponent count and bridge the logarithm conventions.

Importing only the external matrix/submodule theorem would therefore be a
narrower substituted theorem and cannot receive proof credit.

## Fresh validation

All repository commands ran in this worker clone. The automation-provided
`.lake` symlink was reused read-only; no `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | The frozen 19-obligation, 49-edge graph passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3 and core M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to a fresh `/tmp` directory; run the existing `lake env lean` with `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, the pinned package `LEAN_PATH`, and fresh output oleans; remove the directory | 0 | All three modules elaborated. Only unused-variable warnings occurred. Both printed axiom sets were `[propext, Classical.choice, Quot.sound]`; temporary olean hashes were `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...8b7`, and all temporary artifacts were removed. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit: no prohibited Lean declaration token occurs in the owned source. |
| Search THM-M-1057 for the local Kingman declarations | 0 | `tendsto_kingman`, both ergodic variants, `pointwiseLimitPackage`, and `kingmanTarget` were found. |
| Search repository targets and pinned mathlib for an exact Oseledets body | 0 | Only statement/interface files were found; no local or pinned-mathlib terminal Oseledets theorem was found. |
| Compile the cached immutable candidate's `ExteriorNorm.Basic` under the pinned toolchain with command-line `-t0` in read-only scratch space | 1 | The module's own default heartbeat limit still applied to some declarations, and the independent compatibility failures listed above also remained; no module or proof credit resulted. |

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
