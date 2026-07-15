# THM-M-0508 proof recheck at current base

Item: `S56-M-0508-PROOF`

Intent: `prove`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `db0f66d878c785ce802d44a6c3c1d7adb6d9a131`

Base tree: `fe54922cd929b31f0cca2373bca0c79a487bcc17`

## Verdict

`blocked`. No eligible placeholder-free proof body inhabits the exact target
`Stage1Instances.THM_M_0508.VinogradovThreePrimesTarget`. This run adds no proof body, closes no
frozen obligation, and leaves the item `[ ]`. The lifecycle remains `planned`; the root vector
remains `[H1, M4, R3]`.

The local theorem `representationCount_pos_iff` genuinely proves that a positive finite count is
equivalent to three natural prime witnesses. The local theorem
`root_of_eventualPositiveRepresentationCount` is also a genuine checked child-to-root composition,
but it consumes the open proposition `EventualPositiveRepresentationCount`. It therefore cannot be
credited as an unconditional proof of Vinogradov's theorem.

The frozen first open root cut is `M0508-N-FOURIER`, `M0508-B-ARCS`, `M0508-L-MAJOR`,
`M0508-L-SINGULAR`, and `M0508-L-MINOR`. Closing it requires the ternary exponential-sum identity,
major/minor arc construction, major-arc asymptotic, positive singular-series bound, minor-arc
estimate, and eventual-positivity assembly. None has a terminal Lean body in the current closure.

Focused current-base searches found no `Proof.lean`, proof receipt, exact root theorem, or eventual
positivity inhabitant in the dossier, repository-local Lean, scanned rev-5.6 worker clones, or the
pinned mathlib source. `THM-M-0487` freezes a stronger weak-Goldbach statement, but it too has only
conditional scaffolding and a proof blocker. The prerequisite immutable audit found only the
Formal Conjectures declaration with a literal `sorry` body; it is forbidden evidence and was not
imported.

The proof inputs are unchanged since the prior proof attempt at `e3d0fd20`, integrated by
`028e2535`: `Statement.lean`, `ObligationTree.lean`, the frozen registry and graphs, anchor audit,
toolchain, manifest, and Lake configuration retain their recorded content. Assuming eventual
positivity, importing the rejected placeholder, or presenting the conditional composer as the
root would add an open premise or substitute an implication for the target. No such shortcut was
introduced.

## Narrow Validation

All checks ran in this automation clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, network request, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | Rank 882; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0508/check_obligation_tree.py` | 0 | 17 obligations and 86 typed edges passed; denominator `79ff122b...53bc2`; root open M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0508/Statement.lean` | 0 | The exact canonical target elaborated and printed. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0508/ObligationTree.lean` | 0 | The count bridge and conditional composer elaborated; both reported exactly `[propext, Classical.choice, Quot.sound]`; three nonfatal linter warnings appeared. |
| `python3 Stage1_Instances/THM-M-0508/check_anchor_audit.py` | 0 | Bounded audit, ten pinned probes, rejected placeholder candidate, and immutable mathlib pin passed. |
| Focused exact-topic scan over pinned mathlib and repo-local Lean | 0 | Only this dossier and the blocked stronger `THM-M-0487` statement/scaffolding matched; no terminal body was found. |
| Bounded worker-clone scan for `THM-M-0508/Proof.lean` | 0 | Count `0`; no worker proof candidate was present. |
| Prohibited-device scan over owned Lean source | 1, expected | No `sorry`, `admit`, `sorryAx`, axiom/unsafe escape, `implemented_by`, or `native_decide` occurred. |
| Mathlib revision, tree, and package-status checks | 0 | Revision `8a178386...ea95`, tree `bdc39a31...1c2b`, and a clean tracked package worktree. |
| Scoped diff from prior blocker base over frozen proof inputs | 0 | No proof input changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent. |

## Retry Condition

Resume after implementing the frozen Fourier, arc-partition, major-arc, singular-series,
minor-arc, and eventual-positivity packages without placeholders, or after identifying an
immutable compatible Lean 4 proof that can be pinned, exact-type transported, kernel-checked, and
provenance-audited without mutating the dependency lock.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0508-PROOF`, propose provisional or accepted state, or support audit completion, theorem
completion, validation, release, receipt acceptance, or master acceptance. Because the assigned
proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.
