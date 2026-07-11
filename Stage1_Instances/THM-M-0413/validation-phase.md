# THM-M-0413 validation-phase result

Item `S56-M-0413-VALIDATION` was run against the proof-phase snapshot. Narrow kernel replay,
exact-root checking, placeholder scanning, frozen-input provenance, and the pinned dependency check
pass. `Validation.lean` independently reconstructs the exact target without importing `Proof.lean`.

## Exact result

Run from repository root on 2026-07-12 (local time):

```text
$ python3 Stage1_Instances/THM-M-0413/check_validation.py
exit 0
ok: four frozen/narrow modules elaborated from fresh temporary source copies
ok: exact root, component assembly, and independently written exact-type probe checked
ok: observed axioms are propext, Classical.choice, and Quot.sound
ok: frozen hashes, registry denominator, placeholder scan, and clean pinned mathlib passed
blocked: warm shared .lake cache is not an empty-cache hermetic release replay
blocked: one mutable worker is not a distinct independently provisioned verifier
```

The validator uses `lake env lean` and copies each Lean input into a new temporary source directory
under `Formalizations/Lean`, then removes it. It does not update, build, clone, fetch, or modify the
pinned `.lake` dependency state.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Statement, conditional composition, both exact-root proof routes, and the independent local probe elaborate. |
| Exact target | pass locally | All three root declarations have the frozen quantified `IsDedekindDomain (RingOfIntegers K)` target. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the four checked modules. |
| Axiom observation | provisional pass | Checked declarations report `propext`, `Classical.choice`, and `Quot.sound`; this is not a complete accepted TCB closure. |
| Local provenance | pass | Frozen source and registry hashes agree; mathlib source is clean at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; no empty-cache cold build, offline restoration, full TCB/SBOM/license closure, or second platform exists. |
| Independent verification | fail closed | The independently written probe still ran in this mutable worker with the shared cache; there is no distinct identity, runner, signature, or independently provisioned minimal verifier. |

This is a self-tested validation-node handoff, not theorem completion. It grants no `E0/E1`,
`M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit. The first failed release gate
is section 10.6's hermetic cold replay, followed by section 10.7 independent verification.
