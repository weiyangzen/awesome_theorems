# THM-M-0698 proof-phase validation

Item: `S56-M-0698-PROOF`. Base revision:
`136ebf643dcdcbc42cef34e415177189578060ef`.

`Proof.lean` closes the frozen `FiniteToSatisfiable` cut with the exact
manifest-pinned mathlib declaration
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable`. It then
checks the frozen child-to-root composition and a separate direct wrapper at
the exact `FirstOrderCompactnessTarget`. The terminal ultraproduct proof body
remains owned by pinned mathlib and is counted once. This supports a
provisional `M0-W` root proposal, not theorem completion.

## Commands and results

Commands ran in the worker clone on 2026-07-12. The Lean checker compiled
temporary local `Statement.olean` and `ObligationTree.olean` files, placed only
that temporary directory before the canonical pinned `LEAN_PATH`, and removed
the files on exit. No update, build, clone, fetch, or mutation of `.lake` was
performed.

```text
cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0698/check_proof.sh
  exit 0
  The reverse-direction wrapper, frozen composition, direct root wrapper, and
  pinned terminal declaration elaborated. Every proof-phase #print axioms
  result was [propext, Classical.choice, Quot.sound].

python3 Stage1_Instances/THM-M-0698/check_proof.py
  exit 0: PASS THM-M-0698 proof phase: exact pinned compactness root closed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0698
  exit 0: rank 739, planned, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-0698/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0698 \
  .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This self-tests proof-phase machine closure only. Primary-source and readable
reconstruction debt, transitive trust/provenance validation, hermetic replay,
independent verification, master acceptance, audit completion, and theorem
completion remain open.
