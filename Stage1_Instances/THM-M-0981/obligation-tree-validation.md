# THM-M-0981 obligation-tree validation

Item: `S56-M-0981-OBLIGATION_TREE`

Base revision: `acfb5cdfcf75eadcf18e7f322e4fc4097c3e0077`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 14 obligations and 29 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Eleven obligations
are root-relevant machine obligations; the other three are provenance, source, and TCB overlays.
The frozen denominator SHA-256 is
`0ccf79f681bab58d0df655155ef09418fb916f781f1fa354260fb97fd4676a33`.

The Lean harness consumes universal empty-event, unit-mass, and countable-additivity packages and
returns the exact expanded canonical target. It does not instantiate those premises. No obligation
is accepted closed; the root remains `M1` with cut set `M0981-L-EMPTY`, `M0981-L-UNIT`, and
`M0981-L-ADDITIVITY`.

## Commands and results

Commands ran from the repository root unless a working directory is shown. The existing pinned
`.lake` artifacts were reused; no update, build, clone, fetch, or dependency mutation was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0981
  exit 0: rank 261; planned; legacy artifacts unaccepted; theorem_complete=false

python3 Stage1_Instances/THM-M-0981/build_obligation_artifacts.py
  exit 0: wrote 14 obligations and 29 typed edges; denominator digest
  0ccf79f681bab58d0df655155ef09418fb916f781f1fa354260fb97fd4676a33

python3 Stage1_Instances/THM-M-0981/check_obligation_tree.py
  exit 0: input hashes, frozen denominators, node schema, seven graph classes,
  reciprocal proof/composition edges, proof acyclicity, structured recipes,
  budgets, prohibited Lean tokens, and open-root boundary passed

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0981/ObligationTree.lean
  exit 0: conditional root composition elaborated; all three pinned declaration
  probes passed; #print axioms reported [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0981/check_statement.py
  exit 0: canonical expression SHA-256
  1170cf6dac37cd1a8b7dfbda1a3cc3d22ddb94a5c3846f16d90dd27541766c2a;
  four mutations distinguished; pinned mathlib revision agreed

python3 -m json.tool Stage1_Instances/THM-M-0981/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0981/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0981/validation-specs.json
  exit 0 for all three files: valid JSON

git diff --check -- Stage1_Instances/THM-M-0981 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This self-test supports only the frozen registry, typed graphs, structured recipes, readable tree,
and conditional composition harness pending master acceptance. Proof-node acceptance, primary-source
review, readable reconstruction review, transitive trust, independent replay, `AUDIT-Z`,
`THEOREM-Z`, and release remain open.
