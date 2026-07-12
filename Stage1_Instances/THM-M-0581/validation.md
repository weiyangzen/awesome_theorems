# Intake validation

Base revision: `d0c81540f24ae847c2651a18be7e829b4b280213`.

Validation is limited to manifest consistency, the planned dossier's structure and invariants, and
the smallest available Lean environment probe. No canonical Lean expression or proof is introduced
by this phase, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0581` | exit 0; rank 623, planned, L0/rework-required, theorem incomplete |
| `lake env lean Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_128.lean` | exit 1; `no default toolchain configured`; no dependency fetch or `.lake` mutation attempted |
| `python3 -m json.tool Stage1_Instances/THM-M-0581/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0581/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0581` | exit 0; no output |

Known downstream failures are the missing configured Lean toolchain, pinpoint source and errata
audit, canonical statement elaboration, anchor audit, obligation registry, proof, hermetic replay,
and independent review. The toolchain failure prevents any Lean evidence but does not invalidate a
fail-closed documentation-and-structure intake; it must be resolved before the statement gate.
