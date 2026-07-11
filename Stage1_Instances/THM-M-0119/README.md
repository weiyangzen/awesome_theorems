# THM-M-0119: Kawamata-Viehweg Vanishing Theorem

Lifecycle: `planned`. Baseline: `L0 / rework_required`.

This dossier freezes the intake scope as the projective klt-pair form of Kawamata-Viehweg
vanishing. [scope-map.md](scope-map.md) fixes the mathematical boundary and
[source-statement-crosswalk.md](source-statement-crosswalk.md) maps that boundary to provisional
primary sources. `instance.json` is the structured intake authority and `task-dag.json` is the open
workflow authority.

Current provisional debt is `H4 / M3 / R4`. The exact local statement interface now elaborates as
`Stage1Instances.THMM0119.KawamataViehwegVanishingTarget`; see `Statement.lean` and
`statement.json`. The pinned library lacks native interfaces covering several required
algebro-geometric notions, so the module exposes typed objects and named compatibility predicates
without assuming the conclusion. The source pinpoints remain independently unreviewed, and no
proof evidence or accepted receipt exists. Audit and theorem completion are both false.

## Intake Validation

Run from the repository root:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0119
python3 -m json.tool Stage1_Instances/THM-M-0119/instance.json
python3 -m json.tool Stage1_Instances/THM-M-0119/task-dag.json
git diff --check -- Stage1_Instances/THM-M-0119
```

These checks establish manifest membership, JSON syntax, and clean patch formatting only. They do
not establish source fidelity, Lean elaboration, or proof closure.
