# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, primary-source discrimination, JSON and scoped invariants, a narrow pinned Lean API
probe, bounded topic search, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement, exact source-to-Lean transport, candidate proof body, or theorem.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The Crossref record, NLM/PMC article page, and the two primary scanned pages for F. A. Behrend's
1946 PNAS note were inspected outside the repository. Temporary observations on 2026-07-13 gave
SHA-256 values `4bb5f9c4...e2a29fde` (Crossref JSON), `340b20bc...2d9397e` (PMC HTML),
`fe479d87...b4eed62c` (page 331), and `a39daa5b...afc485f` (page 332). No remote source was added
to the repository. The displayed statement was transcribed and independently re-read by a second
worker, but no immutable H0 source admission, accountable reviewer approval, complete correction
or errata audit, or node-level source reconstruction is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0957` | 0 | rank 1491; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6987,6992 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| dated `curl` observations of Crossref, NLM/PMC, and two PMC page images; `sha256sum`; visual inspection | 0 | matching title, author, journal, date, pages, DOI, PMCID, exact source definition, construction, and displayed eventual bound observed; mutable discovery input only, not a replay-stable receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum` on the toolchain, manifest, Behrend module, and 3AP definitions | 0 | hashes `651c8acc...85b1d2`, `321626c8...2d81`, `1f8c1813...15cf65`, and `b325fb63...b28e3` as recorded |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0957/IntakeProbe.lean)` | 0 | eleven relevant pinned definitions, construction interfaces, extremal specification, and bound declarations elaborated; complete output hash recorded in the receipt |
| bounded case-insensitive Behrend/3AP search over repo-local Lean and pinned mathlib | 0 | exact-topic pinned module and downstream Ruzsa-Szemeredi uses located; discovery only, not the complete immutable anchor audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0957-pycache python3 -m py_compile Stage1_Instances/THM-M-0957/check_intake.py` | 0 | scoped validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0957/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M3/R3 boundary, source and pin hashes, null target, candidate inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0957/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0957 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked coverage comes from the preceding no-index checks |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0957-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Immutable source admission and accountable review,
canonical Lean elaboration and statement mutations, exact source/formal transports, formal-anchor
provenance and trust audit, obligation registry, typed graphs, proof/composition credit, hermetic
replay, deterministic release bundle, and independent verification remain open. These failures
prevent statement, audit-completion, and theorem-completion claims, but they do not invalidate the
planned intake.
