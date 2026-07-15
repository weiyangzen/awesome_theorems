# THM-M-0115: Grothendieck-Riemann-Roch

Lifecycle: `planned`. Baseline: `L0 / rework_required`.

This dossier freezes the intake scope for the classical nonsingular quasi-projective variety form
of Grothendieck-Riemann-Roch. [scope-map.md](scope-map.md) records the mathematical boundary and
[source-statement-crosswalk.md](source-statement-crosswalk.md) records the provisional primary-source
mapping. `instance.json` is scope authority and `task-dag.json` is workflow authority.

The statement worker has now elaborated the exact selected target as
`Stage1Instances.THMM0115.GrothendieckRiemannRochExpandedTarget` in
[Statement.lean](Statement.lean), with two direct pinned imports, a checked definitional alias,
four structural mutation kills, expression/environment fingerprints, and a provisional worker
receipt. Missing native `K_0`, rational Chow, characteristic-class, tangent, and cap APIs are
represented by conclusion-free typed interfaces with explicit semantic compatibility hypotheses;
no field assumes the GRR identity.

The proposed debt is `H4 / M3 / R4`. This is statement/interface evidence only. The intake and
statement still await dependency-ordered master acceptance; the source convention mismatch,
obligation registry, proof, validation, readability, and release gates remain open. Consequently
both audit completion and theorem completion are false and no accepted receipt exists.

## Statement Validation

Run from repository root:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0115
cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0115/Statement.lean
cd ../.. && LC_ALL=C TZ=UTC python3 Stage1_Instances/THM-M-0115/check_statement.py
python3 -m json.tool Stage1_Instances/THM-M-0115/instance.json
python3 -m json.tool Stage1_Instances/THM-M-0115/task-dag.json
python3 -m json.tool Stage1_Instances/THM-M-0115/statement.json
python3 -m json.tool Stage1_Instances/THM-M-0115/statement-receipt.json
git diff --check -- Stage1_Instances/THM-M-0115
```

The narrow Lean and checker commands validate statement elaboration, fingerprints, import pins,
transport, and mutation distinctions. They do not validate source pinpoints or theorem truth and
closure.
