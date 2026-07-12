# THM-M-1270 validation-phase result

Item `S56-M-1270-VALIDATION` was run against the proof-phase snapshot. The narrow kernel,
exact-type, placeholder, dependency-pin, frozen-hash, and local provenance checks pass for the
statement, conditional composition, admitted partial proof bodies, and an independently written
maximality probe. This does not prove Ekeland's principle: `target_of_maximalPoint` still takes the
descent-maximal-point construction as an explicit premise.

## Exact result

The structured recipe in `validation-spec.json` ran from repository root on `2026-07-12`:

```text
python3 Stage1_Instances/THM-M-1270/check_validation.py
  exit 0
  ok: statement, obligation composition, partial proof bodies, and independent probe elaborated in a fresh temporary module directory
  ok: exact ProofTarget-to-frozen-target bridge checked definitionally
  ok: observed axiom output contains only the expected propext, Classical.choice, and Quot.sound set
  ok: placeholder scan, frozen hashes, registry denominator, and clean pinned mathlib checks passed
  open: exact root remains conditional on construction of a descent-maximal point; frozen machine debt is M3
  blocked: cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies the four Lean modules to a fresh temporary directory under
`Formalizations/Lean`, invokes `lake env lean`, and removes all temporary outputs. It reuses the
existing pinned `.lake` artifacts without running update, build, clone, or fetch. It also verifies
that mathlib is clean at `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, obligation composition, partial proof bodies, and independent probe elaborate. |
| Exact target identity | pass | `proofTarget_iff_frozen` is proved by definitional equality between the separately compiled statement and proof modules. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, local `axiom`, `unsafe`, or `sorryAx` occurs in source or kernel output. |
| Axiom observation | provisional pass | Every printed declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`; no release-grade TCB profile is accepted. |
| Local provenance | pass | Frozen statement and registry hashes agree, sources are checked directly, and pinned mathlib is clean. |
| Exact root kernel closure | fail | The proof exposes the unproved maximal-point constructor as `hardCore`; the frozen root remains `M3`. |
| Hermetic release replay | fail closed | No clean checkout, empty-cache cold build, offline restoration, full executable/olean TCB inventory, or SBOM/license closure was available. |
| Independent verification | fail closed | The independent probe used the same worker checkout and shared cache, without a distinct verifier identity or signed second attestation. |

This is a self-tested validation-phase artifact with an honest negative root decision. It grants no
`E0/E1`, `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit. Theorem completion is
false, and the frozen cut set remains the six obligations listed in `typed-graphs.json`.
