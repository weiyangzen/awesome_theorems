# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, bibliographic source-family discrimination, JSON and scoped invariants, a narrow pinned
Lean substrate probe, bounded local search, prohibited-construct hygiene, and whitespace. It does
not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref metadata for DOI `10.1006/jctb.1995.1011` confirmed Galvin's title, author, journal, January
1995 date, volume 63, issue 1, and pages 153-158. The normalized record has SHA-256
`88f7f274...c704c`. Cambridge publisher metadata and abstract for Slivnik's 1996 short proof were
inspected; the extract has SHA-256 `70960b8a...3d72` and states that every `k`-edge-colorable
bipartite multigraph is `k`-edge-choosable. Downloads stayed in `/tmp` and are not repository
artifacts. The primary theorem text, original array formulation, exact corollary, errata, and
independent review were not available and are not credited.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0904` | 0 | rank 1044; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6614,6619 -- Docs/researches/math_theorems.md` | 0 | all six uncited Dinitz catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref API query for `10.1006/jctb.1995.1011`, normalized with `jq`, then `sha256sum` | 0 | Galvin title, author, journal locator, 1995 date, and DOI confirmed; normalized SHA-256 `88f7f274...c704c` |
| Cambridge publisher page query for `S0963548300001851`, bounded metadata/abstract extraction, then `sha256sum` | 0 | Slivnik citation and stronger theorem-family abstract inspected; extract SHA-256 `70960b8a...3d72` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0904/IntakeProbe.lean)` | 0 | eight ordinary coloring, bipartite, complete-bipartite, and line-graph APIs elaborated; output SHA-256 `907604cd...5442` |
| bounded `rg` search for Dinitz, Galvin, list coloring, choosability, and list chromatic in pinned mathlib and repo-local Lean | 1 (expected no match) | no target theorem or list-coloring framework found; ordinary coloring and line-graph substrate were separately recorded; not a complete anchor audit or external absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0904-pycache python3 -m py_compile Stage1_Instances/THM-M-0904/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0904/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null formal target, exact artifact inventory, packet agreement, and six open downstream tasks agree |
| `python3 Stage1_Instances/THM-M-0904/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0904 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0904-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. These failures prevent statement,
audit-completion, and theorem-completion claims, but they do not invalidate the planned intake.
