# Intake validation

Base revision: `f608e06dccf2e158f1d2feeadb48f1b64d296cdd` (tree
`c0e4ab057a962cd2020342a692d39952f65d8bec`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation covers target membership, the planned dossier and open task DAG, catalog provenance,
JSON integrity, a bounded local formal search, and a narrow pinned Lean API probe. Crossref metadata
for Artin and Schreier's 1927 paper and two Encyclopedia of Mathematics revisions were inspected.
No exact primary-source theorem passage or independently reviewed definition and assumption chain
was admitted, so the source work remains H1 rather than H0.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0018` | 0 | rank 1067, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short` before edits | 0 | only the automation-provided `.lake` link was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 149,154 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1007/BF02952512` | 0 | Artin and Schreier, *Algebraische Konstruktion reeller Korper*, Hamburg 5(1), 1927, pages 85-99; 4,032-byte response SHA-256 `17f124e2...1c6`; metadata only |
| inspection of Encyclopedia of Mathematics `Real closed field`, `oldid=48449` | 0 | secondary entry distinguishes the finite nontrivial algebraic-closure characterization from real-closure existence and uniqueness |
| inspection of Encyclopedia of Mathematics `Artin-Schreier theorem`, `oldid=54480` | 0 | secondary entry records the characteristic-p namesake and alternate formal-reality/orderability usage |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0018/IntakeProbe.lean)` | 0 | twelve adjacent real-closed, semireal, ordering, algebraic-closure, algebraicity, and finite-rank interfaces elaborated; no target theorem declared |
| bounded `ArtinSchreier` and real-closed-equivalence search over repo-local Lean and pinned mathlib | expected no exact-topic match | pinned mathlib exposes adjacent APIs and a TODO for equivalent conditions; the similarly numbered legacy file belongs to `THM-M-0405`; intake discovery only, not a complete anchor audit |

The final JSON checks, scoped checker in public and worker-packet modes, prohibited-construct scan,
and untracked-file whitespace checks are recorded in `intake-receipt.json` after finalization. Known
downstream failures are exact primary-source statement selection and independent review; canonical
Lean elaboration, transports, and mutations; immutable formal anchor/provenance audit; obligation
and graph freezes; proof and composition; readable reconstruction; hermetic replay; deterministic
evidence bundling; independent validation; and master acceptance. They prevent audit and theorem
completion but do not invalidate a truthful, self-tested `planned` intake.
