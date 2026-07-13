# THM-M-1056 proof recheck at `18ff7447`

Item: `S56-M-1056-PROOF`

Date: `2026-07-14T04:06:15+08:00`

Base revision: `18ff7447208231633bf2e01e8aad3111af56531a`

Base tree: `9ea9aab30253e72b62ef25c80e17b575356fb7b6`

## Verdict

`blocked`. This current-base execution found no placeholder-free inhabitant of
`OseledetsCorePackage`, which is definitionally the complete universal target.
`root_of_oseledetsCorePackage` therefore remains conditional composition, and
`unitIdentitySplitting_nonempty` remains a one-point identity-cocycle sanity
instance rather than a proof of the universal theorem.

No proof body was added, no frozen obligation was closed, and no state change or
receipt is proposed. The root vector remains `[H1, M3, R3]`, the minimal open
root cut remains `M1056-T-CORE`, and theorem completion is false. Because the
assigned proof phase is not genuinely self-tested complete, the root
`.stage1-worker-selftest.json` is deliberately absent.

## External candidate execution

The immutable cached source
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
contains the substantive theorem `ErgodicTheory.oseledets_splitting`. Its own
guarded source records exactly `[propext, Classical.choice, Quot.sound]` for the
headline theorem, and a declaration-token scan found no `sorry`, `admit`,
`axiom`, `sorryAx`, or `unsafe` in its `ErgodicTheory` source tree. This is
candidate provenance evidence only: the candidate uses Lean `4.30.0-rc2` and
mathlib `34f7a6cd...`, while this target is pinned to Lean `4.29.0` and mathlib
`8a178386...`.

A read-only scratch backport under `/tmp` now elaborates the first 17 of the
candidate theorem's 62 transitive local modules with this target's pinned Lean
and mathlib artifacts. Module 17, `Lyapunov/ForwardMeasurable.lean`, required a
compatibility reproof of self-adjointness using `StarAlgEquiv.map_star'`. The
next module, `Lyapunov/ExteriorNorm/Basic.lean`, fails with multiple real API
and proof incompatibilities: changed real-inner-product normal forms, missing
`AlternatingMap.map_smul_univ`, adjoint rewrite changes, and consequent unknown
constants. This is not a direct import or a completed compatible port.

Even a complete port would not yet inhabit the frozen target. The candidate
returns measurable submodules and `DirectSum.IsInternal` for a matrix cocycle on
`EuclideanSpace Real (Fin d)`. Exact closure additionally requires checked:

- continuous coordinates for arbitrary finite-dimensional normed Borel `E`;
- strong-measurability, inverse, both log-integrability, iterate, and growth
  transports through the coordinate conjugacy;
- strongly measurable oblique component projections from the measurable
  internal direct sum, with idempotence, pairwise annihilation, sum, nonzero,
  equivariance, and simultaneous growth.

Orthogonal projectors onto the candidate's generally nonorthogonal summands are
not component projections. A viable future construction is to form their frame
operator `S = sum_i P_i`, prove its measurable inverse on the conull internal-
sum set, and define the oblique maps by `Q_i = P_i * S^-1`; none of those exact
bridges is implemented. Importing only the candidate would therefore prove a
narrower, differently typed theorem and cannot receive root credit.

## Validation

All repository checks reused the automation-provided canonical pinned `.lake`
artifacts read-only. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was run. The untracked `.lake` symlink makes this nonrelease
evidence. Scratch candidate edits and outputs stayed below `/tmp`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248, lifecycle `planned`, rework required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | 19 obligations and 49 typed edges passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root M3 and core M4 remain open. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` with fresh temporary oleans | 0 | All three elaborated. Conditional composition and the sanity theorem each reported `[propext, Classical.choice, Quot.sound]`. Temporary olean SHA-256 values were `c55d17a...f64db`, `a75c500...7f0e`, and `ff4de13c...8b7`; the temporary directory was removed. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited declaration token occurs in owned Lean sources. |
| Same prohibited-token scan over the cached external `ErgodicTheory` source | 1 | Expected no-match exit; no prohibited declaration token was found. |
| Named terminal search for Oseledets, multiplicative ergodic, or Kingman in pinned Mathlib | 1 | Expected no-match exit; pinned Mathlib has no named terminal theorem. |
| Scratch compile cached external modules 17 and 18 with pinned `lake env lean`, `--trust=0`, and `LEAN_NUM_THREADS=1` | 0, 1 | Compatibility reproof made module 17 pass; module 18 failed at `ExteriorNorm/Basic.lean` with multiple API/proof incompatibilities, including missing `AlternatingMap.map_smul_univ`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `8a178386...95`, tree `bdc39a31...b2b`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent. |

The isolated replay copied the three owned Lean modules to a fresh `/tmp`
directory, obtained the pinned search path with `lake env printenv LEAN_PATH`,
and elaborated them in dependency order with `LEAN_NUM_THREADS=1`, `--trust=0`,
and fresh output paths. It started at `2026-07-14T04:03:57+08:00`, ended at
`2026-07-14T04:05:40+08:00`, and removed the temporary directory.

## Retry condition

Resume after placeholder-free implementations of the frozen core packages are
available, or after the immutable external development is compatibly ported
together with kernel-checked coordinate, integrability, measurable-oblique-
projection, equivariance, growth, exact-type, provenance, and trust transports.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-1056-PROOF`, propose checklist state, or support audit, theorem,
validation, release, or master-completion claims.
