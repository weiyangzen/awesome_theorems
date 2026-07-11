# THM-M-0082 validation-phase result

Item `S56-M-0082-VALIDATION` was run against base revision
`a6425da42e4fd63ec88cf4a2ce9b2facf0d32b33`. The exact frozen statement,
obligation composition, proof-phase bridge/root, and an independently
implemented exact-root probe all elaborate against pinned Lean 4.29.0 and
mathlib `8a178386`. The independent probe imports only `Statement.lean` and
invokes the upstream declaration directly rather than reusing the proof
wrapper or `root_of_bridge`.

## Commands and exact results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0082
  exit 0: execution rank 135; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0082/check_validation.py
  exit 0: fresh temporary Statement/ObligationTree/Proof/Validation
  elaboration passed; independent exact-root reconstruction passed; hashes,
  placeholder/unsafe scan, registry denominator, mathlib pin, source identity,
  and dependency cleanliness passed; observed axioms were propext,
  Classical.choice, and Quot.sound

git diff --check -- Stage1_Instances/THM-M-0082
  exit 0: no output
```

The validator invokes only narrow `lake env lean` elaborations. It copies the
four modules into a fresh temporary module tree under `Formalizations/Lean`,
writes `.olean` files only there, and removes that tree. It did not run Lake
update/build, fetch, clone, or modify `.lake`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, composition, bridge/root proof, and independent probe elaborate. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in checked code. |
| Axiom observation | provisional pass | All proof declarations report only `propext`, `Classical.choice`, and `Quot.sound`; no release TCB acceptance is inferred. |
| Local provenance | pass | Frozen hashes agree; mathlib is clean at the manifest pin; the terminal source hash and declaration body markers agree with the anchor audit. |
| Same-clone independent reconstruction | pass with boundary | `Validation.lean` reaches the exact target directly without importing proof-phase code. This is not a distinct runner. |
| Authoritative structured state | fail closed | The frozen graph predates `Proof.lean` and still reports `M0082-X-BRIDGE` open. Workers cannot reconcile master state. |
| Human source/readability | fail closed | The dossier remains H2 and lacks independently accepted H0/R0 reviews. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; no clean checkout, empty-cache build, offline restoration, complete TCB/SBOM, or deterministic bundle exists. |
| Independent verification | fail closed | No distinct verifier identity, independently provisioned runner, second signature, or protected CI result exists. |

This is truthful provisional worker validation, not completion. Both
`audit_complete` and `theorem_complete` remain false; reconciliation, H0/R0,
hermetic release, distinct-runner verification, release, and master acceptance
remain open.
