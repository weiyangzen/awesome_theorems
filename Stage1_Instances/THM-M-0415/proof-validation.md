# THM-M-0415 proof-phase validation

Item: `S56-M-0415-PROOF`. Base revision:
`081824d18f2e6414e9aad5a74d8ada82eaa1c9ea`.

`Proof.lean` implements a direct wrapper at the exact frozen
`IdealClassGroupFiniteTarget` and separately checks the frozen
`FintypePresentation` child-to-root composition. The terminal body is the
pinned mathlib class-number construction at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; it is imported rather than
relocated or counted twice. This supports a provisional `M0-W` root proposal,
not theorem completion.

Validation ran in the worker clone on 2026-07-12. Existing pinned `.lake`
artifacts were reused through the canonical worker symlink. No update, build,
clone, fetch, or other dependency mutation was run.

```text
cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0415/check_proof.sh
  exit 0
  idealClassGroupFinite depends on axioms:
    [propext, Classical.choice, Quot.sound]
  idealClassGroupFinite_via_frozen_composition depends on axioms:
    [propext, Classical.choice, Quot.sound]
  instFintypeClassGroup, fintypeOfAdmissibleOfFinite,
  fintypeOfAdmissibleOfAlgebraic, and mkMMem_surjective each report the same
  three-axiom set

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0415
  exit 0: rank 70, planned, theorem_complete false

python3 Stage1_Instances/THM-M-0415/check_proof.py
  exit 0: PASS THM-M-0415 proof phase: exact root wrapper pinned and checked

python3 -m json.tool Stage1_Instances/THM-M-0415/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0415 \
  .stage1-worker-selftest.json
  exit 0: no output
```

The root proof is kernel-elaborated, but proof execution is not release
assurance. `M0415-S-FOUNDATION`, `M0415-X-SOURCE`, and
`M0415-X-PROVENANCE` still require their downstream validation or human gates.
H0, R0, a complete transitive trust/provenance audit, hermetic replay,
independent verification, and master acceptance are not claimed.
