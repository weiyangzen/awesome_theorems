# Intake validation

Base revision: `94f6abf9359f26384e0f68bef694dc5b9aae624c` (tree
`e0083f4f402c93febe4419b51498afa8ecf81c06`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, planned-dossier structure, scope and
non-substitution invariants, repository and source-lead provenance, pinned environment identity, a
narrow Lean candidate-API and axiom probe, proof-escape hygiene, JSON integrity, and whitespace.
Because the exact source contract and source-to-Lean matrix transport are not accepted, no
canonical target, expression hash, statement mutation, source closure, or root proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned artifacts and root worker packet make the final tree dirty and nonrelease.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0043` | 0 | rank 1083; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git blame -L 328,333 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa...b74f` |
| download and text inspection of `https://linear.axler.net/LADR4e.pdf` | 0 | official fourth edition SHA-256 `45f821b6...d03`; Theorem 7.31 on book pages 246-247 gives the complex finite-dimensional normal-operator equivalence; source lead only, no H0 |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, pinned commit and x86_64 target above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0043/IntakeProbe.lean)` | 0 | normality, Hermitian, unitary, diagonal, and eigenvalue interfaces elaborated; strict Hermitian candidate reports `[propext, Classical.choice, Quot.sound]`; no root target or proof credit |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | located only the strict Hermitian spectral theorem and its unrelated legacy wrapper; no exact finite normal-matrix unitary-diagonalization declaration; intake discovery only |
| `python3 -m json.tool` on structured intake artifacts and root packet | 0 | all JSON artifacts valid |
| `python3 -B Stage1_Instances/THM-M-0043/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and pin hashes, H1/M3/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0043 .stage1-worker-selftest.json` and scoped new-file checks | 0 | no whitespace diagnostics |

## Known downstream failures

- No primary source passage supports the catalog's Hilbert/1906 attribution, and no source edition,
  exact theorem, incorporated definitions, errata, or independent review is accepted.
- The scalar field, finite index and boundary conventions, normality and unitary predicates,
  diagonal witnesses, equality orientation, and theorem direction are unresolved.
- Axler Theorem 7.31 is a strong modern source lead, but its operator-to-matrix and
  orthonormal-basis-to-unitary transports have not been frozen or checked.
- The pinned Hermitian theorem is only a strict specialization. Canonical expression and
  environment fingerprints, four mutation classes, exhaustive anchor and terminal-body audits,
  discovery protocol, obligation registry, typed graphs, composition, proof, readable
  reconstruction, hermetic replay, deterministic bundle, independent verification, and master
  acceptance remain open.

These failures prevent statement, H0, exact proof, audit-completion, and theorem-completion claims.
They do not invalidate a truthful self-tested `planned` intake that freezes the target boundary and
opens the downstream DAG. Only the integration lane may accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0043-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, source closure, root proof, audit
completion, theorem completion, or master acceptance is claimed.
