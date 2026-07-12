# THM-M-0325 obligation-tree validation

Item: `S56-M-0325-OBLIGATION_TREE`. Base revision:
`81c766970d38b9ae3179b58cc75a46425a624c6e`.

Validation ran from the worker clone on 2026-07-12. It reused the existing
pinned Lake artifacts and ran no update, build, fetch, clone, or network step.

```text
python3 Stage1_Instances/THM-M-0325/build_obligation_artifacts.py
  exit 0
  4c41e44f32c7c300ac25319a49fd14dcf197599756525b2dec8dcdce4207703c

python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py
  exit 0
  PASS THM-M-0325 obligation tree: 15 obligations, 33 typed edges
  registry denominator sha256: 4c41e44f32c7c300ac25319a49fd14dcf197599756525b2dec8dcdce4207703c
  root closure: open (M3); Grothendieck analytic proof package remains M4

cd Formalizations/Lean &&
  LEAN_PATH=$(lake env printenv LEAN_PATH) lake env lean -R ../.. \
    -o ../../Stage1_Instances/THM-M-0325/Statement.olean \
    ../../Stage1_Instances/THM-M-0325/Statement.lean &&
  LEAN_PATH=../../Stage1_Instances/THM-M-0325:$(lake env printenv LEAN_PATH) \
    lake env lean -R ../.. \
    ../../Stage1_Instances/THM-M-0325/ObligationTree.lean
  exit 0
  target_of_proofPackage depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0325
  exit 0: rank 214, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0325
  exit 0; no output
```

The first scoped Lean attempt omitted `-R ../..` and exited 1 because Lean
requires an input file outside `Formalizations/Lean` to be contained in the
configured root. After adding that root flag, an initial elaboration exposed an
unfixed universe metavariable in `GrothendieckProofPackage`; the declaration was
corrected to carry explicit universe `u`, and the exact command above passed.

These checks validate source-bound hashes, frozen eligibility denominators,
required node ledgers, all seven typed graph families, reciprocal proof edges,
acyclic root reachability, structured recipe coverage, placeholder hygiene,
Lean elaboration, the exact conditional root output, and its axiom surface.
They do not prove the explicit analytic package. There is no accepted receipt;
master acceptance remains required.
