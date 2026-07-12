# Intake validation

Base revision: `d0c81540f24ae847c2651a18be7e829b4b280213`.

This node introduces no Lean declaration because exact source-statement identification is still a
hard statement-phase blocker. Validation is therefore limited to real manifest/standard checks,
structured dossier checks, scoped invariants, and whitespace; no kernel result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0584` | 0 | rank 625; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0584/instance.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0584/task-dag.json >/dev/null` | 0 | structured open DAG is valid JSON |
| scoped Python intake assertions | 0 | `intake invariant check: ok`; item identity, lifecycle, open downstream states, owned files, and no accepted proof state agree |
| `git diff --check -- Stage1_Instances/THM-M-0584` | 0 | no whitespace errors |

Known downstream failures are exact primary-source pinning and review, canonical Lean elaboration,
anchor audit, obligation registry, proof, trust closure, hermetic replay, and independent release
verification. They prevent theorem completion but do not invalidate this fail-closed planned intake.
