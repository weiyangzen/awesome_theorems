# Intake validation

Item: `S56-M-0772-INTAKE`  
Theorem: `THM-M-0772`  
Base revision: `31e30357eb3a9bb108b17fbc50c003c84a21b3e6`  
Validation date: 2026-07-12 (Asia/Shanghai)

Validation covers target-set consistency, dossier structure, JSON syntax, scoped intake invariants,
and elaboration of a discovery probe against the already materialized pinned Lake artifacts. No
`lake update`, build, clone, fetch, or other `.lake` mutation was run. The probe does not define the
canonical target or establish proof credit.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0772` | 0 | Rank 580, planned, statement-first lane, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0772/IntakeProbe.lean` | 0 | Pinned import elaborated; Lean printed `IsChain`, `IsMaxChain`, `maxChain`, and `maxChain_spec`, with `maxChain_spec : IsMaxChain r (maxChain r)` |
| `python3 -m json.tool Stage1_Instances/THM-M-0772/instance.json` | 0 | Structured intake parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0772/task-dag.json` | 0 | Open task DAG parsed |
| scoped Python intake assertions | 0 | Reported `intake invariant check: ok`; identity, lifecycle, baseline, root vector, empty accepted states, artifact inventory, and six open downstream tasks agree |
| `git diff --check -- Stage1_Instances/THM-M-0772 .stage1-worker-selftest.json` | 0 | No whitespace errors |

Known downstream failures are exact primary-source locator/edition inspection and independent review,
canonical target elaboration and mutation tests, full anchor audit, obligation registry, proof and
composition checks, hermetic replay, and independent release validation. They prevent theorem
completion but do not invalidate a truthful `planned` intake.

The worktree contains the automation-provided untracked `Formalizations/Lean/.lake` link. It was not
created or modified for this item, and this validation is nonrelease evidence.
