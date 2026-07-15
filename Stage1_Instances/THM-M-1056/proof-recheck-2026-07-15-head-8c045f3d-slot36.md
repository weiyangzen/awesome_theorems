# THM-M-1056 proof recheck: blocked

Item: `S56-M-1056-PROOF`

Attempt: 2026-07-15 (Asia/Shanghai)

Base revision: `8c045f3d21e3e747c39dd266f581367b08bddd8b`

Base tree: `9910c8170c82875bd17db434d6a9dbf3ac340d94`

## Verdict

The assigned proof phase remains `blocked`. No proof body was added, no frozen
obligation was closed, and no state change or receipt is proposed. The root
remains `[H1, M3, R3]`; its minimal open proof cut is `M1056-T-CORE`, which
remains M4. Because the proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.

`OseledetsCorePackage` is definitionally the same full universal proposition as
the canonical target. Thus `root_of_oseledetsCorePackage` is only a conditional
identity composer. `SanityInstance.lean` constructs a genuine splitting for
the admissible one-point identity cocycle, but that special case cannot prove
the target's universal quantification over every invertible cocycle.

## Proof Search Boundary

The pinned repository closure has no terminal Oseledets proof. Repo-local
`THM-M-1057` supplies placeholder-free Kingman theorems, including
`ErgodicTheory.tendsto_kingman_ergodic_means`, but that closes only one analytic
input. It does not construct the forward and backward Lyapunov flags,
transversality, measurable complementary projections, equivariance, or
simultaneous vector growth required by `LyapunovSplitting`.

The only substantive external candidate remains
`ErgodicTheory.oseledets_splitting` from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
It pins Lean 4.30.0-rc2 and mathlib `34f7a6cd...`, whereas this target pins Lean
4.29.0 and mathlib `8a178386...`. The pre-existing scratch backport had
elaborated 17 of the candidate's 62 transitive modules and stopped at module
18, `ErgodicTheory.Lyapunov.ExteriorNorm.Basic`.

This attempt copied that scratch tree to `/tmp` and continued the module-18
compatibility work without touching the repository or `.lake`. Raising the
file-local heartbeat budget and adapting several changed inner-product,
exterior-multilinear, Euclidean-coordinate, and adjoint proof terms reduced the
fresh failure from 13 reported errors to 8. The remaining failures concern two
real-coordinate inner normal forms, the coercion to
`exteriorPower.ιMulti.toMultilinearMap`, dependent `Pi.single` inference, and
three adjoint rewrite orientations. No module-18 olean was produced. The final
scratch log has SHA-256
`3a436850f9ca4d93bf93f09bc3c634f0d66c782e71a0d64120d85f26750c7074`;
scratch sources, edits, and logs are outside the owned artifact and receive no
proof credit.

Even a complete compatibility port would not directly inhabit the frozen
target. The external theorem returns a measurable internal direct sum of
submodules for a Euclidean matrix cocycle. An exact wrapper must additionally:

- choose coordinates for arbitrary finite-dimensional normed Borel `E` and
  transport strong measurability, inversion, both log-integrability
  hypotheses, cocycle iterates, and equivalent-norm growth;
- construct strongly measurable oblique component projections from the
  internal direct sum, rather than use generally non-disjoint orthogonal
  projections;
- prove idempotence, pairwise annihilation, sum-to-identity, nonzero,
  equivariance, positive count, fixed-space identification, and the target's
  common-conull-set growth field;
- align `Real.posLog`, normalization, and cocycle conventions.

Importing only the matrix/submodule theorem would therefore substitute a
narrower theorem and is not legal root closure.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, network action, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; rework required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1056/check_statement.py` | 0 | Exact expression SHA-256 `8e1a96a...403b`; all four frozen mutations were distinguished under Lean 4.29.0 and mathlib `8a178386...`. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | Passed 19 obligations and 49 typed edges; denominator `5246a9d...b57828`; root M3 and core M4 remain open. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status check | 0 | Pinned revision `8a178386...95`, tree `bdc39a31...b2b`, clean package worktree. |
| Fresh `/tmp` replay of `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` using the pinned Lean executable, existing package `LEAN_PATH`, `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, and fresh oleans | 0 | All three modules elaborated. The conditional composer and sanity theorem reported `[propext, Classical.choice, Quot.sound]`; olean SHA-256 values were `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...178b7`. |
| `rg -n '^\s*(sorry|admit|axiom)(\s|$)|sorryAx|^\s*unsafe\s|implemented_by|^\s*extern\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| Search repo targets and pinned mathlib for an Oseledets terminal declaration | 0 | Found only target/interface definitions; no local or pinned-mathlib terminal proof. |
| Search `THM-M-1057` for Kingman terminal declarations | 0 | Found the three repository-local Kingman theorems and its package/root bodies. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 LEAN_PATH=/tmp/m1056-module18-slot36:$(lake env printenv LEAN_PATH) timeout 1200 lake env lean --root=/tmp/m1056-module18-slot36 -o /tmp/m1056-module18-slot36/ErgodicTheory/Lyapunov/ExteriorNorm/Basic.olean /tmp/m1056-module18-slot36/ErgodicTheory/Lyapunov/ExteriorNorm/Basic.lean` | 1 | Scratch module 18 still has 8 errors; no olean or proof credit was produced. |
| `python3 -m json.tool` on the current blocker JSON; `git diff --check -- Stage1_Instances/THM-M-1056`; `test ! -e .stage1-worker-selftest.json` | 0 | The structured blocker parses, the owned diff has no whitespace errors, and the completion self-test manifest is absent. |

## Reopen Condition

Resume after the immutable Oseledets closure is compatibly ported or equivalent
placeholder-free local bodies exist, and after the coordinate, integrability,
measurable-oblique-projection, equivariance, count, growth, exact-type,
provenance, and trust bridges are implemented and kernel-checked.

## Status Boundary

This is current-base, nonrelease blocker evidence only. Lifecycle remains
`planned -> planned`; accepted receipt IDs are empty; audit completion and
theorem completion are false. It does not satisfy the proof item or authorize
validation, release, checklist edits, or master acceptance.
