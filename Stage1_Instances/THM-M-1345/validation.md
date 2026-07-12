# Intake validation

Base revision: `3ed74ce8b03564707b34b6e2314d2bb6d0a6206e` (tree
`5d5275ace8e7c0d1026c248e8f2760e18c3c8dda`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation covers target membership, dossier and open-DAG invariants, repository/source identity,
JSON integrity, bounded formal discovery, and a narrow pinned Lean API probe. The primary Hartman
paper, a modern source candidate, and the modern source's official errata were actually inspected;
they remain candidate evidence rather than an accepted source-to-statement mapping.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1345` | 0 | rank 956, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided `.lake` link, preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| source retrieval and inspection for Hartman 1960, DOI `10.1090/S0002-9939-1960-0121542-7` | 0 | publisher PDF, Theorem (II) on page 615 and proof pages 615-618 inspected; SHA-256 `f633e1c7...997f9`; candidate only |
| source retrieval and inspection for Teschl 2012, DOI `10.1090/gsm/140` | 0 | author-hosted preliminary PDF, Theorem 9.9/page 264 and proof inspected; SHA-256 `36243315...36e`; candidate only |
| retrieval and inspection of Teschl's official `errata.pdf` | 0 | SHA-256 `3eacbac5...996e`; proof-relevant page 265, 266, and 268 corrections recorded, not yet accepted node-by-node |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no build or update run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1345/IntakeProbe.lean)` | 0 | thirteen adjacent ODE, flow, fixed-point, derivative, local-homeomorphism, and conjugacy interfaces elaborated; no target theorem declared |
| bounded exact-topic search over repo-local Lean and pinned mathlib | 1 for theorem-specific ODE/dynamics query | no Hartman-Grobman or hyperbolic-equilibrium topological-conjugacy result found; unrelated topological conjugation text excluded; intake discovery only |

The final owned JSON, scoped checker, worker-packet reconciliation, prohibited-construct scan, and
whitespace checks are recorded in `intake-receipt.json` after finalization. Known downstream
failures are source-variant selection and independent review; binder-complete statement
transcription, elaboration, transports, and mutations; immutable formal anchor/provenance audit;
obligation and graph freezes; proof and composition; readable reconstruction; hermetic replay;
deterministic evidence bundling; independent validation; and master acceptance. They prevent audit
and theorem completion but do not invalidate a truthful, self-tested `planned` intake.
