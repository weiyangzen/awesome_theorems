# Intake validation

Base revision: `122f443c54e4e81d1bf325b07e18ba095823da6d` (tree
`2629bb0cacebd896715a9abad7c52ad60e7bccd0`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation covers target membership, the planned dossier and open task DAG, repository/source
identity, duplicate-target boundaries, JSON integrity, a bounded local formal search, and a narrow
pinned Lean API probe. Crossref metadata for Roch's 1865 article and Forster's 1981 book was
actually inspected. Neither source text nor an exact theorem and definition chain was admitted, so
the candidates remain H1 discovery evidence rather than H0.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0237` | 0 | rank 940, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided `.lake` link was untracked; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 1710,1715 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1515/crll.1865.64.372` | 0 | metadata identifies Roch's 1865 article, journal issue 64, pages 372-376; response SHA-256 `ba216c5...b04`; article text not inspected |
| Crossref query for DOI `10.1007/978-1-4612-5961-9` | 0 | metadata identifies Forster's 1981 Springer book and ISBNs; response SHA-256 `4dd3ce43...dbd`; exact theorem text not inspected |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no build or update run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0237/IntakeProbe.lean)` | 0 | ten adjacent complex-manifold, compactness, holomorphicity, and plane-meromorphic interfaces elaborated; no target theorem declared |
| bounded exact-topic search over repo-local Lean and pinned mathlib | mathlib 1 (no match); repo-local 0 | no pinned-mathlib exact-topic result; repo-local matches occur only in legacy files for other theorem IDs; intake discovery only, not a complete anchor audit |

The final owned JSON checks, scoped checker, worker-packet reconciliation, prohibited-construct
scan, and whitespace checks are recorded in `intake-receipt.json` after finalization. Known
downstream failures are exact source selection and independent review; definition-complete statement
transcription, elaboration, transports, and mutations; immutable formal anchor/provenance audit;
obligation and graph freezes; proof and composition; readable reconstruction; hermetic replay;
deterministic evidence bundling; independent validation; and master acceptance. They prevent audit
and theorem completion but do not invalidate a truthful, self-tested `planned` intake.
