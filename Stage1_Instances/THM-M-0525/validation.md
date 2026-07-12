# Intake validation record

Base revision: `31e30357eb3a9bb108b17fbc50c003c84a21b3e6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0525` | 0 | rank 582, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0525/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0525/task-dag.json >/dev/null` | 0 | open dependent task DAG is valid JSON |
| scoped Python intake assertions | 0 | `intake invariant check: ok`; identity, rank, planned state, open formal gate, root boundary, required files, and six open dependent tasks agree |
| `rg -n 'sorry\|admit\|sorryAx\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0525/IntakeProbe.lean` | 1 | no forbidden Lean proof-escape matches; exit 1 is ripgrep's no-match result |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0525/IntakeProbe.lean)` | 0 | pinned Lean elaborated candidate APIs; printed `FundamentalGroup`, the path-homotopy quotient, composition/identity anchors, the path-induced basepoint equivalence, and synthesized `instGroupFundamentalGroup X x`; the definitional carrier example checked |
| `git diff --check -- Stage1_Instances/THM-M-0525 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The worker clone's `Formalizations/Lean/.lake` is the scheduler-provided symlink to canonical pinned
artifacts and was not modified, updated, built, fetched, or cloned. The Lean command is a narrow
elaboration probe, not an exact-statement or proof receipt.

Known failures and open gates: master acceptance; exact formal-target selection, normalized
expression and environment fingerprints, mutation tests, primary-source edition/page/assumption and
errata audit, full Lean anchor/provenance/trust audit, obligation registry, proof composition,
hermetic validation, readability review, and release evidence. Consequently audit completion and
theorem completion remain false.
