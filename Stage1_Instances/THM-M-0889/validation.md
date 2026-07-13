# Intake validation

## Boundary

This validation covers only `S56-M-0889-INTAKE`: target membership, the planned dossier, source
and scope discrimination, the open downstream DAG, pinned adjacent Lean APIs, and artifact hygiene.
It does not validate a canonical mathematical or Lean statement. The catalog does not choose among
the primary paper's distinct candidate roots, so exact elaboration and statement mutations belong
to the still-open statement phase.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was preserved read-only and points to the canonical pinned
artifacts. No update, build, dependency fetch, or `.lake` mutation was run. This is nonrelease
worker evidence.

## Source inspection

The author-hosted 16-page AM85 scan (876378 bytes, SHA-256
`5942686400daeac3383624c285ae24d795f39de838726d5fa24c231a4e3fe868`) was inspected with bounded
text extraction and page-image checks. Section 2, Lemma 2.1, Theorems 2.5 through 2.7, Theorem 4.3,
and Remark 4.4 establish a matching source family and multiple inequivalent roots. Crossref DOI
metadata and the author's publication list corroborate its identity. No source selection or
independent review is accepted, so the source class is `H1`, not `H0`.

## Environment fingerprint

- Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`; tree
  `43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`.
- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All commands ran at the repository root unless a different `cwd` is stated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0889` | 0 | rank 1439; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6509,6514 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| author-hosted PDF, Crossref, and author publication-list retrieval; `pdftotext` plus bounded page inspection | 0 | exact bibliographic family and competing source roots recorded; mutable response/PDF hashes captured |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake match the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` plus package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0889/IntakeProbe.lean)` | 0 | eleven adjacent graph, distance, degree, matrix, positivity, and spectrum APIs elaborated; output SHA-256 `0521eb...b835`; no target or proof |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 0 | one unrelated legacy spectral-gap phrase; no target-family pinned-mathlib occurrence; intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `compile` of `Stage1_Instances/THM-M-0889/check_intake.py` | 0 | validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0889/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned H1/M4/R4 boundary, null target, pins, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0889/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| scoped prohibited-construct scan | 0 | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| byte/newline/trailing-whitespace check plus `git diff --check` | 0 | all ten changed files pass; no whitespace diagnostics |

## Known downstream failures

- No accepted immutable source selection decides which AM85 numbered result or approved later
  formulation this target owns, with complete definitions, proof boundary, corrections, review,
  and reconciliation with `THM-M-0888`.
- Graph model, spectral operator and indexing, expansion invariant, normalization, binder order,
  direction, constants, denominators, and degenerate cases are not frozen.
- No canonical Lean target, minimal imports, expression/environment fingerprint, checked alternate
  transport, or mutation suite exists.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity
boundary and open the downstream DAG. Only the integration lane may accept the provisional receipt.
