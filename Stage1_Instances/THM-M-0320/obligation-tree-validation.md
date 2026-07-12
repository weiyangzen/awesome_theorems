# THM-M-0320 obligation-tree validation

Item: `S56-M-0320-OBLIGATION_TREE`  
Base revision: `83f5974d31f82ec4ad3b558c2e1c5078e070e986`

Validation ran in the worker clone on 2026-07-12. It reused the existing
pinned Lake artifacts; no dependency update, build, clone, or fetch ran.

```text
python3 Stage1_Instances/THM-M-0320/build_obligation_artifacts.py
  exit 0
  b513af2baba56c289271260eadeeaea0c1df46090f3728123c0395b955b0b974

python3 Stage1_Instances/THM-M-0320/check_obligation_tree.py
  exit 0
  PASS THM-M-0320 obligation tree: 10 obligations, 22 typed edges
  registry denominator sha256: b513af2baba56c289271260eadeeaea0c1df46090f3728123c0395b955b0b974
  root closure: open (M1); closed-graph bridge and integrated core remain open

LEAN_PATH="$(cd Formalizations/Lean && lake env printenv LEAN_PATH)"
LEAN_BIN="$(cd Formalizations/Lean && lake env which lean)"
cd Stage1_Instances/THM-M-0320
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  compact_of_closed_bounded depends on [propext, Classical.choice, Quot.sound]
  root_of_closedGraph_packages depends on [propext, Classical.choice, Quot.sound]

rg -n '\bsorry\b|\badmit\b|(^|\s)axiom\s|unsafe|implemented_by' \
  Stage1_Instances/THM-M-0320 --glob '*.lean'; test $? -eq 1
  exit 0; the search itself returned the expected no-match exit 1

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0320
  exit 0; rank 686, planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0320/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0320/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0320/validation-specs.json
  each exit 0
```

The structural check recomputes the frozen denominator, checks eligibility
projections, node ledgers and step budgets, all seven graph types, reciprocal
proof edges, graph adjacency, root reachability, recipe coverage, open closure,
and Lean-source hygiene. The scoped Lean run checks the exact statement,
Euclidean compactness transport, explicit graph/core interfaces, and conditional
child-to-parent composition against the pinned environment.

This is node-specific worker evidence pending master acceptance. It does not
close `M0320-T-GRAPH`, `M0320-C-CORE`, or `M0320-T-SUBTYPE`; it does not resolve
the external candidate's license or compatibility; and it does not establish
audit or theorem completion. There is no accepted receipt ID at this phase.
