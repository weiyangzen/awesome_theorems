# Statement validation

Base revision: `e7eee8ac07da60bac144a377a6a5c3fabd7659e4`.

The preflight worktree contained the automation-provided untracked symlink
`Formalizations/Lean/.lake` to the canonical pinned artifacts; it was not modified. Validation is
limited to manifest consistency, exact statement elaboration, checked direct transport, one positive
boundary fixture, three negative mutation fixtures, JSON structure, hygiene, and whitespace.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0540` | exit 0; rank 597, L0/rework_required, planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/Statement.lean)` | exit 0; canonical target, direct-expression `iff`, and `Empty`/degree-zero boundary fixture elaborated |
| the same narrow command on `MutationRemovedDegree.lean` | exit 1 as expected; unknown identifier `n` |
| the same narrow command on `MutationChangedDomain.lean` | exit 1 as expected; `Nat` rejected as the space domain passed to `TopCat.of` |
| the same narrow command on `MutationBinderScope.lean` | exit 1 as expected; `X` is out of scope and the topology instance cannot synthesize |
| the same narrow command on `MutationNegativeDegree.lean` | exit 1 as expected; `Int` degree rejected by the `Nat`-graded API |
| `python3 -m json.tool Stage1_Instances/THM-M-0540/statement.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0540/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0540/task-dag.json` | exit 0 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/IntakeProbe.lean)` | exit 0; all three pinned mathlib declarations elaborated with their full types |
| `rg -n '\b(sorry\|admit\|axiom)\b' Stage1_Instances/THM-M-0540 --glob '*.lean'` with failure on a match | exit 0; no forbidden Lean token found |
| `git diff --check -- Stage1_Instances/THM-M-0540` | exit 0; no output |

## Status boundary

Known downstream failures are pinpoint source and errata review, the anchor/provenance audit,
obligation registry, terminal-body audit, proof-phase credit, hermetic replay, and independent
review. They prevent audit and theorem completion but do not invalidate the self-tested statement
handoff. The exact target intentionally excludes higher-universe spaces; broadening it requires a
new statement receipt rather than silent universe polymorphism.
