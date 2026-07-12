# THM-M-0982 validation-phase result

Item `S56-M-0982-VALIDATION` was run against the proof-phase snapshot. The
exact frozen root re-elaborates, its local wrapper reports only the expected
Lean foundation axioms, the pinned mathlib source and revision agree with the
audited provenance, and a separately implemented Lean declaration reconstructs
the exact target without calling the proof-phase wrapper.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root
on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0982/check_validation.py
  exit 0
  ok: exact statement and proof-phase root elaborated against the clean pinned mathlib revision
  ok: exact-type replay and separately implemented same-workspace reconstruction both passed
  ok: machine-reported axiom set is propext, Classical.choice, and Quot.sound; no sorryAx
  ok: placeholder/unsafe scan, frozen statement/registry hashes, and terminal source provenance passed
  blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies `Statement.lean`, `Proof.lean`, and `Validation.lean` to a
fresh temporary module directory beneath `Formalizations/Lean`, invokes only
`lake env lean`, and removes that directory afterward. It verifies that the
existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch,
or dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, proof root, exact-type replay, and separate reconstruction elaborate with pinned Lean 4.29.0/mathlib. |
| Placeholder and unsafe gate | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the checked modules or kernel output. |
| Axiom observation | provisional pass | All five reported proof/validation declarations use only `propext`, `Classical.choice`, and `Quot.sound`. Full transitive release trust closure remains absent. |
| Provenance gate | provisional pass | Statement and frozen-registry hashes agree; mathlib is clean at the pinned revision; both terminal theorem bodies and the audited source hash are present. |
| Exact root kernel closure | pass pending master | `Proof.probabilityContinuity` has exactly `ProbabilityContinuityTarget`, and the independent probe reconstructs the same conjunction. |
| Hermetic release replay | fail closed | The run reused shared warm `.lake` artifacts; there was no immutable clean checkout, empty-cache cold build, offline restoration, SBOM/license closure, or complete executable/compiled-artifact TCB inventory. |
| Independent verification | fail closed | The separate implementation ran in the same worker and cache, without a distinct identity, independently provisioned runner, second signed attestation, or minimal release-bundle verifier. |

This is truthful provisional validation evidence, not a theorem-completion
claim. Human-source `H0`, readable `R0`, full hermetic and independent gates,
deterministic release evidence, and master acceptance remain open. The
structured receipt is `validation-receipt.json`.
