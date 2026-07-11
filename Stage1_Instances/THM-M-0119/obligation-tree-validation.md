# THM-M-0119 obligation-tree validation

Item: `S56-M-0119-OBLIGATION_TREE`

Validation date: `2026-07-12` (Asia/Shanghai)

Base revision: `3773db6f4af23b2524ac9ffc12352c352b2f5532`

## Frozen result

Registry version 1 freezes 33 obligations and 42 edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs.
Twenty-eight obligations are required machine nodes, five are informational
overlays, and all remain open. The canonical denominator digest is
`d9c76b6bb201afa0b50c3e3a38e86e6db4faab64d250009313606b3ae79592db`.

## Commands and results

All commands ran inside this worker clone. Lean reused the existing canonical
pinned `.lake` artifacts; no update, build, clone, fetch, or dependency mutation
was performed.

```text
python3 Stage1_Instances/THM-M-0119/build_obligation_artifacts.py
  exit 0: wrote 33 obligations and 42 typed edges; emitted denominator digest

python3 Stage1_Instances/THM-M-0119/check_obligation_tree.py
  exit 0: schemas, canonical denominator, seven graph classes, reciprocal edge
  indices, proof acyclicity, complete required-node reachability, semantic
  ledgers, open M3 boundary, and exact four-node cut set passed

python3 -m json.tool Stage1_Instances/THM-M-0119/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0119/typed-graphs.json
  exit 0 for both files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0119/ObligationTree.lean
  exit 0: positive_degrees_compose and implication_compose elaborated;
  #print axioms reported that neither declaration depends on any axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets passed

python3 scripts/stage1_target.py show THM-M-0119
  exit 0: rank 38, planned, legacy artifacts unaccepted, theorem incomplete

git diff --check -- Stage1_Instances/THM-M-0119 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Status boundary

This evidence self-tests only the frozen registry, typed graphs, and two
conditional composition lemmas. No birational, singularity, positivity,
cohomological, or vanishing proof body is supplied. The root remains M3 and all
obligations remain open. Primary-source acceptance, readable review, trust
closure, independent validation, `AUDIT-Z`, `THEOREM-Z`, theorem completion,
release, and master acceptance remain open. The pre-existing untracked
`Formalizations/Lean/.lake` worker artifact also makes this nonrelease evidence.
