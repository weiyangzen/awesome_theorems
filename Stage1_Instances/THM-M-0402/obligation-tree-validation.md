# THM-M-0402 obligation-tree validation

Base revision: `026b21f5359f8f2e643d0f1ee2846428c517be20`.

This validation is scoped to the frozen registry and typed architecture. It proves no mathematical
node and makes no theorem-completion claim. No dependency was fetched, built, updated, or modified.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets; ranks 1..1546; all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0402
  exit 0: rank 15; lifecycle planned; theorem_complete=false
(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0402/Statement.lean)
  exit 0: canonical EvertseSUnitStatement elaborated and printed with pinned Lean/mathlib artifacts
python3 Stage1_Instances/THM-M-0402/validate_obligation_tree.py
  exit 0: 10 obligations, 19 typed edges, denominator hash matched, root open M3
python3 -m json.tool Stage1_Instances/THM-M-0402/obligation-registry.json
  exit 0
python3 -m json.tool Stage1_Instances/THM-M-0402/obligation-graphs.json
  exit 0
git diff --check -- Stage1_Instances/THM-M-0402 .stage1-worker-selftest.json
  exit 0
```

The structural validator checks registry/node identity, denominator projections, required node
fields, substantive step ledgers with budgets at most 100, reciprocal typed adjacency, global edge
identity, proof acyclicity, root reachability of every mathematical machine obligation, and the
fail-closed closure boundary. The Lean command rechecks only the prerequisite exact statement; it
does not provide proof credit for any obligation.
