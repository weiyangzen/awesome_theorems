# THM-M-1007 obligation-tree validation

Item: `S56-M-1007-OBLIGATION_TREE`

Base revision: `31c0253e7592e9a19dd9571adcf10eb0023effda`

Validation date: `2026-07-12` (Asia/Shanghai)

## Frozen result

Registry version 1 freezes 19 obligations and 54 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Sixteen obligations
are root-relevant machine obligations; three are informational assurance overlays. The frozen
denominator SHA-256 is `0a29c34a938eeb9ddb91009316aabe1be97f16a7606fbc6da3c3aea7429e87cf`.

The Lean harness consumes exact necessity and sufficiency premises and returns the exact
fixed-cutoff root biconditional. It does not instantiate either premise. The root remains open at
`M3`, and no obligation is marked closed.

## Commands and results

Commands ran from the repository root unless a working directory is shown. The pre-existing
canonical `.lake` dependency closure was reused; no update, build, clone, fetch, or dependency
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1007
  exit 0: rank 287; planned; legacy artifacts unaccepted; theorem_complete=false

python3 Stage1_Instances/THM-M-1007/build_obligation_artifacts.py
  exit 0: wrote 19 obligations and 54 typed edges; denominator digest
  0a29c34a938eeb9ddb91009316aabe1be97f16a7606fbc6da3c3aea7429e87cf

python3 Stage1_Instances/THM-M-1007/check_obligation_tree.py
  exit 0: source-input hashes, frozen denominators, node schema, seven graph classes,
  reciprocal proof/composition edges, proof acyclicity, structured recipes, budgets,
  forbidden Lean tokens, and the open-root boundary passed

python3 -m json.tool Stage1_Instances/THM-M-1007/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1007/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-1007/validation-specs.json
  exit 0 for all three files: valid JSON

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-1007/ObligationTree.lean
  exit 0: root_of_directions and exact-type probe elaborated; #print axioms reported
  [propext, Classical.choice, Quot.sound] and no sorryAx

python3 Stage1_Instances/THM-M-1007/check_statement.py
  exit 0: canonical expression digest 3b1a82b3fc0ce70be489e8a49279e3f29cfe244f7a50c28f5c4e5de26894cf38;
  four structural mutations remained distinguished at the pinned toolchain

rg -n '\bsorry\b|\badmit\b|\baxiom\b|sorryAx' \
  Stage1_Instances/THM-M-1007/ObligationTree.lean
  exit 1: no forbidden proof shortcuts (rg exit 1 means no matches)

git diff --check -- Stage1_Instances/THM-M-1007 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Status boundary

This receipt supports only the version-1 registry, seven typed graph classes, structured recipes,
readable architecture, and conditional iff-composition harness, pending master acceptance. The
frozen proof cut set contains `M1007-C-TRUNC-PROPS`, `M1007-C-EVENT-INDEP`, both large-jump
Borel-Cantelli branches, `M1007-T-EVENTUAL`, and both bounded independent-series directions.
Primary-source review, proof bodies, body provenance, readable independent review, transitive
trust, hermetic replay, `AUDIT-Z`, `THEOREM-Z`, and release remain open.
