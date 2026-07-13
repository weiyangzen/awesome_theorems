# THM-M-0957 anchor-audit validation

Item: `S56-M-0957-ANCHOR_AUDIT`.
Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`; base tree:
`b4b092069141ac54ea1ab5a6ea946192a30ec78c`.

## Result

The bounded immutable inventory contains no Lean 4 declaration matching the frozen historical
eventual bound. Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
does contain a substantial, placeholder-free Behrend construction and two terminal bounds. They
use the fixed exponential constant `4`, while the root requires
`2 * sqrt (2 * log 2) + epsilon` for every positive `epsilon`.

The Lean probe checks the two terminal declarations, candidate-own wrappers, and an exact restricted
adapter when the requested constant is at least four. It also proves that the historical constant
at the admissible value `epsilon = 1` is strictly below four. Therefore the terminal conclusion is
not an exact or direct monotonicity wrapper for the root: it supplies a smaller lower-bound
expression at that epsilon. The lower-level construction may support a new sharp optimization, but
that is future proof work, not anchor identity.

All nine inspected imported/local declarations are machine-reported sorry-free. Their axiom sets
are exactly `propext`, `Classical.choice`, and `Quot.sound`. The environment traversal covers
28,265 declarations in 1,079 modules and reports no bodyless nonaxioms or unsafe declarations.
This identifies a prospective `M2` partial family for the next obligation-tree phase, while the
unfrozen and accepted root stays `[H1, M3, R3]`. It does not support `M0`, audit completion, or
theorem completion.

## Discovery Boundary

Repository-local sources and every materialized manifest package were searched at fixed revisions.
Public Sourcegraph queries included forks and archives and were bound to completed response hashes.
GitHub repository searches returned complete zero results for four topic queries before the
anonymous API limit was reached; code search later returned HTTP 403. grep.app returned an HTTP 429
checkpoint. The public hits were mathlib4, its Lean 3 predecessor, or unrelated uses of the name
`Behrend`. This is complete classification of the seven-member frozen inventory, not exhaustive
internet discovery or reviewed saturation.

## Commands And Results

All commands ran in this worker clone on 2026-07-13 Asia/Shanghai. Lean ran from
`Formalizations/Lean` against the existing pinned Lake environment. No `lake update`, `lake build`,
clone, fetch, checkout, or other `.lake` mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0957` | 0 | rank 1491; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD HEAD^{tree}` and `git status --short --untracked-files=all` before edits | 0 | base identity above; only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and `git status --short` | 0 | pinned revision `8a178386...ea95`, tree `bdc39a...5c2b`, clean worktree |
| bounded `rg` searches over tracked repo-local Lean and all eleven materialized manifest packages | 0/1 | exact-topic mathlib module found; no non-mathlib manifest or repo-local root candidate; exit 1 means no match for bounded negative queries |
| mathlib `git log`, `blame`, blob and source/license/olean SHA-256 inspection | 0 | current source blob `7d3eb0...e254`; Lean 4 port ancestor `6dea3c8...3211`; exact source, license, and compiled hashes recorded |
| bounded Sourcegraph, GitHub repository/code, and grep.app HTTP queries | 0 or explicit 403/429 | completed content-hashed results and explicit access failures recorded in the candidate ledger; no global absence claim |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0957/AnchorAudit.lean` | 0 | candidate types and statement mismatches checked; nine sorry-free and axiom reports; closure 28,265/1,079; no bodyless/unsafe declarations; output SHA-256 `782637a17d30fd6035a11f35e536d234400e4d4653ca80b9bd7f345845de2404` |
| the preceding command with `--trust=0` | 0 | narrow kernel recheck passed with the same semantic reports and combined output hash |
| `python3 -B Stage1_Instances/THM-M-0957/check_anchor_audit.py` | 0 | immutable pins, source hashes, seven candidate classifications, exact-root absence, prospective partial family, root M3 boundary, receipt, and worker packet agree |
| `python3 -m json.tool` on the audit JSON files, receipt, and worker packet | 0 | all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0957-anchor-pycache python3 -m py_compile Stage1_Instances/THM-M-0957/check_anchor_audit.py` | 0 | checker compiles without generated files in the owned path |
| comment-aware prohibited-construct scan of `AnchorAudit.lean` and `check_anchor_audit.py` | 1 (expected no match) | no proof escape or prohibited declaration |
| per-file `git diff --no-index --check /dev/null <new-file>` plus `git diff --check` | 0 diagnostic aggregate | no whitespace errors; no-index exit 1 is only the expected new-file difference |

## Status Boundary

This is a provisional node-specific worker self-test pending dependency-ordered master acceptance.
It does not accept the provisional statement prerequisite, freeze obligations, implement the sharp
constant, assign semantic coverage, complete provenance/TCB release closure, repair H1 or R3 debt,
or establish `AUDIT-Z` or `THEOREM-Z`.
