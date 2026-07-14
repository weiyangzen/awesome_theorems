# THM-M-1056 proof attempt: blocked

Item: `S56-M-1056-PROOF`

Attempt: 2026-07-15 (Asia/Shanghai)

Base revision: `3b741f76df83670ba151a8f6ad6257bb8b6f6ead`

Base tree: `021c27ee3fae960d30f31e7f932f29401412edb0`

## Verdict

The assigned proof phase is `blocked`. No proof body was added, no frozen
obligation was closed, and no state change or receipt is proposed. The root
remains `[H1, M3, R3]`; its minimal open proof cut is `M1056-T-CORE`, which
remains M4. Because this phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and the item must remain
`[ ]`.

`OseledetsCorePackage` has the same full universal proposition as the target.
Consequently, `root_of_oseledetsCorePackage` is only a checked conditional
composer. `SanityInstance.lean` realizes every antecedent and the conclusion
for the one-point identity cocycle, so it rules out a contradictory-hypothesis
or vacuous-conclusion shortcut without proving the universal theorem.

## Proof Search Result

Repository-local `THM-M-1057` now supplies placeholder-free Kingman theorems,
including `ErgodicTheory.tendsto_kingman_ergodic_means`. That closes one
analytic input only. It does not construct the forward and backward Lyapunov
flags, their transversality and splitting, or measurable component
projections.

The only substantive terminal candidate found is the immutable theorem
`ErgodicTheory.oseledets_splitting` from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
It pins Lean `4.30.0-rc2` and mathlib `34f7a6cd...`, while this target pins Lean
`4.29.0` and mathlib `8a178386...`. A pre-existing read-only scratch port has
17 of its 62 transitive modules elaborated. Module 18,
`ErgodicTheory.Lyapunov.ExteriorNorm.Basic`, still fails under the pinned
environment. The captured failure log has SHA-256
`151abf89848940b9e0ccaa5b9cd715de5d54129cc3e333a2c68f5aebf5a70a55`
and reports incompatible real-inner-product normal forms, a missing
`AlternatingMap.map_smul_univ`, failed Euclidean-coordinate and adjoint
rewrites, downstream `compoundMatrix_mul` failures, and heartbeat exhaustion.
Scratch files and oleans are not owned artifacts and receive no proof credit.

Even a complete compatible port would not directly inhabit the frozen target.
The external theorem assumes a measurable matrix cocycle and returns measurable
Euclidean submodules with an internal direct sum. An exact wrapper still has to:

- choose continuous coordinates for arbitrary finite-dimensional `E` and
  transport strong measurability, inversion, both log-integrability
  hypotheses, cocycle iterates, and norm growth;
- construct strongly measurable oblique component projections from the
  generally nonorthogonal internal direct sum;
- prove their idempotence, pairwise annihilation, sum, nonzero, equivariance,
  positive count, and simultaneous growth fields;
- bridge the logarithm and normalization conventions.

Orthogonal projections onto nonorthogonal summands do not satisfy the target's
pairwise-annihilation law. Importing only the matrix/submodule theorem would
therefore be a narrower substituted theorem and is prohibited.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_statement.py` | 0 | Exact expression hash `8e1a96a...403b`; all four frozen statement mutations were distinguished under the pinned Lean 4.29.0/mathlib revision. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | Passed the frozen 19-obligation, 49-edge graph; denominator `5246a9d...b57828`; root M3 and core M4 remain open. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status check | 0 | Revision `8a178386...95`, tree `bdc39a31...b2b`, clean package worktree. |
| Fresh `/tmp` replay of `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` with the existing package `LEAN_PATH`, `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, and fresh oleans | 0 | All three elaborated; only unused-variable warnings. The conditional composer and sanity result reported `[propext, Classical.choice, Quot.sound]`. Olean SHA-256 values were `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...178b7`; the temporary directory was removed. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| Search repository targets and pinned mathlib for an Oseledets terminal body | 0 | Found only the target/interface definitions; no local or pinned-mathlib terminal proof. |
| Search `THM-M-1057` for the Kingman terminal declarations | 0 | Found all three Kingman theorems plus its exact package and root bodies. |
| Inspect the cached immutable source, 62-module order, 17 scratch oleans, and module-18 log | 0 / prior compile exit 1 | The external theorem is not in the pinned closure and its compatibility port remains incomplete. |
| Parse the structured blocker; run whitespace checks on both new artifacts; assert `.stage1-worker-selftest.json` is absent | 0 | JSON parsed, neither file emitted a whitespace diagnostic, and the completion self-test manifest is absent. |

## Reopen Condition

Resume after the immutable Oseledets closure is compatibly ported or equivalent
placeholder-free local bodies exist, and after the coordinate, integrability,
measurable-oblique-projection, equivariance, count, growth, exact-type,
provenance, and trust bridges are implemented and kernel-checked. Until then
`S56-M-1056-PROOF` cannot truthfully receive `[_]` credit.

## Status Boundary

This is current-base, nonrelease blocker evidence only. Lifecycle remains
`planned -> planned`; accepted receipt IDs are empty; audit completion and
theorem completion are false. It does not satisfy the proof item or authorize
validation, release, checklist edits, or master acceptance.
