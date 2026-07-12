# Anchor-audit validation

Item: `S56-M-1356-ANCHOR_AUDIT`

Base revision: `7a489588a59dbd7cca44de7e3b8c3bafcb7448f5` (tree
`54d558bf8ed3ea71536ff6a7e6ac7ee67cccfe98`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Result

The exact local target remains a proposition definition with no proof body.
The immutable pinned mathlib inventory contains generic coefficient, root,
complex embedding, submatrix, and determinant APIs, but no theorem connecting
strict left-half-plane roots to positive Hurwitz leading minors. Its only exact
name entry is a declaration-free title in `docs/1000.yaml`.

Bounded Sourcegraph and GitHub repository-metadata searches found no external
Lean 4 candidate. GitHub code search and grep.app were unavailable and are
recorded as blocked lanes, so exhaustive discovery is not claimed. With no
external declaration or body to audit or integrate, the root vector stays
`[H1, M3, R4]`. No proof, audit-completion, or theorem-completion state is
claimed.

## Commands and exact outcomes

Commands ran from the repository root unless another directory is shown.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | rank 966, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pinned mathlib revision/tree/status checks | 0 | commit `8a178386...`, tree `bdc39a31...`, clean worktree |
| pinned mathlib `HEAD:LICENSE` and file hash | 0 | Apache-2.0; blob `8dada3ed...`; SHA-256 `b40930bb...` |
| complete repo-local and 7,871-file pinned-mathlib exact-topic searches | 1 | expected no-match results; no Routh-Hurwitz formal candidate |
| Sourcegraph grouped Lean queries with forks and archives included | 0 | both completed with `matchCount=0` and no skipped index class |
| GitHub repository-metadata queries | 0 | four queries returned `total_count=0`, `incomplete_results=false` |
| GitHub code search and grep.app queries | blocked | HTTP 403/security checkpoint; no negative evidence credited |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1356/Statement.lean)` | 0 | frozen target and statement checks re-elaborated; stdout SHA-256 `f4f17824...` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1356/AnchorAudit.lean)` | 0 | all selected pinned support declarations elaborated |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | immutable pin, exact statement marker, negative local inventory, catalog boundary, external ledger, and `M3` decision agreed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1356-anchor-pycache python3 -m py_compile Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -m json.tool Stage1_Instances/THM-M-1356/anchor-audit.json` | 0 | structured audit parsed |
| prohibited-construct scan over owned Lean/Python anchor artifacts | 1 | expected no match for `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, unsafe, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-1356 .stage1-worker-selftest.json` plus untracked-file whitespace checks | 0 | no whitespace diagnostics |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed. This phase is self-tested pending master acceptance only.
