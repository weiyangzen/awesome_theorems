# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13
in the isolated worker clone.

Validation is limited to target-set consistency, dossier and source-boundary invariants, pinned
environment identity, a narrow discovery-only Lean API probe, a bounded target-name search,
proof-escape hygiene, and whitespace. The catalog record is not a proposition, so elaborating a
purported canonical target would invent missing mathematics. `IntakeProbe.lean` therefore checks
only adjacent calculus, ODE, and symplectic-matrix substrate; it introduces no theorem and supplies
no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1379` | 0 | rank 989, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 10048,10053 -- Docs/researches/math_theorems.md` | 0 | all six uncited mathematics-catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 6443,6449 -- Docs/researches/physics_theorems.md` | 0 | all seven distinct physics-record lines originate at the same corpus commit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1379/IntakeProbe.lean)` | 0 | eight adjacent pinned derivative, gradient, product projection, integral-curve, and symplectic-matrix APIs elaborated; complete output SHA-256 `4c165b56...30c097` |
| bounded case-insensitive target-name/principal-function search in pinned mathlib and repo-local Lean | 1 | expected no-match exit; no exact Hamilton-Jacobi source name located, intake discovery only and not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1379-pycache python3 -m py_compile Stage1_Instances/THM-M-1379/check_intake.py` | 0 | scoped validator compiles without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1379/check_intake.py` | 0 | target/DAG identity, immutable inputs, H5/M4/R4 planned boundary, null target, cross-target exclusions, exact artifact inventory, provisional receipt, and six open tasks agree |
| the same invariant check with `--worker-packet .stage1-worker-selftest.json` | 0 | root worker packet and owned receipt agree |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1379` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1379 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics across all changed files |

Known downstream failures remain deliberately open: an approved correction to one stable
truth-valued target; an immutable exact source proposition, definition chain, proof boundary,
errata audit, cross-target reconciliation, and independent review; exact spaces, equation,
Hamiltonian/action data, derivative and solution notions, binders, hypotheses, conclusion, and
boundary cases; canonical Lean elaboration, expression and environment fingerprints, transports,
and mutations; immutable formal-anchor audit; discovery and obligation freezes; typed graphs;
proof and composition; hermetic replay; deterministic evidence bundling; independent release
verification; and master acceptance. These block theorem execution and completion but do not
invalidate a truthful, self-tested `planned` intake.
