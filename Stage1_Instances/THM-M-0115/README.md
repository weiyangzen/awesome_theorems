# THM-M-0115: Grothendieck-Riemann-Roch

Lifecycle: `planned`. Baseline: `L0 / rework_required`.

This dossier freezes the intake scope for the classical nonsingular quasi-projective variety form
of Grothendieck-Riemann-Roch. [scope-map.md](scope-map.md) records the mathematical boundary and
[source-statement-crosswalk.md](source-statement-crosswalk.md) records the provisional primary-source
mapping. `instance.json` is scope authority and `task-dag.json` is workflow authority.

Current debt is `H4 / M5 / R4`. No Lean expression has yet been elaborated, no obligation registry
has been frozen, and no proof or accepted receipt exists. Consequently both audit completion and
theorem completion are false.

## Intake Validation

Run from repository root:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0115
python3 -m json.tool Stage1_Instances/THM-M-0115/instance.json
python3 -m json.tool Stage1_Instances/THM-M-0115/task-dag.json
git diff --check -- Stage1_Instances/THM-M-0115
```

These checks validate target membership and artifact syntax only. They do not validate the source
pinpoints, the eventual Lean statement, or theorem truth/closure.
