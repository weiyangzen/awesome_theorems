# Obligation-tree validation

Item: `S56-M-1419-OBLIGATION_TREE`  
Base revision: `302112912689e2e6fcac50a7c0b0ab94afaef090`

The registry contains 14 unique root-relevant obligations and freezes denominator SHA-256
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`. Structural validation
checks source hashes, denominator projection, eligibility projections, typed edge endpoints and
reciprocals, proof acyclicity/reachability, local budgets, closure boundaries, and forbidden Lean
placeholders. Lean elaboration checks the exact conditional composition and reports only
`propext`, `Classical.choice`, and `Quot.sound`; it does not close its premise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework targets |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1419/build_obligation_artifacts.py` | 0 | deterministically generated 14 obligations and seven typed graphs |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | 14 obligations, 41 typed edges, open M3 root |
| scoped `lake env lean` commands recorded below | 0 | statement olean and `ObligationTree.lean` elaborated with pinned Lean/mathlib |
| `python3 -m json.tool` on the four structured target artifacts | 0 | all JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-1419 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The scoped Lean recipe is:

```bash
cd Formalizations/Lean
lake env lean --root=../../Stage1_Instances/THM-M-1419 \
  -o ../../Stage1_Instances/THM-M-1419/OseledetsStatement.olean \
  ../../Stage1_Instances/THM-M-1419/OseledetsStatement.lean
LEAN_PATH="../../Stage1_Instances/THM-M-1419:$(lake env printenv LEAN_PATH)" \
  lake env lean --root=../../Stage1_Instances/THM-M-1419 \
  ../../Stage1_Instances/THM-M-1419/ObligationTree.lean
rm ../../Stage1_Instances/THM-M-1419/OseledetsStatement.olean
```

No `lake update`, build, fetch, clone, or `.lake` mutation was performed. Remaining failures are
the four-node immediate root cut, their exterior-power/Kingman and filtration descendants,
primary-source review, provenance/trust closure, proof, hermetic validation, and release. Thus the
obligation-tree phase alone is self-tested pending master acceptance; the theorem is not complete.
