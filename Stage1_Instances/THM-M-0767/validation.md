# Intake validation

Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`.

This validation covers target membership, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. It does not elaborate or prove a canonical target.
The shared canonical `.lake` artifacts were used read-only; no update, build, clone, fetch, or
dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0767` | exit 0; rank 777, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0767/IntakeProbe.lean)` | exit 0; six pinned Cantor/cardinal API types elaborated under Lean 4.29.0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0767 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures remain intentionally open: immutable primary-source inspection and
independent review, canonical statement elaboration and mutation tests, obligation/discovery
freezes, formal-anchor and proof-body audit, proof/composition evidence, hermetic replay, and
release acceptance. They prevent theorem completion but do not invalidate a truthful `planned`
intake.

## Statement validation (2026-07-12)

Base revision: `3159849a5319960dea505779c7c20894ea30487c`.

The exact set-subtype statement, its type-level and exponential transports, and empty/finite
boundary fixtures were elaborated with the existing pinned artifacts. No `.lake` mutation command
was run. `#print axioms` reports `propext`, `Classical.choice`, and `Quot.sound` for every transport.

| Command | Result |
|---|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0767/Statement.lean)` | exit 0; exact canonical/type targets printed; five checked transports elaborate; empty and `Fin 3` fixtures elaborate; axioms exactly `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/task-dag.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/statement-freeze.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0 |
| `python3 scripts/stage1_target.py check` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0767 .stage1-worker-selftest.json` | exit 0; no output |

The statement node is self-tested but not master-accepted. Primary-source acceptance, anchor and
terminal proof-body provenance, transitive trust closure, M0, audit completion, and theorem
completion remain explicitly downstream.
