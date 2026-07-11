# THM-M-0112 obligation-tree validation

Item: `S56-M-0112-OBLIGATION_TREE`. Base revision:
`3773db6f4af23b2524ac9ffc12352c352b2f5532`.

Validation ran inside the worker clone on 2026-07-12. It reused the existing pinned Lake artifacts;
no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0112/build_obligation_artifacts.py
  exit 0
  5d119562299ca46e160d86947fd92a0cd5c0d50bfbac345da26eacee0b7df7f4

python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py
  exit 0
  PASS THM-M-0112 obligation tree: 13 obligations, 31 typed edges
  registry denominator sha256: 5d119562299ca46e160d86947fd92a0cd5c0d50bfbac345da26eacee0b7df7f4
  root closure: open (M3); below-boundary and boundary packages remain M4

cd Formalizations/Lean &&
  LEAN_PATH=$(lake env printenv LEAN_PATH) lake env lean \
    -o ../../Stage1_Instances/THM-M-0112/Statement.olean \
    ../../Stage1_Instances/THM-M-0112/Statement.lean
  exit 1
  Lean rejected an input outside its configured root directory. No artifact was produced.

cd Stage1_Instances/THM-M-0112 &&
  LEAN_BIN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) &&
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:"$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
  exit 0
  weakTopologicalLefschetz_of_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  The temporary Statement.olean was removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets consistent
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0112
  exit 0: rank 35, planned, theorem_complete false
```

The successful narrow Lean command uses the pinned Lean executable selected by `lake env which
lean` and Lake's existing `LEAN_PATH`. The earlier root-directory failure is retained rather than
hidden and supports no claim.

The checks bind the registry to the statement and anchor-audit bytes, recompute the frozen
denominator, validate every required node field and budget, check reciprocal proof edges and graph
adjacency, reject proof cycles, verify structured recipe coverage and no-network policy, scan the
Lean source for forbidden proof devices, and elaborate the exact conditional composition. The
composition consumes both package premises and yields the frozen root, but neither premise has a
proof body. Root debt remains `[H1, M3, R3]`; there is no theorem-completion or accepted-receipt
claim, and master acceptance remains required.
