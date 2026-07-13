# THM-M-0483 intake validation

Base revision: `2226f559136f12fde46b1bf73cdf629043b8a648` (tree
`33cb254ed06b1391379b8e7f88c5e23188957b62`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, planned-dossier and source-boundary invariants,
pinned environment identity, a narrow discovery-only Lean API probe, bounded repository searches,
artifact syntax and hygiene, and whitespace. The catalog family does not determine a unique
proposition, so the canonical target, fingerprints, obligations, and proof state stay open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0483` | 0 | rank 1364, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` link |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 3546,3551 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0483/IntakeProbe.lean)` | 0 | six nearby Mersenne/Lucas-Lehmer signatures elaborated; three axiom reports each show `propext`, `Classical.choice`, and `Quot.sound`; complete output SHA-256 `4249ced0...36f770` |
| bounded case-insensitive Mersenne/Lucas search in repo-local Lean and pinned mathlib | 0 | located exact-topic mathlib module, exponent-127 archive example, and other-target discovery references; not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0483-pycache python3 -m py_compile Stage1_Instances/THM-M-0483/check_intake.py` | 0 | scoped validator compiles without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0483/check_intake.py` | 0 | target/DAG identity, source pins, H1/M3/R4 planned boundary, null target, cross-target exclusion, exact artifact inventory, provisional receipt, and six open downstream tasks agree |
| the same invariant check with `--worker-packet .stage1-worker-selftest.json` | 0 | root worker packet and owned receipt agree |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0483` Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0483 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics across all changed files |

The first failed downstream gate is an immutable exact source proposition with incorporated
definitions, premise/conclusion mapping, corrections audit, independent review, and a reviewed
allocation against `THM-M-0484`. Exact Lean elaboration and fingerprints, mutations, complete
anchor audit, discovery and obligation freezes, typed graphs, proof and composition, provenance and
trust closure, readable reconstruction, hermetic replay, deterministic evidence bundling,
independent release verification, and master acceptance all remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose job is to preserve ambiguity and open
work. Only the integration lane may accept the provisional receipt.
