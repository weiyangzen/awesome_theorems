# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, primary-source discrimination, JSON and scoped invariants, a narrow pinned Lean API
probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem
statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The arXiv v1 PDF for Michael Elkin's *An Improved Construction of Progression-Free Sets* was
inspected outside the repository. It is 20 pages and 242,272 bytes, with SHA-256
`f2be0497fb1be4653343463a6ca95b647c9c880402f4b1115f77e98c5843022b`. Section 2 definitions and
the bounds at equations (5) and (12) were inspected. DOI metadata confirms a 2010 proceedings
edition and the 2011 journal publication matching the catalog year. These mutable discovery inputs
were not added to the repository or promoted to replay-stable recipes. The journal body, edition
differences, exact transcription, corrections, errata, complete source-node map, and independent
review remain open, so no H0 source admission is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0958` | 0 | rank 1492; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6994,6999 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| arXiv/DOI metadata and PDF discovery with `curl`, `pdfinfo`, `pdftotext`, and `sha256sum` | 0 | matching arXiv v1 and 2010/2011 publication identities; PDF properties and hash shown above; temporary mutable discovery only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...2d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0958/IntakeProbe.lean)` | 0 | seven adjacent progression, extremal-number, interval, and Behrend APIs elaborated; complete stdout SHA-256 `153e163b...59b4f`; no target statement or proof credit |
| bounded case-insensitive Elkin/improved-bound search over pinned mathlib and repo-local Lean | 1 (expected no match) | no source-identical Elkin declaration located; not a complete anchor audit or external absence claim |

Final JSON parsing, scoped invariant replay, worker-packet agreement, prohibited-construct scan, and
untracked-file whitespace checks are recorded in `intake-receipt.json`. The public structural recipe
does not depend on the scheduler-only root packet; a separate worker-only invocation checks the
handoff packet.

## Statement-phase update

The later statement phase selects arXiv `0801.4310v1` as its authoritative statement edition and
adds `Statement.lean`, `statement.json`, `check_statement.py`, `statement-validation.md`, and a
provisional statement receipt. That evidence freezes and elaborates the exact source extremal
inequality, checked witness and zero-based transports, four mutation classes, and boundary
fixtures. See `statement-validation.md` for its exact commands and results. This section preserves
the historical intake command record; `check_intake.py` is reconciled to validate the expanded
dossier without rewriting the provisional intake receipt's historical base or hashes.

## Status boundary

The intake receipt remains provisional evidence for `S56-M-0958-INTAKE` only. The subsequent exact
statement evidence is separately provisional for `S56-M-0958-STATEMENT`; neither is an accepted
node receipt. H0 source admission and independent review, complete anchor audit and discovery
freeze, obligation registry, typed graphs, proof, composition, trust closure, readable
reconstruction, hermetic replay, deterministic release bundle, and independent verification
remain open. These failures prevent audit-completion and theorem-completion claims, but do not
invalidate the planned dossier or the self-tested statement interface.
