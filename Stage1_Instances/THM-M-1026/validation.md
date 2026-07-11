# Intake validation

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

All commands below exited 0 on 2026-07-12:

```text
python3 -m json.tool Stage1_Instances/THM-M-1026/intake.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1026/task-dag.json >/dev/null
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1026
! rg -n '\b(sorry|axiom)\b|placeholder|fake result' Stage1_Instances/THM-M-1026 --glob '!validation.md'
git diff --check -- Stage1_Instances/THM-M-1026
```

The standard checker reported 15 assurance groups and 1546 uniform-L0 targets; the target checker
reported 1546 unique ranks; `show` confirmed rank 502, `planned`, L0/rework-required, and theorem
incomplete. Both JSON documents parsed, the prohibited-term scan had no matches, and the diff check
was clean. No Lean command is applicable to this intake because it intentionally creates no Lean
declaration; exact elaboration is the dependent statement phase.

Known failures: exact source variant and pinpoint, canonical Lean expression, environment
fingerprint, source/anchor audit, proof, and every later theorem-completion gate remain open.
