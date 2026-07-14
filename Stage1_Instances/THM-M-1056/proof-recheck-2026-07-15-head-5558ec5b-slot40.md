# THM-M-1056 proof recheck: blocked

Item: `S56-M-1056-PROOF`

Attempt: 2026-07-15 (Asia/Shanghai)

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

## Verdict

The assigned proof phase remains `blocked`. No proof body was added, no frozen
obligation was closed, and no state change or receipt is proposed. The root
remains `[H1, M3, R3]`; its minimal open proof cut is `M1056-T-CORE`, which
remains M4. Because the proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and the item must remain
`[ ]`.

The frozen target is not vacuous. `count_pos` excludes an empty family;
`projection_nonzero` and idempotence give every component a nonzero fixed
vector; and `projection_sum = id` forces the components to cover the fiber.
The one-component identity splitting fails for cocycles with distinct growth
rates. `SanityInstance.lean` separately realizes the hypotheses and conclusion
for the one-point identity cocycle.

`OseledetsCorePackage` is the same full universal proposition as the target.
Thus `root_of_oseledetsCorePackage` is only a checked conditional identity
composer and supplies no proof credit. The repository-local Kingman theorem in
`THM-M-1057` closes one analytic input but does not construct the two Lyapunov
flags, their transverse splitting, measurable component projections,
equivariance, or growth fields.

## External Candidate Recheck

The only substantive terminal candidate remains
`ErgodicTheory.oseledets_splitting` from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
It pins Lean 4.30.0-rc2 and mathlib `34f7a6cd...`; this target pins Lean 4.29.0
and mathlib `8a178386...`.

A pre-existing scratch compatibility tree contains a 62-module, 27,355-line
dependency cut. Only 17 modules have oleans. A fresh pinned-environment replay
of module 18, `ErgodicTheory.Lyapunov.ExteriorNorm.Basic`, failed. The earlier
failure log has SHA-256
`151abf89848940b9e0ccaa5b9cd715de5d54129cc3e333a2c68f5aebf5a70a55`;
the current replay still reports changed real-inner-product and Euclidean
coordinate normal forms, an exterior alternating-map scaling rewrite failure,
heartbeat exhaustion, downstream `compoundMatrix_mul` failures, and adjoint
rewrite failures. Scratch source and oleans are outside the owned artifact and
receive no proof credit.

Even a compatible build would not directly inhabit the frozen target. The
external theorem returns measurable Euclidean submodules and an internal direct
sum for a matrix cocycle. An exact wrapper must still choose and audit
coordinates for arbitrary finite-dimensional `E`, transport strong
measurability, inversion and both log-integrability hypotheses, align cocycle
iterates and growth across equivalent norms, and build strongly measurable
oblique component projections satisfying all algebraic and equivariance laws.
Orthogonal projections onto generally nonorthogonal summands do not satisfy the
target's pairwise-annihilation law. Importing only the external theorem would
therefore substitute a narrower theorem.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_statement.py` | 0 | Exact expression SHA-256 `8e1a96a...403b`; all four frozen mutations were distinguished under pinned Lean 4.29.0 and mathlib `8a178386...`. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | Passed 19 obligations and 49 typed edges; denominator `5246a9d...b57828`; root M3 and core M4. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` plus status check | 0 | Revision `8a178386...95`, tree `bdc39a31...b2b`, clean package worktree. |
| Fresh `/tmp` replay of `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` via `lake env lean`, existing package `LEAN_PATH`, `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, and fresh oleans | 0 | All elaborated; unused-variable warnings only. The conditional composer and sanity theorem reported `[propext, Classical.choice, Quot.sound]`. Olean SHA-256 values: `c55d17a...f64db`, `a75c5008...7f0e`, `ff4de13c...178b7`; temporary files were removed. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s|implemented_by|^\\s*extern\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| Search repository targets and pinned mathlib for an Oseledets terminal body | 0 | Found only the target/interface definitions; no local or pinned-mathlib terminal proof. |
| Fresh `lake env lean --trust=0 -t0` replay of cached port module 18 with the existing pinned package `LEAN_PATH` and output under `/tmp` | 1 | Compatibility module still fails; no olean or proof credit was produced. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent as required for a blocked phase. |

## Reopen Condition

Resume after the immutable Oseledets closure is compatibly ported, or equivalent
placeholder-free local bodies exist, and after the coordinate, integrability,
measurable-oblique-projection, equivariance, count, growth, exact-type,
provenance, and trust bridges are implemented and kernel-checked.

## Status Boundary

This is current-base, nonrelease blocker evidence only. Lifecycle remains
`planned -> planned`; accepted receipt IDs are empty; audit completion and
theorem completion are false. It does not satisfy the proof item or authorize
validation, release, checklist edits, or master acceptance.
