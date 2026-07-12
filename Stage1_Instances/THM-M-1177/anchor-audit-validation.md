# Anchor-audit validation record

Base revision: `ebd311cf50e67029e9794aa8f09ab3cee28a745f`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1177/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | Seven pinned component declarations elaborated; representative axiom reports contain only standard classical/propositional/quotient choice dependencies |
| `python3 -m json.tool Stage1_Instances/THM-M-1177/anchor-audit.json >/dev/null` | 0 | Structured audit receipt is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1177` | 0 | Rank 377, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1177` | 0 | No whitespace errors |

The discovery commands and immutable external revisions are preserved in `anchor-audit.json`. This
is node-scoped audit evidence, not kernel closure of the ABP target.
