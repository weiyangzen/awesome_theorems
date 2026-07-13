# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation covers target membership, the `planned` dossier and open task DAG, repository/source
identity, neighbor-target boundaries, JSON integrity, a primary-source discovery lead, bounded
repo-local formal inspection, and a narrow pinned Lean API probe. The Abel 1827 article scan,
volume manifest, opening page, and Crossref metadata were actually inspected. No exact source
proposition or complete definition/proof chain was admitted, so the source remains H1 discovery
evidence rather than H0.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Commands and results

All repository commands ran at the repository root unless a different cwd is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0238` | 0 | rank 1249, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided `.lake` link was untracked; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 1717,1722 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1515/crll.1827.2.101` | 0 | metadata identifies Abel's article, journal, 1827, issue 2, pages 101-181; response SHA-256 `512e1b9...007` |
| retrieve and inspect the Goettingen volume manifest and article `LOG_0018` scan outside the repository | 0 | manifest identifies Abel and 81 article canvases; manifest SHA-256 `bb65164...de3`; 82-page PDF including terms page, 6,310,908 bytes, SHA-256 `95671c3...9d8`; printed page 101 inspected |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no build or update run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0238/IntakeProbe.lean)` | 0 | eight adjacent `PeriodPair` and Weierstrass APIs elaborated; four axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `c70df61...eb2`; no integral or inverse theorem declared |
| bounded exact-topic inspection over repo-local files and pinned mathlib | discovery only | the pinned Weierstrass module supplies adjacent output-side infrastructure; no source-selected integral/inverse root was credited; this is not an exhaustive anchor audit |

Final JSON parsing, scoped checker replays, worker-packet reconciliation, prohibited-construct scan,
and whitespace checks are recorded in `intake-receipt.json`. Known downstream failures are exact
source selection and independent review; definition-complete statement transcription, elaboration,
transports and mutations; immutable formal anchor/provenance audit; obligation and graph freezes;
proof and composition; readable reconstruction; hermetic replay; deterministic evidence bundling;
independent validation; and master acceptance. They prevent audit and theorem completion but do not
invalidate a truthful, self-tested `planned` intake.
