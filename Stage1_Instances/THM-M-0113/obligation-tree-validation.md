# THM-M-0113 obligation-tree validation

Item: `S56-M-0113-OBLIGATION_TREE`

Validation date: `2026-07-12` (Asia/Shanghai)

Base revision: `cf2b907b1d10a3b5c923fc84e10b495a48530690`

## Frozen result

Registry version 1 freezes 26 obligations and 49 edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs.
All obligations remain M4 and eligible for machine, human-source, and readable
coverage. The canonical denominator projection digest is
`e509c1920e23d809083d43f1c19996cd20a97c5931144d4cb266eca39484cbd5`.

## Commands and results

All commands ran at the repository root unless the command explicitly changes
directory. Existing pinned `.lake` artifacts were reused; no update, build,
clone, fetch, or other dependency mutation was performed.

```text
python3 Stage1_Instances/THM-M-0113/build_obligation_artifacts.py
  exit 0: wrote 26 obligations and 49 typed edges; emitted denominator digest

python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py
  exit 0: schemas, canonical denominator, seven graph classes, reciprocal edge
  indices, acyclicity, complete root reachability, ledgers, cut set, and open
  M4 boundary passed

python3 -m json.tool Stage1_Instances/THM-M-0113/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0113/typed-graphs.json
  exit 0 for both files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0113/ObligationTree.lean
  exit 0: conclusion_compose and conjugation_membership_iff elaborated;
  #print axioms reported that neither declaration depends on any axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets passed

python3 scripts/stage1_target.py show THM-M-0113
  exit 0: rank 25, planned, legacy artifacts unaccepted, theorem incomplete

git diff --check -- Stage1_Instances/THM-M-0113 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Status boundary

This evidence self-tests only the obligation registry, typed graphs, and two
conditional composition steps. No analytic theorem premise, terminal proof
body, or obligation is closed. Primary-source acceptance, readable review,
transitive trust, independent validation, `AUDIT-Z`, `THEOREM-Z`, theorem
completion, release, and master acceptance remain open. The pre-existing
untracked `Formalizations/Lean/.lake` worker artifact makes this nonrelease
evidence.
