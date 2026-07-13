# Intake validation

Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5` (tree
`aaa82721074fccea81033a9a18d21652af89f8e4`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, planned-dossier structure, source and
non-substitution boundaries, repository provenance, pinned environment identity, a narrow Lean
API/candidate-shape/axiom probe, JSON and validator integrity, prohibited-construct hygiene, and
whitespace. No canonical expression is selected because the catalog omits the displayed formula,
source identity, scalar domain, matrix shapes, rank convention, association, and boundary policy.

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
| `python3 scripts/stage1_target.py show THM-M-0049` | 0 | rank 1519; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git blame -L 370,375 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa...b74f` |
| inspect `https://arxiv.org/pdf/1909.13202v1` | 0 | immutable v1 PDF SHA-256 `390811a8...200a`; printed page 1 supplies the conventional formula and quotient-space proof as a complete modern source lead; no H0 |
| inspect Crossref metadata for DOI `10.1080/03081087908817301` | 0 | Wang 1979, pages 79-82, identified as a second theorem-name lead; exact passage not admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision/tree above; package worktree clean |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | no named terminal Frobenius triple-product rank theorem found; two-factor, zero-product, composition, transport, and rank-nullity interfaces found; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0049/IntakeProbe.lean)` | 0 | ten adjacent APIs and one candidate triple-product shape elaborated; three adjacent theorems report `[propext, Classical.choice, Quot.sound]`; no canonical target or root proof credit |
| `python3 -m json.tool` on structured intake artifacts and root packet | 0 | all four finalized JSON documents parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0049-pycache python3 -m py_compile Stage1_Instances/THM-M-0049/check_intake.py` | 0 | scoped validator compiles without writing generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0049/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and pin hashes, H1/M3/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0049 -g '*.lean'` | 1 | expected no-match result; no prohibited declaration |
| `git diff --check -- Stage1_Instances/THM-M-0049 .stage1-worker-selftest.json` and scoped new-file checks | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog has no primary source passage or sufficient formula to choose the canonical root.
- Taylor v1 gives an exact complete modern field-valued theorem and proof lead, but it is not
  catalog-cited or historical primary evidence; its genealogy, assumptions, errata, translation,
  source-to-node mapping, and independent review remain open.
- The triple-product identity, scalar domain, matrix index types, multiplication association, rank
  convention, inequality presentation, and degenerate cases remain statement decisions.
- No canonical Lean expression or environment fingerprint, checked transport, or four-class
  statement mutation has been accepted.
- Exhaustive anchor and terminal-body audit, discovery protocol, obligation registry, typed graphs,
  proof, composition, source-faithful readable reconstruction, hermetic replay, deterministic
  bundle, independent verification, and master acceptance remain open.

These failures prevent statement, H0, exact proof, audit-completion, and theorem-completion claims.
They do not invalidate a truthful self-tested `planned` intake. Only the integration lane may
accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0049-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, source closure, root proof, audit
completion, theorem completion, or master acceptance is claimed.

