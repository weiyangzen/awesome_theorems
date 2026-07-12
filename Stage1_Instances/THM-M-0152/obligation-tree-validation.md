# THM-M-0152 obligation-tree validation

Item: `S56-M-0152-OBLIGATION_TREE`. Base revision:
`0a66013e1558a3bc4e31c9d7f64c0e8fb1dfebab`.

Validation ran from the worker clone on 2026-07-12. It reused the canonical
pinned Lake artifacts. No dependency update, build, clone, or fetch was run.

```text
python3 Stage1_Instances/THM-M-0152/build_obligation_artifacts.py
  exit 0
  fa50f18f390428eeadcb5308decdcc9f9cce7cf2377a1675c74e033b557f634b

python3 Stage1_Instances/THM-M-0152/check_obligation_tree.py
  exit 0
  PASS THM-M-0152 obligation tree: 17 obligations, 41 typed edges
  registry denominator sha256: fa50f18f...f634b
  root closure: open (M4); intrinsic formula and coordinate invariance remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0152/Statement.lean
  exit 0
  exact target and its checked definitional transport elaborated

python3 Stage1_Instances/THM-M-0152/check_anchor_audit.py
  exit 0
  exact target identity, pins, eight Lean probes, three candidates, and M4 boundary agreed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0152
  exit 0: rank 651, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0152 .stage1-worker-selftest.json
  exit 0; no output
```

The structural check validates content binding to the statement and anchor
audit, the frozen denominator, all required node fields and step budgets,
typed graph endpoints and adjacency, reciprocal proof/composition edges,
acyclic proof reachability, per-node validation recipes, hygiene, and the
truthful open-root boundary. Lean re-elaboration checks only the frozen target
and definitional transport; it is not evidence for any open curvature lemma.
There is no accepted master receipt yet.
