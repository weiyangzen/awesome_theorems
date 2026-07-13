# Intake validation

Base revision: `bba12d6e1323b0998c5f255e488c95ef89ab9e4c` (tree
`aa4a56c727a0a616388e4bbdd8ceac1243c3a07d`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, planned-dossier structure, scope and
non-substitution invariants, repository and source-lead provenance, pinned environment identity, a
narrow Lean Smith-interface/axiom probe, JSON integrity, proof-escape hygiene, and whitespace. No
canonical expression is selected because source identity, matrix/module scope, dimensions,
equivalence, divisibility, normalization, uniqueness, and boundary policy remain open.

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
| `python3 scripts/stage1_target.py show THM-M-0060` | 0 | rank 1092; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git blame -L 447,452 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa...b74f` |
| inspect Crossref metadata and abstract for DOI `10.1098/rstl.1861.0016` | 0 | Smith 1861 pages 293-326 identified as a primary historical source lead; response SHA-256 `a5ea5c9c...d16b`; no H0 |
| request publisher PDF for DOI `10.1098/rstl.1861.0016` | 22 | HTTP 403; no immutable source paper or theorem passage admitted; recorded as downstream source blocker |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision/tree above; package worktree clean |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | general-PID Smith basis/submodule APIs and matrix transports found; no direct full integer left/right-unimodular divisibility-normalized matrix declaration found; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0060/IntakeProbe.lean)` | 0 | Smith structure, all five fields, three submodule APIs, and two matrix/linear-map APIs elaborated; existence theorem reports `[propext, Classical.choice, Quot.sound]`; no canonical target or root credit |
| `python3 -m json.tool` on structured intake artifacts and root packet | 0 | all finalized structured artifacts are valid JSON |
| `python3 -B Stage1_Instances/THM-M-0060/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and pin hashes, H1/M3/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0060 -g '*.lean'` | 1 | expected no-match result; no prohibited declaration |
| `git diff --check -- Stage1_Instances/THM-M-0060 .stage1-worker-selftest.json` and scoped new-file checks | 0 | no whitespace diagnostics |

The finalized checker also recomputes the canonical hashes of both structured recipes, the sorted
input manifests for the structure and Lean actions, the dirty non-receipt manifest, and every
non-receipt dirty file. It re-executes the Lean recipe and requires its complete stdout/log digest
`dba598e0...d829`; the structure action is bound to the exact success-line digest
`490829d2...ef2d`. Both actions record start/end/exit, item coverage, declaration coverage, and
their trust boundary. The receipt remains unsigned and explicitly non-content-addressed because it
cannot embed its own digest; integration must recapture it and all raw logs for acceptance.

## Known downstream failures

- The catalog supplies no bibliography, displayed formula, matrix equivalence, normal-form
  convention, or uniqueness boundary.
- Smith's 1861 primary paper is identified, and its metadata abstract is relevant, but the paper's
  exact theorem and proof passage, definitions, corrections, errata, immutable source packet, and
  independent review remain open.
- Matrix versus module formulation, integer versus general PID domain, dimensions, left/right
  equivalence, diagonal and zero conventions, divisibility chain, associate/sign normalization,
  existence versus uniqueness, and degenerate cases remain statement-gate decisions.
- Pinned mathlib proves a relevant diagonal basis/submodule form, but no checked transport maps it
  to an accepted integer-matrix source root, and its structure does not include divisibility or
  uniqueness.
- No canonical Lean expression or environment fingerprint, checked alternate transport, required
  statement mutations, exhaustive anchor and proof-body audit, discovery protocol, obligation
  registry, typed graphs, proof, composition, readable reconstruction, hermetic replay,
  deterministic bundle, independent verification, or master acceptance exists.

These failures prevent statement, H0, exact proof, audit-completion, and theorem-completion claims.
They do not invalidate a truthful self-tested `planned` intake. Only the integration lane may
accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0060-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, source closure, root proof, audit
completion, theorem completion, or master acceptance is claimed.
