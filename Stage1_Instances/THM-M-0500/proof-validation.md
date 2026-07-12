# THM-M-0500 proof-phase validation

Item: `S56-M-0500-PROOF`. Base revision:
`e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`.

## Implemented body

`Proof.lean` defines the frozen target verbatim and proves it with the exact proof-bearing
`Nat.infinite_setOf_prime_and_eq_mod` declaration from mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pinned terminal source is
`Mathlib/NumberTheory/LSeries/PrimesInAP.lean`, SHA-256
`d99edfb234cc2c044332951a16f32bbfad58c8c73cc51faf4e9219d3bc6684c2`. Its body discharges the
frozen non-summability and support cut and the finite-support assembly; the repo-local wrapper has
no premise and does not weaken or substitute the target.

Both upstream and wrapper declarations report exactly `propext`, `Classical.choice`, and
`Quot.sound`. No placeholder, custom axiom, unsafe declaration, oracle, or moving dependency is
used. This is proof-phase evidence only. Validation, release, H0/R0, hermetic and independent
replay, master acceptance, and theorem completion remain open.

## Commands and results

Validation ran on 2026-07-12 (Asia/Shanghai), reusing the pre-existing canonical pinned `.lake`
symlink. No `lake update`, build, clone, fetch, or network action was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0500
  exit 0: rank 877, planned, L0/rework_required, theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0500/Proof.lean
  exit 0: exact root elaborated; upstream and wrapper axioms were
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0500/check_proof.py
  exit 0: exact proof fragments, input hashes, receipt boundary, and no-completion claim passed

python3 Stage1_Instances/THM-M-0500/check_obligation_tree.py
  exit 0: 14 frozen obligations, 26 typed edges, and exact denominator passed; this earlier freeze
  artifact truthfully retains its pre-proof M3 status overlay

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|sorryAx' \
  Stage1_Instances/THM-M-0500 -g '*.lean'
  exit 1: expected no-match result

git diff --check -- Stage1_Instances/THM-M-0500 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The node-specific provisional receipt is `proof-receipt.json`. Only the integration lane can
accept it.
