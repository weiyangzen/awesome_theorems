# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`).

Validation is deliberately limited to target membership, repository-standard consistency, dossier
structure, JSON syntax, planned-state invariants, source-record provenance, pinned toolchain and
dependency identities, a bounded exact-topic name search, adjacent ODE API elaboration, proof-hole
hygiene, and whitespace. The repository record does not determine a proposition, so elaborating a
remembered RK4, order, error, convergence, or stability theorem would be substitution rather than
validation. `IntakeProbe.lean` therefore checks only generic ODE APIs and introduces no theorem.

The automation-provided `Formalizations/Lean/.lake` symlink exposes the canonical pinned artifacts.
It was present before this work and was used read-only. No update, build, dependency clone, fetch,
or `.lake` mutation was run.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1396` | 0 | rank 1006, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` | 0 | initial tree contained only the pre-existing `.lake` symlink; final tree contains it and this owned intake packet |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision/tree above |
| `git blame -L 10167,10172 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa...` |
| Crossref query and GDZ issue-scan retrieval recorded in `intake-receipt.json` | 0 | Runge 1895 bibliography/issue metadata inspected; no exact proposition or proof passage credited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake 5.0.0; no update/build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib `8a178386...`, tree `bdc39a31...` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1396/IntakeProbe.lean)` | 0 | eight adjacent ODE, Picard, existence, Gronwall, and approximate-trajectory APIs elaborated; no target theorem stated |
| bounded `rg` search for Runge-Kutta/Kutta/RK/numerical-ODE-integrator Lean names | 1 (expected) | no match; discovery only, not a complete anchor audit or global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1396-pycache python3 -m py_compile Stage1_Instances/THM-M-1396/check_intake.py` | 0 | validator compiles without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-1396/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H5/M4/R4 boundary, null target, exact inventory, packet agreement, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-1396/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| scoped forbidden-declaration `rg` scan | 1 (expected) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` aggregate | 0 | no whitespace diagnostics; exit 1 for each file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1396 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1396-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay,
deterministic release bundle, and independent verification remain open. These failures prevent
statement, audit-completion, and theorem-completion claims, but they do not invalidate the planned
intake.
