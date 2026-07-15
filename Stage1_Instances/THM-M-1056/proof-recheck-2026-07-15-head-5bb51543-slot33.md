# THM-M-1056 proof recheck: blocked

Item: `S56-M-1056-PROOF`

Attempt: 2026-07-15 (Asia/Shanghai)

Base revision: `5bb515438bd0e1d53584e5243c5d434dfde7158e`

Base tree: `8055b8d863f0978f110a628ab3ccc7ab1e146b12`

## Verdict

The proof phase remains `blocked`. No proof body was added, no frozen
obligation was closed, and no state change or receipt is proposed. The root
remains `[H1, M3, R3]`; its minimal open proof cut is `M1056-T-CORE`, which
remains M4. Because the assigned phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and the item must remain
`[ ]`.

`OseledetsCorePackage` is definitionally the same full universal proposition as
the canonical target. Thus `root_of_oseledetsCorePackage` is only a conditional
identity composer. `SanityInstance.lean` realizes the antecedents and conclusion
for the one-point identity cocycle, so there is no contradictory-typeclass or
vacuity shortcut. A count-one identity projection also cannot solve a general
cocycle: its growth field would require one common exponent for every nonzero
vector.

## Proof Search Boundary

The pinned repository closure has no Oseledets terminal body. Repo-local
`THM-M-1057` now provides placeholder-free Kingman theorems, including
`ErgodicTheory.tendsto_kingman_ergodic_means`, but that closes only one analytic
input. It does not construct the two Lyapunov flags, transversality, measurable
splitting projections, equivariance, or simultaneous vector growth.

The only substantive external candidate remains
`ErgodicTheory.oseledets_splitting` from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
The immutable source snapshot is present only as scratch discovery material and
pins Lean 4.30.0-rc2 plus mathlib `34f7a6cd...`, not this target's Lean 4.29.0
plus mathlib `8a178386...`. A prior read-only compatibility attempt elaborated
17 of the 62 transitive modules. Module 18,
`ErgodicTheory.Lyapunov.ExteriorNorm.Basic`, still has real-inner-product
normal-form failures, a missing `AlternatingMap.map_smul_univ`, Euclidean
coordinate and adjoint rewrite failures, dependent `compoundMatrix_mul`
failures, and heartbeat exhaustion. Its captured failure log has SHA-256
`151abf89848940b9e0ccaa5b9cd715de5d54129cc3e333a2c68f5aebf5a70a55`.
Scratch source and oleans are outside the owned path and receive no proof credit.

Even a successful compatibility port would not directly inhabit the frozen
target. The external theorem returns measurable Euclidean submodules for a
matrix cocycle. An exact wrapper must additionally transport an arbitrary
finite-dimensional normed Borel fiber `E` to coordinates, preserve strong
measurability and both logarithmic integrability hypotheses, align cocycle and
norm-growth conventions, and construct strongly measurable oblique component
projections satisfying idempotence, pairwise annihilation, sum, nonzero,
equivariance, and growth. Importing only the matrix/submodule theorem would be a
narrower substituted result.

## Fresh Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_statement.py` | 0 | Exact expression SHA-256 `8e1a96a...403b`; all four frozen mutations were distinguished under Lean 4.29.0 and mathlib `8a178386...`. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | Passed 19 obligations and 49 typed edges; denominator `5246a9d...b57828`; root M3 and core M4 remain open. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status check | 0 | Pinned revision `8a178386...95`, tree `bdc39a31...b2b`, clean package worktree. |
| Fresh `/tmp` replay of `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` with existing package `LEAN_PATH`, `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, and fresh oleans | 0 | All three modules elaborated; only unused-variable warnings. The printed axiom sets were `[propext, Classical.choice, Quot.sound]`; olean SHA-256 values were `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...178b7`. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| Search repo targets and pinned mathlib for an Oseledets terminal declaration | 0 | Found only target/interface definitions; no local or pinned-mathlib terminal proof. |
| Search `THM-M-1057` for Kingman terminal declarations | 0 | Found all three Kingman theorems and its package/root bodies. |
| Inspect the immutable external snapshot, 62-module order, 17 scratch oleans, and module-18 failure log | 0 | Confirmed the external source is outside the pinned closure and the compatibility attempt remains incomplete. |

The pre-existing untracked `Formalizations/Lean/.lake` symlink makes this
nonrelease evidence. After writing the owned blocker artifacts, their JSON parse,
scoped whitespace check, and deliberate self-test-manifest absence are checked
separately.

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
