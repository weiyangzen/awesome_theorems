# THM-M-1014 validation-phase handoff

Item `S56-M-1014-VALIDATION` is self-tested as provisional worker evidence. The frozen statement,
composition boundary, proof root, and an independently written direct probe elaborate from fresh
temporary source copies. The probe does not import any local THM-M-1014 module.

## Gate results

| Gate | Result | Evidence or boundary |
|---|---|---|
| Narrow kernel replay | pass | All four modules elaborate with Lean 4.29.0. |
| Exact target | pass locally | The proof root and direct probe have the same frozen binders, premise, and pushforward conclusion. |
| Trust observation | provisional pass | The root, direct probe, and terminal declaration report `propext`, `Classical.choice`, and `Quot.sound`. |
| Placeholder/unsafe policy | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the checked modules. |
| Provenance and freshness | pass | Frozen hashes, registry denominator, manifest pin, clean mathlib checkout, terminal source digest, and terminal olean digest agree. |
| Hermetic release replay | fail closed | Canonical warm `.lake` artifacts were reused; no empty-cache offline cold build or release TCB/SBOM archive was produced. |
| Independent runner | fail closed | The independent implementation ran inside this worker with the shared cache; no distinct identity or signed attestation exists. |

## Commands and exact results

Run from base revision `5efc9accb7b7d20411403a280fb058cb19aea566` on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-1014/check_validation.py
  exit 0
  validation: PASS: four frozen modules elaborated from fresh temporary source copies
  validation: PASS: exact proof root and independently written direct probe kernel-check
  validation: PASS: observed axioms are propext, Classical.choice, and Quot.sound
  validation: PASS: frozen hashes, provenance, placeholder policy, and dependency pin passed
  validation: BLOCKED release-only: warm shared .lake is not an empty-cache hermetic replay
  validation: BLOCKED release-only: this worker is not a distinct independent runner

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1014
  exit 0: rank 293, planned, legacy artifacts unaccepted, theorem_complete=false

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
```

No `lake update`, build, clone, fetch, network access, or `.lake` mutation was performed.

## Status boundary

The validation node is self-tested pending master acceptance. This does not establish the
release-only hermetic or distinct-runner gates and grants no `AUDIT-Z`, `THEOREM-Z`, release, H0,
or R0 credit. `audit_complete=false` and `theorem_complete=false` remain mandatory. The first
failed release gate is section 10.6's empty-cache hermetic replay; section 10.7 remains blocked too.
