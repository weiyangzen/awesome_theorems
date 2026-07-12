# THM-M-1268 proof-phase validation

Item: `S56-M-1268-PROOF`. Base revision:
`4ac441e7be0c42ea78cddc541390953fa7318de7`.

`Proof.lean` supplies genuine bodies for all three members of the frozen root cut. It derives
convexity of EReal sublevels directly from the frozen Jensen inequality, turns norm-closed convex
sublevels into weakly closed sublevels with pinned `Convex.toWeakSpace_closure`, and proves the
converse by composing with the continuous norm-to-weak map. `ProofExact.lean` imports independently
compiled copies of `Statement` and `Proof` and checks that the result inhabits the exact canonical
statement-phase declaration.

Validation ran in the worker clone on 2026-07-12. It reused the canonical pinned Lake artifacts.
No update, build, dependency fetch/clone, network operation, or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-1268/check_proof.sh
  exit 0
  Statement.lean and Proof.lean compiled to isolated temporary oleans;
  ProofExact.lean checked the exact canonical target; the root axiom report was
  [propext, Classical.choice, Quot.sound], with no sorryAx

python3 Stage1_Instances/THM-M-1268/check_obligation_tree.py
  exit 0: frozen denominator, IDs, graph indexes, closure boundary, and cut set passed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-1268
  exit 0: rank 444, planned, theorem incomplete

git diff --check -- Stage1_Instances/THM-M-1268 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The proof node is self-tested pending master acceptance. This phase does not claim accepted proof
state, audit completion, hermetic validation, independent verification, or theorem completion;
those decisions belong to the downstream validation, release, and integration lanes.
