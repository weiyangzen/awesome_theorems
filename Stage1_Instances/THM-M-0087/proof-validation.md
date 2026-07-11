# THM-M-0087 proof-phase validation

Item: `S56-M-0087-PROOF`. Base revision:
`03523e6728e323f2844994a3e6a20ac7c269c6eb`.

`Proof.lean` integrates real pinned proof bodies for the four mathematical
packages in the frozen Gabriel-Popescu target. It checks both the frozen
child-to-root composition and a direct exact-target wrapper. The terminal
bodies are imported from mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, not duplicated or counted twice.
This supports a provisional `M0-W` root proposal, not theorem completion.

Validation ran in the worker clone on 2026-07-12 (Asia/Shanghai). Existing
pinned `.lake` artifacts were reused through the canonical worker symlink. No
update, build, clone, fetch, or other dependency mutation was run.

```text
cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0087/check_proof.sh
  exit 0
  fullPackage, faithfulPackage, adjunctionPackage, finiteLimitsPackage,
  gabrielPopescu_via_frozen_composition, gabrielPopescu,
  kernel_ι_d_comp_d, exists_d_comp_eq_d, and preservesInjectiveObjects
  each depend only on [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0087
  exit 0: rank 133, planned, theorem_complete false

python3 Stage1_Instances/THM-M-0087/check_proof.py
  exit 0: PASS THM-M-0087 proof phase: exact Gabriel-Popescu root pinned and checked

python3 -m json.tool Stage1_Instances/THM-M-0087/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0087 \
  .stage1-worker-selftest.json
  exit 0: no output
```

The proof node closes the exact machine root, but validation and release remain
separate downstream nodes. `M0087-S-BOUNDARY`, `M0087-X-SOURCE`,
`M0087-X-PROVENANCE`, and `M0087-X-TRUST` receive no proof credit here. H0,
R0, full provenance and trust review, hermetic replay, independent verification,
and master acceptance are not claimed.
