# Intake validation

Base revision: `540472523b6c0717ed925193071191f81f62d6eb` (tree
`64b0c81418ef2c97b0250188444c672b9ae885d0`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, planned-dossier structure, scope and
non-substitution invariants, repository and source-lead provenance, pinned environment identity, a
narrow Lean API/candidate-shape/axiom probe, JSON integrity, proof-escape hygiene, and whitespace.
No canonical expression is selected because source identity, domain generality, dimensions, minor
conventions, and boundary policy remain open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned artifacts and root worker packet make the final tree dirty and nonrelease.

## Environment

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
| `python3 scripts/stage1_target.py show THM-M-0048` | 0 | rank 1088; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git blame -L 363,368 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa...b74f` |
| inspect `https://arxiv.org/pdf/1305.0644v1` | 0 | immutable v1 PDF SHA-256 `5a989fa3...80f`; formula (1), Theorem 1/formula (6), and derivation (9) on printed pages 1 and 3-4 mapped as a complete modern source lead; no H0 |
| inspect publisher metadata for DOI `10.1016/0024-3795(93)90371-T` | 0 | Zeng 1993 pages 79-82 identified as a second published proof lead; exact passage not admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision/tree above; package worktree clean |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | no named terminal Cauchy-Binet/Binet-Cauchy theorem found; square `Matrix.det_mul` and relevant interfaces found; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0048/IntakeProbe.lean)` | 0 | seven adjacent APIs and two candidate shapes elaborated; `Matrix.det_mul` reports `[propext, Classical.choice, Quot.sound]`; no canonical target or root proof credit |
| `python3 -m json.tool` on structured intake artifacts and root packet | 0 | all finalized structured artifacts are valid JSON |
| `python3 -B Stage1_Instances/THM-M-0048/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and pin hashes, H1/M3/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0048 -g '*.lean'` | 1 | expected no-match result; no prohibited declaration |
| `git diff --check -- Stage1_Instances/THM-M-0048 .stage1-worker-selftest.json` and scoped new-file checks | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog has no primary source passage or sufficient formula to choose the canonical root.
- Konstantopoulos v1 gives an exact complete modern field-valued theorem and proof lead, but it is
  not catalog-cited or primary; the ring generalization, errata, historical mapping, and independent
  review remain open.
- Full rectangular Cauchy-Binet versus square determinant multiplicativity, coefficient domain,
  dimension inequality, subset ordering, minor orientation, and degenerate cases remain decisions.
- No canonical Lean expression or environment fingerprint, checked transport, or four-class
  statement mutation has been accepted.
- Exhaustive anchor and terminal-body audit, discovery protocol, obligation registry, typed graphs,
  proof, composition, source-faithful readable reconstruction, hermetic replay, deterministic
  bundle, independent verification, and master acceptance remain open.

These failures prevent statement, H0, exact proof, audit-completion, and theorem-completion claims.
They do not invalidate a truthful self-tested `planned` intake. Only the integration lane may
accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0048-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, source closure, root proof, audit
completion, theorem completion, or master acceptance is claimed.
