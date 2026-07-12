# THM-M-1268 validation-phase result

Item: `S56-M-1268-VALIDATION`. Base revision:
`d106a271df55889c00fab33c3ecbdcc7f1d21bd1`. Validation date: 2026-07-12.

The exact frozen statement, frozen conditional composition, local proof, exact statement wrapper,
and a separately implemented exact-root probe all elaborate with pinned Lean 4.29.0 and mathlib
`8a178386`. `Validation.lean` deliberately does not import `Proof`; it independently reconstructs
convex sublevels, weak closedness, both topology directions, and the exact root.

## Commands and exact results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1268
  exit 0: rank 444; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-1268/check_validation.py
  exit 0: fresh temporary elaboration of Statement, ObligationTree, Proof, ProofExact, and
  Validation passed; checked declarations reported exactly propext, Classical.choice, and
  Quot.sound; placeholder, hash, denominator, pin, and mathlib-cleanliness checks passed
```

The validator uses only narrow `lake env lean` invocations. It copies inputs into a fresh temporary
directory under `Formalizations/Lean`, writes temporary oleans there, and removes the directory. It
does not run Lake update/build, fetch or clone dependencies, use the network, or modify `.lake`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, composition, proof, wrapper, and independent reconstruction elaborate. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in checked code. |
| Trust observation | provisional pass | Root-relevant declarations report only `propext`, `Classical.choice`, and `Quot.sound`; release TCB acceptance is not inferred. |
| Local provenance | pass | Frozen hashes and denominator agree; mathlib is clean at the manifest pin; two material support-source hashes agree with the anchor audit. |
| Same-clone independent reconstruction | pass with boundary | The validation probe does not import `Proof` and separately proves the exact root, but is not a distinct runner. |
| Authoritative structured state | fail closed | The frozen graph predates proof work and retains the three proof bridges in its root cut. Workers cannot reconcile master state. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; no clean immutable empty-cache build, offline restoration, complete TCB/SBOM, or deterministic bundle exists. |
| Independent verification | fail closed | No distinct verifier identity, independently provisioned runner, second signature, or protected result exists. |

This is provisional worker validation. `audit_complete=false` and `theorem_complete=false`; H0/R0,
authoritative state reconciliation, hermetic release, distinct-runner verification, release, and
master acceptance remain open.
