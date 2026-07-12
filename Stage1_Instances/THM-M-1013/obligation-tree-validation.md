# THM-M-1013 obligation-tree validation

Item: `S56-M-1013-OBLIGATION_TREE`. Base revision:
`240ce7cf9937f5d92636d86bdc3c05b9224b27b0`.

Validation ran from the isolated worker clone on 2026-07-12. It reused the canonical pinned Lake
artifacts through the clone's pre-existing untracked `.lake` symlink. No dependency update, fetch,
clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1013/build_obligation_artifacts.py
  exit 0
  41873784159809cc09371822dc5121c17dbfa74bf6613c734eb709a9babfc970

python3 Stage1_Instances/THM-M-1013/check_obligation_tree.py
  exit 0
  PASS THM-M-1013 obligation tree: 14 obligations, 36 typed edges
  registry denominator sha256: 41873784159809cc09371822dc5121c17dbfa74bf6613c734eb709a9babfc970
  root closure: open (M3); proof execution and release gates remain downstream

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1013/ObligationTree.lean
  exit 0
  compose_directions consumes exact forward and reverse children and returns ExactTarget
  zero_dimension_boundary checks the d = 0 specialization remains in scope
  both axiom reports: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: rev-5.6 structural standard passes for 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: target manifest and ordered projection pass

python3 scripts/stage1_target.py show THM-M-1013
  exit 0: rank 292; planned; theorem completion false

python3 -m json.tool Stage1_Instances/THM-M-1013/obligation-registry.json
  exit 0

python3 -m json.tool Stage1_Instances/THM-M-1013/typed-graphs.json
  exit 0

rg -n --glob '*.lean' '(^|[^[:alnum:]_])(sorry|admit|axiom)[[:space:]]+[[:alnum:]_]|sorryAx'
  Stage1_Instances/THM-M-1013
  exit 1: no prohibited proof construct or fabricated-result marker found

git diff --check -- Stage1_Instances/THM-M-1013 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The first Lean attempt failed before validation because the initial generic `WeakLimit` helper did
not provide the measurable-space instance required by `ProbabilityMeasure`. The helper was narrowed
to the frozen `Vector d` domain, and the exact command above then passed. This corrected attempt is
the evidence-bearing run; the failure introduced no proof assumption or dependency mutation.

## Status boundary

The obligation-tree phase is locally self-tested and ready for master inspection. It freezes the
registry denominator, all seven required graph families, the immediate root cut set, step budgets,
and a checked conditional composition. It does not accept the anchor candidates as proof-phase
closure, complete primary-source review, establish release-grade provenance/trust, or prove the
theorem. Root status remains `[H1, M3, R3]`; theorem completion is false.
