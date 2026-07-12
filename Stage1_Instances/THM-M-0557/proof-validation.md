# THM-M-0557 proof-phase validation

Item: `S56-M-0557-PROOF`  
Base revision: `308079b76fbc748b8f9d71a25d1e04b19c090ccf`

## Implemented proof

`Proof.lean` implements both frozen structure branches through the existing
pinned mathlib instances. `groupStructureBranch` obtains the positive-dimensional
group structure, `commutativeStructureBranch` obtains the dimension-at-least-two
commutative group structure, and `homotopyGroupStructureTarget` composes them.
`check_proof.py` checks that the root declaration's proposition is textually
identical after whitespace normalization to the expression frozen in
`Statement.lean`.

This closes the proof bodies represented by `M0557-GROUP`,
`M0557-GROUP-TRANSFER`, `M0557-COMM`, `M0557-EH`, and `M0557-DISTRIB`, then
closes the conjunction through `M0557-COMPOSE`. It does not accept the separate
transitive provenance/trust gate, source gate, readability gate, validation, or
release. Therefore theorem completion remains false.

## Commands and exact results

All commands ran in this worker clone. No update, build, clone, fetch, network
operation, or intentional `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0557
  exit 0: rank 605; planned; L0/rework_required; theorem_complete=false

python3 Stage1_Instances/THM-M-0557/check_obligation_tree.py
  exit 0: 9 obligations and 49 typed edges; denominator 6e74b519...08596

python3 Stage1_Instances/THM-M-0557/check_proof.py
  exit 0: exact frozen expression and both structure branches implemented

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0557/Proof.lean
  exit 0: all three declarations elaborated; #print axioms reported only
  propext, Classical.choice, and Quot.sound

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0557/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0557
  exit 0: no whitespace errors
```

An initial combined validation invocation ran the five Python commands from
`Formalizations/Lean` instead of the repository root, so those five commands
exited 2 with path-not-found errors. The Lean command in that invocation exited
0. The Python commands were immediately rerun from the correct directory and
their successful results are recorded above.
