# THM-M-0032 anchor-audit validation

Item: `S56-M-0032-ANCHOR_AUDIT`

Base revision: `4ecdda4863162748b3ee70bc4ec842789418145d`

Base tree: `aace54662cd5e9ca38472011f41afdbffdedfa04`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The bounded immutable inventory has been classified. The narrow Lean probe elaborates the exact
target copy and seven relevant pinned interfaces, and its expected-failure check verifies that the
target conclusion is not already synthesized. The two exact-topic external declarations have
terminal bodies `by sorry` and an extra `[IsDomain R]` premise. The other external project supplies
only partial, API-incompatible infrastructure. The root remains `[H1, M3, R4]`; neither audit nor
theorem completion is claimed.

All local Lean work used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation ran. External repositories
were inspected through immutable raw/API responses and were not installed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | rank 1076, planned, L0/rework-required, theorem incomplete |
| `git status --short` | 0 | preflight showed only the automation-created untracked `Formalizations/Lean/.lake` symlink; it was preserved |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision `8a1783...ea95`, tree `bdc39a...5c2b`, clean dependency worktree |
| `rg -n -i '\b(Auslander\|Buchsbaum)\b\|regular local ring.{0,120}(UFD\|unique factor)\|IsRegularLocalRing.{0,120}UniqueFactorization\|UniqueFactorization.{0,120}IsRegularLocalRing' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 1 (expected no match) | no terminal candidate in pinned mathlib source |
| `rg -n -i '\b(Auslander\|Buchsbaum)\b\|IsRegularLocalRing\|regular local ring.{0,120}(UFD\|unique factor)\|UniqueFactorization.{0,120}IsRegularLocalRing'` over every non-mathlib directory in `Formalizations/Lean/.lake/packages/*`, with `-g '*.lean'` | 1 (expected no aggregate match) | no target candidate in another locally materialized pinned package |
| `rg -n -i` with the same aliases over repo-local `*.lean`, excluding this dossier and `.lake` | 1 (expected no match) | no alternate repo-local terminal candidate |
| `lake env lean ../../Stage1_Instances/THM-M-0032/Statement.lean` from `Formalizations/Lean` | 0 | prerequisite exact target and transport re-elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-0032/AnchorAudit.lean` from `Formalizations/Lean` | 0 | seven pinned APIs checked, failed UFD synthesis authenticated, exact target printed; stdout SHA-256 `8d3b1018...9968f` |
| Sourcegraph queries for `IsRegularLocalRing`, `regularLocalRing_isUFD`, and `auslander_buchsbaum_UFD` with forks/archives included | 0 | only mathlib and Atlas matched; exact-name queries lead solely to admitted Atlas declarations/call sites; response hashes recorded |
| GitHub REST repository searches for regular-local/Auslander aliases in Lean | 0 | one topic project and zero Auslander repositories; complete responses, hashes recorded |
| GitHub REST code search for `IsRegularLocalRing language:Lean` | 0 request | HTTP 401 authentication blocker; response SHA-256 `b7dbd173...65e29e` |
| immutable raw/API inspection of `facebookresearch/atlas-lean@34ffed3...` | 0 | target-like files, toolchain, manifest, tree, and license hashed; both target declarations end in `by sorry` |
| immutable raw/API inspection of `JarodAlper/RegularLocalRings@ea5a55e...` | 0 | complete 30-entry tree and three nonempty Lean sources inspected; domain/1D results only, no UFD target |
| immutable tree inspection of `google-deepmind/formal-conjectures@b2e608f...` | 0 | complete 1204-entry tree, no matching aliases; response SHA-256 `76fa3f96...3efc61` |
| `python3 -B Stage1_Instances/THM-M-0032/check_anchor_audit.py` | 0 | immutable pins, blobs/hashes, candidate ledger, status boundary, worker packet, and narrow Lean replay agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0032/anchor-audit.json >/dev/null` and the same command separately for `anchor-audit-receipt.json` and `.stage1-worker-selftest.json` | 0 each | all structured artifacts parsed |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|unsafe\|opaque)\b\|TODO\|FIXME' Stage1_Instances/THM-M-0032/AnchorAudit.lean` | 1 (expected no match) | no proof placeholder, axiom declaration, unsafe/opaque body, TODO, or FIXME |
| `git diff --check -- Stage1_Instances/THM-M-0032 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Known limitations

Search coverage is bounded rather than globally exhaustive. The statement prerequisite and this
node still require master acceptance. Full transitive proof/provenance/trust evidence is impossible
without a terminal proof body and belongs to later phases. `AUDIT-Z` and theorem completion remain
false.
