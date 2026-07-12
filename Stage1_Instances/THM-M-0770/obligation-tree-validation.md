# THM-M-0770 obligation-tree validation

Date: 2026-07-12  
Item: `S56-M-0770-OBLIGATION_TREE`  
Base revision: `4586a02100c5be8974b9cb0ab2d4e9e51d0480f0`

The deterministic builder freezes 13 obligations and seven separate typed
graphs. The validator recomputes statement and anchor input hashes, recomputes
the denominator, checks complete node schemas, edge endpoint/index integrity,
reciprocal proof/composition edges, proof acyclicity, validation-recipe
coverage, the open-root boundary, and narrow Lean elaboration. It does not
modify or fetch the shared pinned dependencies.

```text
$ python3 Stage1_Instances/THM-M-0770/build_obligation_artifacts.py
exit 0
d5b67591e736730f839146d0a89ac4a7beac27733d034d68556499e8b2e06d20

$ python3 Stage1_Instances/THM-M-0770/check_obligation_tree.py
exit 0
PASS THM-M-0770 obligation tree: 13 obligations, 17 typed edges
registry denominator sha256: d5b67591e736730f839146d0a89ac4a7beac27733d034d68556499e8b2e06d20
Lean composition probes: exit 0, axioms []
root closure: open (M3); audited anchor awaits proof-node acceptance

$ git diff --check -- Stage1_Instances/THM-M-0770 .stage1-worker-selftest.json
exit 0, no output
```

The Lean command executed by the validator is `lake env lean
Stage1_Instances/THM-M-0770/ObligationTree.lean` from `Formalizations/Lean`.
Both abstract composition probes elaborate and report no axioms. This is only
evidence for exact child-to-parent interface composition; it does not execute
or accept the Zorn proof body.
