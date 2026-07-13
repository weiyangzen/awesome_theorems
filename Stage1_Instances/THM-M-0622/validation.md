# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba`.
Base tree: `7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`.

The worker reused the automation-provided canonical `.lake` symlink read only. No `lake update`,
`lake build`, dependency clone/fetch, package mutation, theorem declaration, or proof was run. The
initial worktree contained only that symlink, so this is dirty nonrelease worker evidence.

## Commands and results

Commands ran at the repository root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0622` | 0 | rank 1316, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 4615,4620 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI metadata and Göttingen IIIF manifest/PDF inspection | 0 | Tietze's 1915 article, pages 9-14, and Satz 3 were located; manifest SHA-256 `14f770f1...5fc6`, PDF SHA-256 `bdfb309a...7872`; primary lead only, no H0 |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned revision `8a178386...e95`, tree `bdc39a31...e2b`; package worktree clean |
| bounded repository and pinned-mathlib exact-topic inspection | 0 | no theorem-specific prior artifact; located generic, bounded, range-preserving, real-instance, vector-valued, and 1000-theorems candidates; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0622/IntakeProbe.lean)` | 0 | nine exact-topic APIs elaborated; two axiom reports are `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `2c181bdf...7435`; no target or proof declared |
| `python3 -m json.tool` on the three structured owned artifacts and root packet | 0 | all JSON artifacts parse after finalization |
| `python3 -B Stage1_Instances/THM-M-0622/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M3/R4 null-target boundary, source and pin hashes, exact inventory, receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0622 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; scoped validator checks every untracked file's text hygiene |

## Validation scope

The Lean probe authenticates adjacent pinned interfaces only. It does not establish that one is the
canonical catalog target, audit terminal proof bodies, or accept its axioms and transitive trust
closure. The primary scan supports attribution and a bounded metric-space theorem, but a visual
inspection is not an independent transcription, translation, assumption crosswalk, proof review,
or historical-to-modern transport certificate.

## Known downstream failures

- No independently accepted proposition fixes the historical versus modern theorem, codomain,
  boundedness, norm or range preservation, normality/T1 convention, binders, or boundary cases.
- The primary scan lacks an independently reviewed transcription/translation, proof-node map,
  correction/errata audit, and checked implication to the catalog's normal-space wording.
- No canonical Lean expression, minimal-import result, expression/environment fingerprint,
  checked transport, or statement mutation certificate exists.
- The anchor and proof-body audit, discovery protocol, obligation registry, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle, and
  independent verification remain open.
- Master acceptance is pending.

These failures block the statement and theorem-completion gates. They do not invalidate a truthful,
self-tested `planned` intake that records the exact ambiguity, sources, candidates, ownership, and
open downstream DAG. Only the integration lane may accept the provisional worker receipt.
