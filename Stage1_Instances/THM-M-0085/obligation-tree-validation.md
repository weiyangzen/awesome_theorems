# THM-M-0085 obligation-tree validation

Item: `S56-M-0085-OBLIGATION_TREE`. Base revision:
`1e6618db41628006f4ba98117f6425af1eb6a0ba`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned
Lake environment. No update, build, fetch, clone, or dependency mutation was
run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  ok: 15 assurance groups and 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0085
  exit 0
  rank 140; planned; theorem_complete false

python3 Stage1_Instances/THM-M-0085/build_obligation_artifacts.py
  exit 0
  07a2af67057c0bb62bd66dd5d36c860025cf83c18c677b6d4321bd30c943cf67

python3 Stage1_Instances/THM-M-0085/check_obligation_tree.py
  exit 0
  PASS THM-M-0085 obligation tree: 5 obligations, 11 typed edges
  registry denominator sha256: 07a2af67057c0bb62bd66dd5d36c860025cf83c18c677b6d4321bd30c943cf67
  root closure: open; exact pinned candidate composition elaborated, named proof and receipts pending

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0085/Statement.lean
  exit 0
  exact frozen statement and expansion elaborated

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0085/ObligationTree.lean
  exit 0
  monadicOfCreatesGSplitCoequalizers depends on axioms:
    [propext, Classical.choice, Quot.sound]

git diff --check -- Stage1_Instances/THM-M-0085 .stage1-worker-selftest.json
  exit 0; no output
```

The structural checker validates the statement and anchor freeze hashes,
stable IDs, frozen eligibility denominators, all required node ledgers, seven
separate typed graphs, reciprocal proof edges, graph adjacency, validation
recipe coverage, and placeholder hygiene. Lean checks the explicit-premise to
local-instance bridge and the exact fixed-adjunction `eqv` projection.

This is obligation-tree evidence only. Root closure, a named proof-phase
wrapper, accepted receipts, audit completion, and theorem completion remain
open and are not claimed.
