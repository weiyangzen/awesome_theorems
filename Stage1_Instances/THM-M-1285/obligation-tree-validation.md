# THM-M-1285 obligation-tree validation

Item: `S56-M-1285-OBLIGATION_TREE`. Base revision:
`4fefd52b2fcf2d237b21cafcc2d72511afaf5cfb`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No update, build, dependency fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-1285/build_obligation_artifacts.py
  exit 0
  6e441bf6a37b0bb83ae0a752e94b30ebf47c8eb567a9284969e869f68b032e9c

python3 Stage1_Instances/THM-M-1285/check_obligation_tree.py
  exit 0
  PASS THM-M-1285 obligation tree: 16 obligations, 83 typed edges
  registry denominator sha256: 6e441bf6a37b0bb83ae0a752e94b30ebf47c8eb567a9284969e869f68b032e9c
  root closure: open (M3); SchwarzConstructionPackage remains M4

LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-1285
LEAN_PATH="$LP" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LP" "$LEAN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  schwarzRearrangementTarget_of_construction depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1285
  exit 0: rank 456, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1285 .stage1-worker-selftest.json
  exit 0; no output
```

The structural validator checks the statement and anchor-audit freeze hashes,
the canonical registry denominator, eligibility projections, node schemas and
step limits, all seven graph kinds, edge adjacency, reciprocal proof edges,
proof-DAG acyclicity/reachability, the open root boundary, and placeholder
hygiene. Lean separately checks that the explicit construction premise has the
exact shape required to compose into the frozen root. The printed axioms arise
from imported foundational definitions; there is no `sorryAx`.

The construction package remains uninhabited. Consequently this receipt is
only worker self-test evidence for the obligation-tree phase pending master
acceptance. It supplies no proof, source acceptance, full audit completion, or
theorem completion.
