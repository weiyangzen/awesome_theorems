# Intake validation

Base revision: `ffe94ac84965dc19f4923f88b7566072ddee37ae` (tree
`876a17f277d84dcf06ca672e5cd351edaa294495`). Validation ran on 2026-07-12 in
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
| `python3 scripts/stage1_target.py show THM-M-1428` | 0 | rank 926, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 10432,10437 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, the finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `python3 Stage1_Instances/THM-M-1428/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null target, exact artifact inventory, and six open tasks agree |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1428-pycache python3 -m py_compile Stage1_Instances/THM-M-1428/check_intake.py` | 0 | intake validator compiles without adding generated files to the owned path |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| first two `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1428/IntakeProbe.lean)` attempts | 1 | probe-only identifiers `Complex`, `Function.iterate`, and then `Complex.abs` were invalid; corrected to `ℂ`, `norm`, and a named iterate lemma; no target declaration or proof was involved |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1428/IntakeProbe.lean)` | 0 | eleven adjacent pinned complex, analytic, iterate, periodic-point, closure, and frontier API checks elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; package was used read-only |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| bounded whole-word Julia/Mandelbrot/complex-dynamics source-name search under pinned mathlib | 1 | expected no-match exit; intake discovery only, not an anchor audit |
| bounded paired whole-word Julia/Fatou/Mandelbrot search under pinned mathlib | 0 | only unrelated Fatou-lemma documentation matched; no complex-dynamics target was identified |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1428 .stage1-worker-selftest.json` plus per-new-file checks and owned-file invariants | 0 | no whitespace diagnostics, including all untracked owned artifacts |

Known downstream failures remain deliberately open: an approved target correction with an
immutable exact primary-source proposition and independent review; exact map, ambient model,
Julia-set and repelling/normality definitions, binders, hypotheses, conclusion, and boundary cases;
canonical Lean elaboration, expression and environment fingerprints, checked transports, and
mutations; immutable formal-anchor audit; discovery and obligation freezes; proof and composition;
hermetic replay; deterministic evidence bundling; independent release verification; and master
acceptance. These block ordinary theorem execution and completion but do not invalidate a truthful,
self-tested `planned` intake.
