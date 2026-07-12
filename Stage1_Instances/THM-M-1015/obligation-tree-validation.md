# THM-M-1015 obligation-tree validation

Item: `S56-M-1015-OBLIGATION_TREE`

Base revision: `e4f68760f8779f934ed18b07dad15e4512436d06`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 17 obligations and 38 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Fourteen obligations
are root-relevant machine obligations; three are informational overlays. The frozen denominator
SHA-256 is `fb5265f3a59199de30de2aab36aa8b0371b08d24cb0b010aaf919d08b59a6a53`.

The checked composition harness consumes pair, addition, multiplication, and conditional quotient
premises and yields the exact root package. It does not instantiate the premises. The root remains
open at `M1`; the quotient-local package remains `M3`.

## Commands and results

Commands ran from the repository root unless a working directory is stated. The pre-existing
pinned `.lake` closure was reused. No update, build, clone, fetch, or dependency mutation occurred.

```text
python3 Stage1_Instances/THM-M-1015/build_obligation_artifacts.py
  exit 0: wrote 17 obligations and 38 typed edges; denominator digest
  fb5265f3a59199de30de2aab36aa8b0371b08d24cb0b010aaf919d08b59a6a53

python3 Stage1_Instances/THM-M-1015/check_obligation_tree.py
  exit 0: input hashes, denominators, full node schema, seven graph classes,
  reciprocal proof/composition edges, proof acyclicity, recipes, budgets,
  prohibited Lean tokens, and open-root boundary passed

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1015/ObligationTree.lean
  exit 0: root_compose elaborated from four explicit branch premises; three
  pinned declaration probes passed; #print axioms reported propext,
  Classical.choice, and Quot.sound

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546

python3 scripts/stage1_target.py show THM-M-1015
  exit 0: rank 294; planned; L0/rework_required; theorem_complete=false

python3 Stage1_Instances/THM-M-1015/check_statement.py
  exit 0: exact statement digest and four killed mutations agreed

python3 Stage1_Instances/THM-M-1015/check_anchor_audit.py
  exit 0: target fingerprint, immutable pin, module hash, and three candidates agreed

python3 -m json.tool Stage1_Instances/THM-M-1015/obligation-registry.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1015/typed-graphs.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1015/validation-specs.json >/dev/null
  exit 0 for all three files: valid JSON

git diff --check -- Stage1_Instances/THM-M-1015 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 frozen registry, typed graphs, recipes, readable tree, and
conditional composition harness, pending master acceptance. It marks no proof obligation closed.
Pair/add/multiply anchor integration, the quotient-local proof, primary-source review, readable
review, transitive trust, independent replay, `AUDIT-Z`, `THEOREM-Z`, and release remain open.
