# Intake validation record

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

All commands below exited 0 on 2026-07-12:

```text
python3 -m json.tool Stage1_Instances/THM-M-1025/intake.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1025/task-dag.json >/dev/null
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1025
! rg -n '\b(sorry|axiom)\b|placeholder|fake result' Stage1_Instances/THM-M-1025 --glob '!validation.md'
rg -n 'source_statement_crosswalk.md|task-dag.json|S56-M-1025-(INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE)' Stage1_Instances/THM-M-1025 >/dev/null
git diff --check -- Stage1_Instances/THM-M-1025 .stage1-worker-selftest.json
```

The standard checker reported 15 assurance groups and 1546 uniform-L0 targets. The target checker
reported 1546 unique ranks, and `show` confirmed rank 501, `planned`, L0/rework-required, and theorem
incomplete. Both JSON documents parsed, all task and local document references were found, the
prohibited-content scan had no matches, and the scoped diff check was clean.

This is the smallest real validation for an intake node. No Lean command applies because no Lean
declaration is introduced before the dependent statement phase. Known open gates are exact source
selection and pinpointing, canonical Lean elaboration and environment fingerprint, source and
formal-anchor audits, obligation freezing, proof, release validation, and master acceptance.
