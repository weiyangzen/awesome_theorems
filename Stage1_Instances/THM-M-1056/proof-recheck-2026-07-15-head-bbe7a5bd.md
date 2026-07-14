# THM-M-1056 proof recheck (slot 41)

Item: `S56-M-1056-PROOF`

Base revision: `bbe7a5bd1c72a12f3f43b79b6a4cac3f62d2085a`

Base tree: `aa558ed6f23779c7d2d9a8427775f709d8b7e31b`

Attempt date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. No exact proof body was added, no frozen obligation was closed, and
no state change or receipt is proposed. The structured proof graph still
reports the root at `[H1, M3, R3]`, with `M1056-T-CORE` at M4. Older intake and
README projections retain root M4 wording; this proof worker did not alter
those authorities or silently reconcile the existing projection disagreement.

`.stage1-worker-selftest.json` is deliberately absent because the assigned
proof phase is not self-tested complete.

## First failed proof gate

The first failed gate remains `M1056-T-CORE`: neither the repository nor its
pinned dependency closure contains a placeholder-free inhabitant of
`OseledetsCorePackage`. The package is definitionally the complete universal
target, so `root_of_oseledetsCorePackage` checks conditional composition only.

The target has no vacuity shortcut. `SanityInstance.lean` realizes all
antecedents for the identity cocycle on the one-point probability space with
fiber `Real` and constructs the requested splitting. Count zero is excluded,
and a nonzero idempotent projection has a nonzero fixed vector, so the growth
field is substantive.

## Available proof input and unresolved body

`Stage1_Instances/THM-M-1057` supplies repository-local Lean 4.29 bodies for
Kingman's theorem, including
`ErgodicTheory.tendsto_kingman_ergodic_means`. This closes only an analytic
input. It does not construct the forward/backward Lyapunov flags,
transversality, splitting, complementary projections, equivariance, or the
exact target transports.

The immutable external candidate
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
contains `ErgodicTheory.oseledets_splitting`, but it pins Lean 4.30.0-rc2 and
mathlib `34f7a6cd...`; this worker pins Lean 4.29.0 and mathlib `8a178386...`.
The existing read-only scratch port has 17 of 62 transitive modules elaborated
and stops at `ErgodicTheory.Lyapunov.ExteriorNorm.Basic`. Its captured failure
log has SHA-256
`151abf89848940b9e0ccaa5b9cd715de5d54129cc3e333a2c68f5aebf5a70a55`
and reports incompatible real-inner-product normal forms, exterior
multilinearity, Euclidean-coordinate and adjoint rewrites, downstream
`compoundMatrix_mul`, and module-local heartbeat limits.

Even a complete port would return a Euclidean matrix/submodule splitting, not
the frozen exact target. A checked wrapper must still:

- choose continuous coordinates for arbitrary finite-dimensional `E` and
  transport measurability, inversion, both log-integrability assumptions,
  cocycle iteration, and norm growth;
- construct strongly measurable oblique component projections from the
  generally nonorthogonal internal direct sum;
- prove their idempotence, pairwise annihilation, sum, nonzero, equivariance,
  positive count, and simultaneous growth fields;
- bridge the logarithm and normalization conventions.

Importing only the matrix/submodule theorem would be a narrower substituted
theorem and cannot receive proof credit.

## Fresh validation

All repository commands ran in this worker clone. The automation-provided
`.lake` symlink was reused read-only; no `lake update`, `lake build`, dependency
clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_statement.py` | 0 | The exact expression hash `8e1a96a...403b` and all four frozen statement mutations passed under the pinned toolchain. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | The frozen 19-obligation, 49-edge graph passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3 and core M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to fresh `/tmp`; obtain the existing package `LEAN_PATH` and Lean binary through `lake env`; run each with `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, and fresh output oleans; remove the directory | 0 | All three modules elaborated. Only unused-variable warnings occurred. The two printed axiom sets were `[propext, Classical.choice, Quot.sound]`; temporary olean SHA-256 values were `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...8b7`; all temporary artifacts were removed. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit: no prohibited Lean declaration token occurs in the owned source. |
| Search THM-M-1057 for `tendsto_kingman`, both ergodic variants, `pointwiseLimitPackage`, and `kingmanTarget` | 0 | All five repository-local Kingman declarations were found. |
| Search repository targets and pinned mathlib for an exact Oseledets body | 0 | Only statement/interface files were found; no local or pinned-mathlib terminal Oseledets theorem was found. |
| Inspect the existing read-only immutable-candidate scratch port and its module-18 log | 0 / prior compile exit 1 | 17 of 62 scratch modules have oleans; `ExteriorNorm.Basic` remains incompatible under the pinned environment. No scratch artifact is proof credit. |

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
