# THM-M-0644 validation-phase result

Item: `S56-M-0644-VALIDATION`. Base revision:
`2a03bdcf79ff75231863756bd712861e43349b06`.

The exact local compactness root and an independently written direct probe both elaborate against
the pinned mathlib terminal declaration. Both report exactly `propext`, `Classical.choice`, and
`Quot.sound`. The verifier confirms proof-receipt freshness, canonical registry/graph identity, a
clean mathlib checkout at the manifest revision, local placeholder policy, and terminal source and
compiled-artifact provenance.

## Commands and results

All commands ran on 2026-07-12 in this worker clone. Existing pinned `.lake` artifacts were reused;
no update, build, clone, fetch, or dependency mutation was performed.

```text
cd Formalizations/Lean
lake env lean ../../Stage1_Instances/THM-M-0644/Proof.lean
  exit 0: exact root and both directions elaborated; all three declarations reported
  [propext, Classical.choice, Quot.sound]

lake env lean ../../Stage1_Instances/THM-M-0644/Validation.lean
  exit 0: direct independent root elaborated; terminal and independent root reported
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0644/check_validation.py
  exit 0: fresh proof inputs, canonical graph identity, clean pinned dependency, and
  placeholder policy; source SHA-256 0abb92d5...43edb; olean SHA-256 56f4ca80...a9b

python3 Stage1_Instances/THM-M-0644/check_proof.py
  exit 0: exact root and both directions present; no prohibited device

python3 Stage1_Instances/THM-M-0644/check_obligation_tree.py
  exit 0: 16 obligations, 45 typed edges, denominator hash valid; frozen root state remains open

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0644
  exit 0: rank 690, planned, theorem_complete=false
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Proof wrapper and direct validation probe elaborate against pinned Lean 4.29.0/mathlib. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs on the checked local surface. |
| Trust observation | provisional pass | Both root routes report only the three declared classical/kernel axioms. Full release TCB closure is absent. |
| Provenance and freshness | pass | Proof receipt hashes agree; mathlib is clean and pinned; terminal source and olean hashes are recorded. |
| Authoritative graph reconciliation | master-only | The frozen graph still says the root is open because it predates proof acceptance. |
| Hermetic release replay | fail closed | Shared warm writable artifacts were reused; no cold empty-cache offline replay or SBOM/license closure occurred. |
| Independent verification | fail closed | The separate probe ran in this same clone/cache, not a distinct signed runner. |

This is provisional validation-phase evidence, not release evidence. `audit_complete=false` and
`theorem_complete=false`; H0/R0, release, and master acceptance remain open.
