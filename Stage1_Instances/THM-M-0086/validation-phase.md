# THM-M-0086 validation-phase result

Item: `S56-M-0086-VALIDATION`. Base revision:
`bfd4cfb5d8531f2811d838fd96c0347715208d75`.

The exact frozen statement and proof root elaborate in a fresh temporary target directory against
pinned Lean 4.29.0 and mathlib `8a178386`. `Validation.lean` independently reconstructs the exact
three-branch root by importing only `Statement.lean` and invoking the three pinned terminal
declarations directly. Both roots report only `propext`, `Classical.choice`, and `Quot.sound`.

## Commands and exact results

All commands ran on 2026-07-12. No Lake update/build, dependency clone/fetch, network access, or
`.lake` modification was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0086
  exit 0: execution rank 134; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0086/check_validation.py
  exit 0: fresh temporary statement/proof/validation elaboration passed; independent exact-root
  reconstruction passed; hashes, placeholder/unsafe hygiene, registry denominator, mathlib pin,
  terminal source identities, and dependency cleanliness passed; observed axioms were propext,
  Classical.choice, and Quot.sound

git diff --check -- Stage1_Instances/THM-M-0086 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The validator copies sources to a fresh temporary directory under `Formalizations/Lean`, emits only
a target-local `Statement.olean`, and removes the directory automatically. It reads the pinned warm
dependency cache without writing to it.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, proof root, and independent exact root elaborate. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in checked code. |
| Axiom observation | provisional pass | Both roots report only `propext`, `Classical.choice`, and `Quot.sound`; full release TCB acceptance is not inferred. |
| Local provenance | pass | Frozen hashes agree; mathlib is clean at the manifest pin; both terminal source hashes and all declaration markers agree with the anchor audit. |
| Same-clone independent reconstruction | pass with boundary | `Validation.lean` reaches the exact target without importing proof-phase code, but this is not a distinct runner. |
| Authoritative structured state | fail closed | The frozen graph predates `Proof.lean` and still reports the three terminal proof leaves open. Workers cannot reconcile master state. |
| Human source/readability | fail closed | The dossier remains H2/R4 and lacks independently accepted H0/R0 reviews. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; no clean checkout, empty-cache build, offline restoration, complete TCB/SBOM, or deterministic bundle exists. |
| Independent verification | fail closed | No distinct verifier identity, independently provisioned runner, second signature, or protected CI result exists. |

This is truthful provisional worker validation, not theorem completion. `audit_complete` and
`theorem_complete` remain false; authoritative reconciliation, H0/R0, hermetic release, distinct-
runner verification, release, and master acceptance remain open.
