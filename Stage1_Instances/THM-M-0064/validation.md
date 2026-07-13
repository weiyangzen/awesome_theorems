# Intake validation

Base revision: `c5f6fb269f6eb84efa935ee66c4e9bab92495e61` (tree
`7a41063c920c1b9cb849aa35c2f02ec4a4733655`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, planned-dossier structure, source-statement and
non-substitution boundaries, repository provenance, pinned environment identity, a narrow Lean
Abel-Ruffini/solvability interface probe, JSON integrity, proof-escape hygiene, and whitespace. No
canonical expression is selected because source identity, `general` semantics, degree
quantification, fields, radical-solvability encoding, polynomial/Galois bridge, and boundary policy
remain open.

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
| `python3 scripts/stage1_target.py show THM-M-0064` | 0 | rank 1095; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git blame -L 477,482 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa...b74f` |
| inspect publisher metadata for DOI `10.1017/CBO9781139245807.008` and `.004` | 0 | degree-above-four and quintic Abel source leads identified; PDF endpoint returned access-gate HTML; no H0 credited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision/tree above; package worktree clean |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | one radical-to-solvable-Galois direction and nonsolvable symmetric-group results located; no direct generic polynomial root or Galois-realization bridge found; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0064/IntakeProbe.lean)` | 0 | five adjacent APIs and two axiom reports elaborated; no canonical target or root proof declared |
| `python3 -m json.tool` on structured intake artifacts and root packet | 0 | all finalized structured artifacts are valid JSON |
| `python3 -B Stage1_Instances/THM-M-0064/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and pin hashes, H1/M3/R4 null-target boundary, exact inventory, packet agreement, probe replay, and six open tasks agree |
| `rg -n` prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0064 .stage1-worker-selftest.json` plus new-file checks | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog supplies no bibliography, displayed proposition, definition of `general`, coefficient
  or extension field, quantifier order, or radical-solution convention.
- Abel primary-source leads are identified, but exact passages, definitions, proofs, attribution
  and date reconciliation, translation, corrections, errata, immutable source admission, and
  independent review remain open.
- Generic-formula versus counterexample scope, degree exactly five versus every degree at least
  five, fields and characteristic, irreducibility/separability, one root versus splitting field,
  radical towers, roots of unity, and boundary cases remain statement-gate decisions.
- Pinned mathlib proves a relevant necessary condition and symmetric-group nonsolvability, but no
  checked bridge maps an accepted generic polynomial to that group or closes the catalog root.
- No canonical Lean expression or environment fingerprint, checked alternate transport, statement
  mutations, exhaustive anchor and proof-body audit, discovery protocol, obligation registry,
  typed graphs, proof, composition, readable reconstruction, hermetic replay, deterministic bundle,
  independent verification, or master acceptance exists.

These failures prevent statement, H0, exact proof, audit-completion, and theorem-completion claims.
They do not invalidate a truthful self-tested `planned` intake. Only the integration lane may
accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0064-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, source closure, root proof, audit
completion, theorem completion, or master acceptance is claimed.
