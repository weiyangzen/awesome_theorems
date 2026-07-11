# THM-M-0001 obligation-tree validation

Item: `S56-M-0001-OBLIGATION_TREE`

Base revision: `aeb963ada34ee3692d6b5eda99936690a4eda538`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 17 obligations and 43 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Fourteen obligations
are root-relevant machine obligations; three are informational overlays. The denominator SHA-256 is
`ed4e0f7d5cefc6bea4b25e384395ab05926b71951a6c2aa3828b0afaaba35773`.

The checked composition harness consumes the three exactness families and returns the exact nested
root. It does not instantiate those premises. The root remains open at `M1`; its frozen proof-phase
cut set is `M0001-L-EXACT1`, `M0001-L-EXACT2`, and `M0001-L-EXACT3`.

## Commands and results

Commands ran from the repository root unless the working directory is stated explicitly. The
canonical pre-existing `.lake` closure was reused; no update, build, clone, fetch, or dependency
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0001
  exit 0: execution rank 96; planned; legacy artifacts unaccepted;
  theorem_complete=false

python3 Stage1_Instances/THM-M-0001/build_obligation_artifacts.py
  exit 0: wrote 17 obligations and 43 typed edges; denominator digest
  ed4e0f7d5cefc6bea4b25e384395ab05926b71951a6c2aa3828b0afaaba35773

python3 Stage1_Instances/THM-M-0001/check_obligation_tree.py
  exit 0: source-input hashes, frozen denominators, required node schema,
  seven graph classes, reciprocal proof/composition edges, proof acyclicity,
  structured recipes, budgets, prohibited Lean tokens, and open-root boundary pass

python3 -m json.tool Stage1_Instances/THM-M-0001/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0001/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0001/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0001/ObligationTree.lean
  exit 0: root_compose elaborated from the three explicit family premises;
  all three upstream declaration probes passed; #print axioms reported
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0001/check_statement.py
  exit 0: statement digest
  6846afc515ceb8a7479a074f21295620ef4f191bd0804e377b56ae37567b7677;
  four mutations distinguished; pinned mathlib revision agrees

python3 Stage1_Instances/THM-M-0001/check_anchor_audit.py
  exit 0: immutable mathlib source and legacy candidate hashes agree; root=M1

git diff --check -- Stage1_Instances/THM-M-0001 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 registry, typed graphs, structured recipes, readable tree,
and conditional composition harness, pending master acceptance. No obligation is marked closed.
Proof-node acceptance, primary-source review, readable reconstruction review, transitive trust,
independent replay, `AUDIT-Z`, `THEOREM-Z`, and release remain open.
