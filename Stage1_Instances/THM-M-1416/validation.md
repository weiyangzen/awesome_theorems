# Intake validation

Base revision: `61ce73b9038706a45488f5644ad0e0f3d98937a1` (tree
`c8e94ac73b6875f43c55ae766b0c4af4abc7ba3e`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, bounded local topic searches, proof-escape hygiene,
and whitespace. The catalog object name and gloss are not a proposition, so elaborating a purported
canonical Lean target would invent missing mathematics. `IntakeProbe.lean` therefore checks only
possible substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1416` | 0 | rank 915, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1416/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1416/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1416/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after worker manifest finalization |
| `python3 Stage1_Instances/THM-M-1416/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null target, empty accepted state, exact artifact inventory, and six open tasks agree |
| `python3 -m py_compile Stage1_Instances/THM-M-1416/check_intake.py` followed by removal of generated `__pycache__` | 0 | intake validator compiles; no generated cache remains in the handoff |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1416/IntakeProbe.lean)` | 0 | six pinned measure, probability, invariant-dynamics, flow, and topological-entropy API checks elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib source tree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `sha256sum` over the root self-test and all non-receipt owned artifacts, plus captured critical command stdout | 0 | exact SHA-256 values are recorded in `intake-receipt.json`; the provisional receipt excludes itself to avoid recursive hashing and remains non-content-addressed pending integration canonicalization |
| bounded exact-topic search under pinned `Mathlib/Dynamics` and `Mathlib/MeasureTheory` | 1 | expected no-match exit; no Bowen-Margulis, maximal-entropy-measure, Patterson-Sullivan, or geodesic-flow source name found; intake discovery only |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1416` | 1 | expected no-match exit; no prohibited proof escape, bodyless declaration, or unsafe code in the API-only probe |
| scoped `git diff --check`, per-file `git diff --no-index --check`, and owned-file invariants | 0 | no whitespace diagnostics; no-index exit 1 was accepted only as the expected added-file difference |
| `git status --short` | 0 | only the automation `.lake` symlink, this owned dossier, and the root self-test manifest are untracked |

Known downstream failures remain deliberately open: an approved target correction with immutable
primary-source theorem identity and independent review; exact system, geometric and hyperbolicity
hypotheses, measure construction and normalization, conclusion, and boundary cases; canonical Lean
elaboration, fingerprints, checked transports, and mutations; immutable formal anchor audit;
discovery and obligation freezes; proof and composition; hermetic replay; deterministic evidence
bundling; independent release verification; and master acceptance. These block ordinary theorem
execution and completion but do not invalidate a truthful, self-tested `planned` intake.
