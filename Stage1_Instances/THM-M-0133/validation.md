# Intake Validation Record

Run from repository root on 2026-07-12 (Asia/Shanghai), base revision
`a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0133` | 0 | rank 22, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0133/instance.json` | 0 | valid JSON |
| `python3 -c 'import json; p="Stage1_Instances/THM-M-0133/instance.json"; d=json.load(open(p)); assert d["theorem_id"]=="THM-M-0133" and d["item_id"]=="S56-M-0133-INTAKE" and d["lifecycle"]=="planned" and d["proof_state"]=="no accepted proof state" and not d["audit_complete"] and not d["theorem_complete"]'` | 0 | intake invariants hold |
| `rg -n '\\b(sorry|admit|axiom)\\b|placeholder|fake results' Stage1_Instances/THM-M-0133/instance.json Stage1_Instances/THM-M-0133/README.md` | 1 | no forbidden token found (expected no-match exit) |
| `git diff --check -- Stage1_Instances/THM-M-0133` | 0 | no whitespace errors |

No Lean theorem is claimed or introduced by this intake, so a Lean build is not evidence for this
phase. Exact elaboration is deliberately assigned to `S56-M-0133-STATEMENT`.
