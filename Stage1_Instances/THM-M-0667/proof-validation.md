# THM-M-0667 proof-phase validation

Item: `S56-M-0667-PROOF`. Base revision:
`d4da54fa4b81642d3c351d58820f005903bbe09e`.

## Implemented body

`Proof.lean` closes the exact frozen root `Not (Primrec₂ Nat.ack)` with a
repo-local wrapper around `Nat.not_primrec₂_ack` from the existing pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The upstream terminal
body derives primitive recursiveness of the diagonal from a hypothetical
binary proof and contradicts `not_primrec_ack_self`; that result is backed by
the constructor induction in `exists_lt_ack_of_nat_primrec`.

The terminal body is dependency source, not copied into this target. Its
source SHA-256 is
`02135d74dcfe97d8ad95402d224be3979babc6e69c2a2b6f2ad06c9fc2f17578`.
This classification is `local_wrapper_upstream_pinned`, not a repo-local
vendored proof body.

## Commands and results

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No update, build, fetch, clone, or `.lake` mutation was
performed.

```text
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0667
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" Proof.lean
rm -f Statement.olean
  exit 0
  ackermannNondefinability : AckermannNondefinabilityTarget
  depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0667
  exit 0: rank 711, planned, theorem_complete false
```

Proof-phase root closure is genuine but is not theorem completion. The source,
trust/provenance, hermetic validation, readable reconstruction, independent
verification, release, and master-acceptance gates remain outside this phase.
