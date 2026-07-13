# Intake validation

Base revision: `ee8c1843ef3ce74178a990f4e64554c1558c51fa` (tree
`3a34df1cc2089854dc563ab4909cc0586713ad20`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
record provenance, pinned environment identity, a narrow Lean API probe, bounded local searches,
proof-escape hygiene, JSON integrity, and whitespace. The source record is not a proposition, so
elaborating a purported canonical Lean target would invent missing mathematics. `IntakeProbe.lean`
therefore checks only possible substrate; it introduces no theorem and supplies no statement or
proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1441` | 0 | rank 1120, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `git blame -L 10525,10530 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Asymptotics/Defs.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/Real/GoldenRatio.lean` | 0 | immutable input hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1441/IntakeProbe.lean)` | 0 | eight pinned asymptotic, convergence, division, iteration, and golden-ratio APIs elaborated; complete output SHA-256 `3277bc3a41b43734b1488b0691c26fcdf838218b00470ef5bdfc7b1e6523ad3c` |
| `rg -n -i --glob '*.lean' 'secant method\|secant iteration\|secant_method\|secantMethod\|chord method\|regula falsi\|secant.*converg\|converg.*secant' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems Stage1_Instances` | 1 | expected no-match within these bounded roots; no numerical secant-method declaration was located, while the downstream formal-candidate audit remains open |
| `python3 -m json.tool Stage1_Instances/THM-M-1441/instance.json`, repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1441-pycache python3 -m py_compile Stage1_Instances/THM-M-1441/check_intake.py` | 0 | scoped intake validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1441/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, hashes, handoff, and six open tasks agree |
| `rg -n -i --glob '*.lean' 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe' Stage1_Instances/THM-M-1441` | 1 | expected no-match; no prohibited proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1441 .stage1-worker-selftest.json`, then `git diff --no-index --check /dev/null <file>` for every untracked changed file | 0 | no whitespace diagnostics; expected no-index difference statuses contained no diagnostics |

## Known downstream failures

- The catalog method/rate gloss does not select one stable truth-valued proposition or primary
  source. An approved correction and independent review are open.
- The function and domain, root, recurrence, two starts, denominator safety, regularity, local
  basin, convergence mode, superlinear-rate definition, conclusion, and boundary cases are open.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, source and formal-candidate audits, obligation registry and typed graphs,
  proof, composition and trust checks, readable reconstruction, hermetic replay, deterministic
  evidence bundle, independent release verification, and master acceptance remain open.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose deliverable is to preserve the ambiguity, scope boundary,
crosswalk, and open DAG. Only the integration lane may accept the provisional worker receipt.
The displayed `[H5, M4, R4]` vector is a nonaccepted catalog-target assessment, not the status of a
canonical proof root; no such root exists until the statement gate is resolved.
