# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation covers target membership, the planned dossier and open task DAG, repository/source
identity, source-statement and non-substitution boundaries, JSON integrity, a bounded local formal
search, and a narrow pinned Lean API probe. It does not validate a canonical Jacobi inversion
proposition or proof because neither is frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`; no build or update was run.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0239` | 0 | rank 1250, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided `.lake` link was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1724,1729 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| fixed-revision Encyclopedia of Mathematics MediaWiki API query and decoded-content inspection | 0 | revision 55795; 8,466 decoded wikitext bytes; SHA-256 `5abb3e7b...e76f4`; simultaneous integral, period, theta, normal/exceptional boundaries identified; H1 lead only |
| arXiv `1909.11952v1` PDF retrieval, `pdfinfo`, and `pdftotext` inspection | 0 | 15-page PDF, 209172 bytes, SHA-256 `f47855f...5f42`; abstract's Abel-Jacobi surjectivity wording identified; secondary lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| bounded `rg` search for Jacobi inversion, Abel-Jacobi, Jacobian variety, Riemann theta, and theta divisor over repo-local Lean and pinned mathlib | 0 | seven repo-local planning hits explicitly mark missing Abel-Jacobi/Jacobian bridges; no exact target declaration found; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0239/IntakeProbe.lean)` | 0 | eleven adjacent pinned interfaces elaborated; output SHA-256 `2358cd59...31b0`; no target theorem or proof body |
| `python3 -m json.tool` on owned JSON files and `.stage1-worker-selftest.json` | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0239-pycache python3 -m py_compile Stage1_Instances/THM-M-0239/check_intake.py` | 0 | scoped validator compiled without writing generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0239/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, null canonical target, H1/M4/R4 boundary, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0239/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null <path>` and scoped `git diff --check` | 0 normalized | no whitespace diagnostics; no-index exit 1 was only the expected new-file difference |

## Known open gates

An accepted immutable proof source, exact root selection, complete analytic or algebraic object
model, ordered binders, period/divisor/Jacobian/Abel-Jacobi definitions, surjectivity versus explicit
theta boundary, exceptional cases, historical date and corrections, neighboring-target
reconciliation, and independent source review remain open. So do the canonical Lean expression and
environment fingerprints, checked transports, statement mutations, exhaustive formal anchor and
provenance audit, obligation and graph freezes, proof and composition, readable reconstruction,
trust closure, hermetic replay, deterministic bundle, independent validation, and master
acceptance. They prevent audit and theorem completion but do not invalidate a truthful,
self-tested `planned` intake.
