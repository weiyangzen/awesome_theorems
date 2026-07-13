# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`.

This validation covers target membership, the planned dossier and open task
DAG, repository-source provenance, source-variant discrimination, JSON and
scoped invariants, a narrow pinned Lean substrate probe, bounded
repository/mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used
read-only. No `lake update`, `lake build`, dependency clone or fetch,
network-triggering Lake operation, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and
nonrelease.

## Source discovery boundary

Crossref and the DOI/Springer surface for Balog and Szemeredi's "A statistical
theorem of set addition," *Combinatorica* 14(3) (1994), 263-268, DOI
`10.1007/BF01212974`, were inspected outside the repository. The observed
Crossref JSON had SHA-256 `abc0fb66...152705`. It confirms bibliographic
identity but supplied no admitted theorem text.

The arXiv PDF for Croot and Borenstein, arXiv `0805.3305v2`, printed page 1,
Theorem 1, was also inspected. The 11-page, 99,315-byte PDF had SHA-256
`0143333b...d1094`. It supplies a precise later restatement of a Gowers
refinement and explicitly notes that Gowers proved more. It is secondary
discovery evidence, not an immutable H0 source admission. No remote source was
added to the repository, and no complete primary-statement, definition,
assumption, proof, correction, errata, or independent-review mapping is
claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13
(`Asia/Shanghai`) unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0944` | 0 | rank 1483; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| catalog, Stage0, manifest, blueprint, DAG, skill, guidelines, and additive-neighbor inspection | 0 | catalog supplies only an ambiguous Freiman/approximate-group gloss; exact BSG statement fields are open |
| `git show bcf3f9f...:Docs/researches/math_theorems.md`; source blob lookup | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; blob `5c1de0c...eef12` |
| `curl -L --fail --max-time 30 -sS 'https://api.crossref.org/works/10.1007/BF01212974'`; `sha256sum` | 0 | dated mutable discovery input: matching title, authors, Combinatorica 14(3), September 1994, pages 263-268, DOI; observed JSON SHA-256 `abc0fb66...152705`; not a replay-stable validation recipe |
| `curl -L --fail --max-time 60 -sS 'https://arxiv.org/pdf/0805.3305v2'`; `file`; `wc -c`; `pdfinfo`; `pdftotext`; `sha256sum` | 0 | dated mutable discovery input: PDF 1.4; 11 pages; 99,315 bytes; printed page 1 Theorem 1 inspected; SHA-256 `0143333b...d1094`; not a replay-stable validation recipe |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and package status | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...2d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0944/IntakeProbe.lean)` | 0 | six adjacent energy, doubling, approximate-subgroup, and covering APIs elaborated; complete output SHA-256 `a1fd840f...61d5e` |
| bounded case-insensitive BSG topic search over pinned mathlib and repo-local Lean | 1 (expected no match) | no Balog/Gowers/popular-sums/source-title or energy-to-small-doubling match; not a complete anchor audit or external absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0944-pycache python3 -m py_compile Stage1_Instances/THM-M-0944/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0944/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, source hashes, null target, artifact inventory, packet agreement, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0944/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0944 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked new-file coverage comes from the preceding no-index checks |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0944-INTAKE` only.
It supports a truthful `planned` dossier, not an accepted node receipt. Exact
source transcription and independent review, canonical Lean elaboration and
statement mutations, complete anchor audit and discovery freeze, obligation
registry, typed graphs, proof, composition, trust closure, hermetic replay,
deterministic release bundle, and independent verification remain open. These
failures prevent statement, audit-completion, and theorem-completion claims,
but they do not invalidate the planned intake.
