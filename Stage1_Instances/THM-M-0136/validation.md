# Intake validation

This phase validates only manifest membership, structural consistency, JSON syntax, owned dossier invariants, and whitespace. No Lean target is frozen, so no kernel validation is claimed.

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

Exact commands and results are recorded after execution.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard reports 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0136` | exit 0; rank 52, L0/rework required, planned, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0136/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0136/task-dag.json` | exit 0 |
| scoped Python assertions over both JSON documents and the owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0136` | exit 0; no output |

Known open gates: exact primary-source theorem coordinates are missing; the provisional claim is not elaborated; no proof, kernel closure, independent review, or release evidence exists. These are intentionally open downstream gates, not intake proof claims.
