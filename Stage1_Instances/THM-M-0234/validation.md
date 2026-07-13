# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation covers target membership, the `planned` dossier and open downstream DAG, repository
source identity, the `THM-M-0232` duplicate boundary, JSON integrity, a bounded formal search, and
a narrow pinned Lean API probe. The BnF catalog record for Rouche's 1866 work was actually
inspected. Its 1866 date differs from the repository's 1862 field, and no exact theorem passage or
definition chain was accepted, so it remains H1 discovery evidence rather than H0.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0234` | 0 | rank 1246, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided `.lake` link was untracked; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 1675,1694 -- Docs/researches/math_theorems.md` | 0 | both adjacent Rouche records originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| BnF SRU query for `Memoire serie Lagrange Rouche` | 0 | two records identify the 1866 Paris printing, 31 pages, catalog ARK `cb31252939w`, and Gallica ARK `bpt6k165297c`; response SHA-256 `00b613da...b6b` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no build or update run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0234/IntakeProbe.lean)` | 0 | eight adjacent analytic-order, isolated-zero, and divisor interfaces elaborated; no target theorem declared |
| bounded exact-topic search over repo-local Lean and pinned mathlib | 1 | no Rouche-named, argument-principle, or same-zero-count declaration; intake discovery only, not a complete anchor audit |

The final owned JSON checks, scoped checker, worker-packet reconciliation, prohibited-construct
scan, and whitespace checks are recorded in `intake-receipt.json` after finalization. Known
downstream failures are duplicate allocation and exact source/date review; definition-complete
statement transcription, elaboration, transports, and mutations; immutable formal candidate and
provenance audit; obligation and graph freezes; proof and composition; readable reconstruction;
hermetic replay; deterministic evidence bundling; independent validation; and master acceptance.
They prevent audit and theorem completion but do not invalidate a truthful, self-tested `planned`
intake.
