# THM-M-0644 proof-phase validation

Item: `S56-M-0644-PROOF`. Base revision:
`78890c5f1b62587a2048303f2f011e6049a50559`.

## Implemented proof

`Proof.lean` provides the exact frozen compactness theorem, not a weakened substitute. The forward
direction invokes satisfiability monotonicity. The backward direction pins the exact theorem in
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, whose audited terminal body constructs an
ultraproduct over finite subtheories. A local root declaration composes the two explicit directions.

Lean elaborated all three declarations and reported exactly `propext`, `Classical.choice`, and
`Quot.sound`. No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs in the proof module.
This closes the proof-body deliverable provisionally; it does not claim validation, release, master
acceptance, H0/R0, hermetic replay, independent verification, or theorem completion.

## Commands and results

All commands ran on 2026-07-12 in this worker clone. The existing pinned `.lake` artifacts were
reused without update, build, clone, fetch, or mutation.

```text
cd Formalizations/Lean
lake env lean ../../Stage1_Instances/THM-M-0644/Proof.lean
  exit 0: exact root and both directions elaborated; all three axiom reports were
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0644/check_proof.py
  exit 0: exact root and both directions present; no prohibited device

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0644
  exit 0: rank 690, planned, theorem_complete=false

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0644/Proof.lean
  exit 1 with empty output: expected no-match status

git diff --check -- Stage1_Instances/THM-M-0644 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The next root cut is the validation phase, followed by release and master acceptance.
