# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, primary-source discrimination, JSON and scoped invariants, a narrow pinned Lean
substrate probe, bounded repository/mathlib search, prohibited-construct hygiene, and whitespace.
It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The DOI landing page, Crossref record, and publisher scan for E. Szemeredi's "On sets of integers
containing no k elements in arithmetic progression," *Acta Arithmetica* 27 (1975), 199-245, were
inspected outside the repository. The scan includes "no" while current landing-page and Crossref
metadata omit it. The landing page and Crossref hashes are `22bdf5db...59ac3` and
`c98e0d4e...7f9a8`. The image-only 24-page, 1,830,546-byte PDF has SHA-256
`78620216...2d2d0`. No source file was added to the repository. The scan was not fully transcribed,
and no immutable H0 source admission, complete definition/assumption/proof/errata mapping, or
independent review is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0948` | 0 | rank 1021; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6924,6929 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://doi.org/10.4064/aa-27-1-199-245' -o /tmp/thm-m-0948-doi.html`; `sha256sum` | 0 | dated mutable discovery input: matching title, author, journal 27 (1975), pages 199-245, and DOI; 40,344-byte HTML, SHA-256 `22bdf5db...59ac3`; not a replay-stable validation recipe |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.4064/aa-27-1-199-245' -o /tmp/thm-m-0948-crossref-work.json`; `jq`; `sha256sum` | 0 | dated mutable discovery input: matching bibliographic metadata; 1,520-byte JSON, SHA-256 `c98e0d4e...7f9a8`; not a replay-stable validation recipe |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://www.impan.pl/shop/publication/transaction/download/product/100627' -o /tmp/thm-m-0948-szemeredi.pdf`; `file`; `wc -c`; `pdfinfo`; `pdffonts`; `pdfimages -list`; `sha256sum` | 0 | dated mutable discovery input: image-only PDF 1.3; 24 pages; 1,830,546 bytes; no embedded fonts; each page has a full-page raster plus a repeated small logo image; SHA-256 `78620216...2d2d0`; not a replay-stable validation recipe |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...2d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0948/IntakeProbe.lean)` | 0 | six adjacent density, three-term-progression, and finite-color APIs elaborated; complete output SHA-256 `f069f4c1...069388` |
| bounded case-insensitive full-Szemeredi search over pinned mathlib and repo-local Lean | 0 | only two regularity-module comment matches; no source-identical arbitrary-length positive-density declaration; not a complete anchor audit or external absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0948-pycache python3 -m py_compile Stage1_Instances/THM-M-0948/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0948/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, source hashes, null target, artifact inventory, packet agreement, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0948/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0948 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked new-file coverage comes from the preceding no-index checks |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0948-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source transcription and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. These failures prevent statement,
audit-completion, and theorem-completion claims, but they do not invalidate the planned intake.
