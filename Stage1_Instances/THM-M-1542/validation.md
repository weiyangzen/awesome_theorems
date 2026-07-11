# Intake validation record

- Base revision: `61369637c5db864082a624c34c62a91e6741f9da`
- Scope: `S56-M-1542-INTAKE` only
- Result date: 2026-07-12 (Asia/Shanghai)

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest valid: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1542` | 0 | Rank 183, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1542/intake.json` | 0 | Structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|theorem_complete.: true' Stage1_Instances/THM-M-1542` | 0 | Only the ordinary audit word `axiom` in the open-task description matched; no Lean code, placeholder proof, or completion claim exists |
| `git diff --check -- Stage1_Instances/THM-M-1542` | 0 | No whitespace errors |

No Lean compilation was run because intake intentionally contains no Lean target or proof. The
narrow validation demonstrates dossier structure and target membership, not mathematical or kernel
closure. Source URLs are discovery anchors; their texts, hashes, assumptions, and errata remain an
explicit dependent-phase gate.
