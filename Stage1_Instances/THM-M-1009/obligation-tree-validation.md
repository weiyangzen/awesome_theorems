# THM-M-1009 obligation-tree validation

Item: `S56-M-1009-OBLIGATION_TREE`

Base revision: `32a5ff1576146ad5f0f6ce7cc6ca7ca0c64a48af`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 15 obligations and 28 directed typed edges across
separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. Ten obligations are root-relevant machine obligations and
five are overlays. The denominator SHA-256 is
`24570f903e38e644cc31fc4f8725224e3551ab48325fedc9a072fdedb4c1b93d`.

The checked composition harness preserves the exact binder and hypothesis
shape while retaining the mathematical assembly as an explicit premise. The
root remains open at `M3`. Its frozen proof cut set is `M1009-L-SECOND-MOMENT`,
`M1009-L-TAIL`, `M1009-L-RATIO`, and `M1009-L-CONTINUITY`.

## Commands and results

Commands ran from the repository root unless a working directory is stated.
The existing pinned Lake closure was reused. No update, build, clone, fetch,
or dependency mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546

python3 scripts/stage1_target.py show THM-M-1009
  exit 0: rank 289; planned; legacy artifacts unaccepted; incomplete

python3 Stage1_Instances/THM-M-1009/build_obligation_artifacts.py
  exit 0: wrote 15 obligations and 28 typed edges; denominator digest
  24570f903e38e644cc31fc4f8725224e3551ab48325fedc9a072fdedb4c1b93d

python3 Stage1_Instances/THM-M-1009/check_obligation_tree.py
  exit 0: input hashes, denominator, node budgets, seven graph classes,
  reciprocal proof edges, structured recipes, and open boundary pass

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1009/ObligationTree.lean
  exit 0: zero_ratio and conditional root_compose elaborate; axioms are
  propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-1009/check_statement.py
  exit 0: exact statement digest 5933a50f...ec1f and four mutations killed

python3 -m json.tool Stage1_Instances/THM-M-1009/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1009/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-1009/validation-specs.json
  exit 0 for all three files

git diff --check -- Stage1_Instances/THM-M-1009 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The pre-existing untracked `Formalizations/Lean/.lake` path makes this
nonrelease evidence.

## Status boundary

This receipt supports only the frozen registry, typed graphs, validation
recipes, readable architecture, and conditional composition harness, pending
master acceptance. No proof obligation is closed. H0 review, readable proof
review, transitive trust, independent replay, audit completion, theorem
completion, and release remain open.
