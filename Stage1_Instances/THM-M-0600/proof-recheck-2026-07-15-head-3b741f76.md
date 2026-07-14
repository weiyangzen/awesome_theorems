# THM-M-0600 proof recheck at `3b741f76`

Item: `S56-M-0600-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `3b741f76df83670ba151a8f6ad6257bb8b6f6ead`

Base tree: `021c27ee3fae960d30f31e7f932f29401412edb0`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact target
`Stage1Instances.THM_M_0600.MorseLemmaTarget`. No frozen obligation was newly closed; the frozen
root remains `M3`, its engine remains `M4`, and `theorem_complete=false`.

The only checked local proof body is
`Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine`. It consumes an explicit
`MorseNormalFormEngine` premise and therefore checks final composition without constructing the
missing engine or proving the root unconditionally. No `Proof.lean`, proof receipt, or engine
inhabitant exists in this target or in the bounded rev-5.6 worker-clone search.

Pinned mathlib supplies fixed quadratic-form diagonalization, signature accounting, and smooth
inverse/implicit-function ingredients. It does not supply the smooth second-order factorization,
parameterized splitting, finite induction, nonlinear normal-coordinate construction, or open-
neighborhood identity needed here. The first failed root gate is `M0600-T-ENGINE`; its first
central unavailable analytic body is `M0600-L-SPLITTING`. Assuming the engine, proving only a
Taylor approximation or Hessian diagonalization, or weakening neighborhood equality would add a
premise or substitute a weaker theorem.

Because the assigned positive proof phase did not pass, `.stage1-worker-selftest.json` is
deliberately absent and the item remains `[ ]`.

## Validation

All checks ran in this worker clone. The automation-provided `.lake` symlink to canonical pinned
artifacts was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. Temporary Lean output was removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0600` | 0 | rank 638; planned `hard_statement_first_partial_verification` lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0600/check_obligation_tree.py` | 0 | 18 obligations and 44 typed edges passed; denominator `071b0844...e93f981`; root open M3 and engine M4 |
| isolated temporary trust-zero Lean replay of `Statement.lean`, then `ObligationTree.lean` with the temporary module prepended to pinned `LEAN_PATH` | 0 | exact statement and conditional composition elaborated; `root_of_morseNormalFormEngine` reported exactly `[propext, Classical.choice, Quot.sound]` |
| pinned mathlib source scan for exact Morse-lemma spellings and nondegenerate critical points | 1 | expected no-match result; no exact Morse-lemma proof source found |
| owned Lean scan for `sorry`, `admit`, `sorryAx`, `native_decide`, axiom/constant/opaque/unsafe/extern declarations, and `implemented_by` | 1 | expected no-match result; no prohibited executable proof construct found |
| pinned mathlib revision/tree and package-status checks | 0 | revision `8a178386...ea95`, tree `bdc39a31...1c2b`, package worktree clean |

The current environment is Lean `4.29.0` at commit `98dc76e3...5b040`, Lake
`5.0.0-src+98dc76e`, and pinned mathlib `8a178386...ea95`. Exact source hashes, full command
summaries, the unchanged debt vector, empty proof-credit arrays, and remaining cut set are recorded
in `proof-recheck-2026-07-15-head-3b741f76.json`.

## Retry Condition

Resume after implementing the frozen smooth Taylor, parameterized splitting, induction, inverse,
normal-coordinate, and neighborhood-identity packages without placeholders, or after locating an
immutable compatible Lean 4 Morse-lemma proof that can be pinned, exact-type transported,
kernel-checked, and provenance-audited without changing the dependency lock.

This is current-base owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0600-PROOF`, propose scheduler state, or support audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
