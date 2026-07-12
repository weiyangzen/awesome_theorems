# Obligation-tree validation

Item: `S56-M-0318-OBLIGATION_TREE`  
Base revision: `83f5974d31f82ec4ad3b558c2e1c5078e070e986`

Commands are run from the worker-clone root. Exact final results:

```text
python3 Stage1_Instances/THM-M-0318/check_obligation_tree.py
exit 0: obligation tree valid: 12 obligations, 12 typed nodes, digest 57d77a8fccc8308a704f1185c92057a17791da515e45325179aa81d000376f87

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0318/ObligationTree.lean
exit 0: #check prints compose_schauder with ApproximationEngine and CompactLimitEngine as explicit premises

python3 Docs/tools/check_stage1_standard.py
exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

git diff --check -- Stage1_Instances/THM-M-0318
exit 0: no output
```

The Lean run uses the existing pinned `.lake` linkage; no update, build, clone, or fetch was run.
The harness proves only conditional composition. No open leaf, root proof, H0, validation, release,
or theorem-completion claim is made.
