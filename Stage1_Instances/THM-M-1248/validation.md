# Intake validation record

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

The validation commands below are the smallest real checks appropriate to this intake-only node.
They do not elaborate or prove a Lean theorem.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Repository rev-5.6 assurance structure accepted |
| `python3 scripts/stage1_target.py check` | 0 | Ordered manifest accepted with 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1248/intake.json >/dev/null` | 0 | Structured intake parses as JSON |
| `rg -n '\b(sorry|admit|sorryAx|axiom)\b' Stage1_Instances/THM-M-1248 --glob '!validation.md'` | 1 | No forbidden Lean proof construct found; exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | No whitespace errors |

Master acceptance and every dependent statement/proof gate remain outstanding.
