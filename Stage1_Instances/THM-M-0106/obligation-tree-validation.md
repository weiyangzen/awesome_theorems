# THM-M-0106 obligation-tree validation

Item: `S56-M-0106-OBLIGATION_TREE`

Base revision: `b11e1f5a1a404420eee7320a845fdb9df48bec0c`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 18 obligations and 39 directed typed edges across
separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. Fifteen obligations are root-relevant machine obligations;
three are informational overlays. The denominator digest is
`c0bea0cca56af925922c0bf56a324e7a6fbfe82459ee7f303d3676a11fcc12ce`.

## Commands and results

All commands ran from the repository root except the explicitly prefixed Lean
command. Exact final results are recorded below.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0106
  exit 0: execution_rank=30; lifecycle_mode=planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0106/build_obligation_artifacts.py
  exit 0: wrote 18 obligations and 39 typed edges; denominator digest
  c0bea0cca56af925922c0bf56a324e7a6fbfe82459ee7f303d3676a11fcc12ce

python3 Stage1_Instances/THM-M-0106/check_obligation_tree.py
  exit 0: schemas, source-input hashes, frozen denominators, seven graph
  classes, reciprocal proof/composition edges, acyclicity, reachability,
  structured recipes, budgets, prohibited tokens, and open-root boundary pass

python3 -m json.tool Stage1_Instances/THM-M-0106/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0106/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0106/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0106/ObligationTree.lean
  exit 0: root_compose elaborated from the explicit AlgebraicCore premise;
  #check probes passed; #print axioms reported [propext, Classical.choice,
  Quot.sound]

python3 Stage1_Instances/THM-M-0106/check_statement.py
  exit 0: statement digest
  4980834b63da78609158f944b53234d72089e2bfaacb348461de2651aa671209;
  four mutations killed; mathlib revision agrees

python3 Stage1_Instances/THM-M-0106/check_anchor_audit.py
  exit 0: audit expression definitionally matches the frozen statement and
  the audited candidate composition elaborates

git diff --check -- Stage1_Instances/THM-M-0106 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The canonical pinned `.lake` closure was reused. No `lake update`, build,
clone, fetch, or dependency mutation was performed. The pre-existing
untracked `Formalizations/Lean/.lake` artifact makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 registry, typed graphs, structured
recipes, readable tree, and conditional composition harness. No obligation is
marked closed. The root remains M2 with `M0106-L-FINITE` as the cut set.
Proof-node acceptance, primary-source review, readable reconstruction review,
transitive trust, independent replay, `AUDIT-Z`, `THEOREM-Z`, release, and
master acceptance remain open.
