# THM-M-0107 obligation-tree validation

Item: `S56-M-0107-OBLIGATION_TREE`

Base revision: `b11e1f5a1a404420eee7320a845fdb9df48bec0c`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 29 obligations and 30 typed edges across separate proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs. Twenty-five obligations are
root-relevant and machine/source eligible; four are informational provenance or trust overlays.
The denominator projection digest is
`973eb733d98c80dc553754ff92e51226b563801b68349cf95e3921dc7dc416a7`.

## Commands and results

Commands ran at the repository root unless the command explicitly changes directory.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0107
  exit 0: execution_rank=31; lifecycle_mode=planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0107/build_obligation_artifacts.py
  exit 0: wrote 29 obligations and 30 typed edges

python3 Stage1_Instances/THM-M-0107/check_obligation_tree.py
  exit 0: registry digest, fields, denominators, seven graph classes, reciprocal
  indices, reachability, acyclicity, ledgers, and open-root boundary passed;
  root remains M3 with the finite-envelope bridge as the explicit cut set

python3 -m json.tool Stage1_Instances/THM-M-0107/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0107/typed-graphs.json
  exit 0 for both files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0107/ObligationTree.lean
  exit 0: conditional root_compose and exact-type check elaborated; #print axioms
  reported propext, Classical.choice, and Quot.sound

git diff --check -- Stage1_Instances/THM-M-0107 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The existing pinned `.lake` closure was reused. No update, build, clone, fetch, or dependency
mutation was performed. The pre-existing untracked `.lake` link/artifact makes this nonrelease
worker evidence.

## Status boundary

This receipt supports only the frozen registry, typed graphs, and conditional composition harness.
No obligation is marked closed. The finite envelope, integral-to-finite bridge, exact proof bodies,
pinpoint source review, readable reconstruction, transitive trust closure, independent validation,
`AUDIT-Z`, `THEOREM-Z`, and master acceptance remain open.
