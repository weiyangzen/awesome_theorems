# Intake validation

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. The legacy Lean file was inspected as discovery evidence, but no
canonical Lean target is accepted in this phase and no kernel closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0325` | exit 0; rank 214, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0325` | exit 0; no output |

Known downstream failures: exact primary-source inspection, normalization choice, canonical Lean
elaboration and mutation tests, anchor audit, obligation registry, proof, hermetic replay, and
independent review remain open. They prevent theorem completion but do not invalidate a fail-closed
planned intake.

## Statement-phase validation

Base revision: `28e77827f1df290b07af3449223a8bb3f3a56bfd`.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0325/Statement.lean` | exit 0; exact target, expanded-shape transport, four mutations, and empty-index boundary elaborated; printed canonical target |
| `python3 Stage1_Instances/THM-M-0325/check_statement.py` | exit 0; expression SHA-256 `b4daa662b6b3f7cc1578975aeaf9fd097ef586b209bd0d26d4262c59ac59cf82`; all four mutations distinguished; pinned mathlib revision confirmed |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/statement.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `git diff --check -- Stage1_Instances/THM-M-0325` | exit 0; no output |

The direct import is `Mathlib.Analysis.InnerProductSpace.Basic`; no dependency or `.lake` mutation
command was run. Statement acceptance does not establish H0 source fidelity, a proof, anchor audit,
or theorem completion. Those remain downstream gates.
