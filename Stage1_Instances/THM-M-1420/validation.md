# Intake validation

Base revision: `508f92b22d15ce42276877b26d34b9da3cac695c` (tree
`765daac67cdaffd2b797474b4c1a3d12f4f99933`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, bounded local name searches, proof-escape hygiene,
and whitespace. The source record is not a proposition, so elaborating a purported canonical Lean
target would invent missing mathematics. `IntakeProbe.lean` therefore checks only possible
substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1420` | 0 | rank 918, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, the finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `python3 Stage1_Instances/THM-M-1420/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null formal target, exact artifact inventory, and six open tasks agree |
| `python3 -m py_compile Stage1_Instances/THM-M-1420/check_intake.py` | 0 | intake validator compiles |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1420/IntakeProbe.lean)` | 0 | eight adjacent pinned measure-preserving, ergodic, manifold-derivative, and tangent-bundle APIs elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| bounded `Pesin` and `nonuniform[ -]hyperbol` search under pinned mathlib | 1 | expected no-match exit; intake discovery only, not an anchor audit |
| bounded `Lyapunov`, `Oseledets`, and `stable[ -]manifold` search under pinned mathlib | 1 | expected no-match exit; no nearby named formal candidate located in the bounded search |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1420 .stage1-worker-selftest.json` plus per-new-file `git diff --no-index --check` | 0 | no whitespace diagnostics; the invariant checker independently checks all untracked owned files |

Known downstream failures remain deliberately open: an approved target correction with an
immutable exact primary-source theorem and independent review; exact binders, hypotheses,
conclusion, and boundary cases; canonical Lean elaboration, expression and environment
fingerprints, checked transports, and mutations; immutable formal-anchor audit; discovery and
obligation freezes; proof and composition; hermetic replay; deterministic evidence bundling;
independent release verification; and master acceptance. These block ordinary theorem execution
and completion but do not invalidate a truthful, self-tested `planned` intake.
