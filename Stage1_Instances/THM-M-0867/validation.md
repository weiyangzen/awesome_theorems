# THM-M-0867 intake validation

Validation covers only the `planned` intake for `S56-M-0867-INTAKE`. The existing pinned `.lake`
symlink was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or cache
mutation was run.

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`

Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`

Pinned Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`

Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`

## Commands and results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0867` | 0 | rank 1421; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `?? Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6355,6360 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source discovery: download author-hosted GM XX PDF; `file`; `wc -c`; `sha256sum`; `pdfinfo`; `pdftotext` | 0 | 34-page, 251,605-byte PDF, SHA-256 `327694f0...aa91`; abstract, Introduction first paragraph, and paper-page-29 Theorem 10.5 inspected; discovery input only |
| Crossref DOI metadata request | 0 | authors, title, journal, volume 92 issue 2, pages 325-357, and November 2004 publication confirmed; response SHA-256 `ca748048...27fa` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree shown above; mathlib source worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0867/IntakeProbe.lean)` | 0 | seven adjacent WQO/simple-graph APIs elaborated; complete combined output SHA-256 `3a1d6846...cf5b`; no target or proof declared |
| bounded `rg` exact-topic search over repo-local Lean and pinned mathlib | 1 (expected no match) | no Robertson-Seymour, Wagner-conjecture, graph-minor WQO, or minor-WQO declaration under the recorded patterns; not a complete anchor audit or external absence claim |
| `python3 -m json.tool` on structured owned artifacts and worker packet | 0 | all JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0867-pycache python3 -m py_compile Stage1_Instances/THM-M-0867/check_intake.py` | 0 | scoped validator compiled without writing under the owned path |
| `python3 -B Stage1_Instances/THM-M-0867/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, authority hashes, planned H1/M3/R4 boundary, null formal target, artifact hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0867/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE` and scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only when it represented a clean new-file diff |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0867-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Complete source admission and independent review,
finite-graph and minor-relation design, canonical Lean elaboration and mutations, formal anchor
audit, obligation registry, typed graphs, proof, composition, trust closure, hermetic replay,
deterministic release bundle, and independent verification remain open. These failures prevent
statement, audit-completion, and theorem-completion claims but do not invalidate the planned intake.
