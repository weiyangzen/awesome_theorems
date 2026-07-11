# THM-M-0183 validation-phase result

Item `S56-M-0183-VALIDATION` was validated fail-closed against the integrated proof-phase
snapshot. Narrow kernel, trust-observation, local provenance, placeholder, and dependency-pin
checks pass. The positive theorem gate fails: `Proof.lean` kernel-checks the exact negation of the
frozen target by instantiating its universally quantified metric interface with an empty carrier.

## Exact result

Run from the worker clone on 2026-07-12 without update, build, fetch, clone, or dependency mutation:

```text
python3 Stage1_Instances/THM-M-0183/check_validation.py
  exit 0
  ok: exact frozen target and checked countermodel elaborated in a fresh temporary module directory
  ok: countermodel reports only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, source hashes, registry denominator, and clean pinned mathlib checks passed
  blocked: the exact positive target is refuted by the empty metric-interface countermodel
  blocked: cold hermetic replay, full TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies `Statement.lean` and `Proof.lean` into a fresh temporary directory, invokes
`lake env lean`, then removes all temporary outputs. It checks the pinned Lean 4.29.0 manifest and
clean mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact target and `not_yauCalabiConjectureTarget` elaborate from copied sources. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` occurs in the three Lean modules. |
| Axiom observation | provisional pass | The negation uses `propext`, `Classical.choice`, and `Quot.sound`; no release-grade TCB profile is claimed. |
| Local provenance | pass | Statement/registry hashes, graph denominator, toolchain manifest, and clean mathlib pin agree. |
| Exact positive root | fail | The frozen proposition quantifies over arbitrary `KahlerMetricInterface`, including one whose metric type is empty. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; no cold empty-cache offline rebuild, SBOM/license closure, or complete TCB inventory exists. |
| Independent verification | fail closed | One mutable worker clone is not a second identity, independently provisioned runner, signed attestation pair, or independent verifier. |

This receipt is truthful negative validation evidence only. It grants no `M0-*`, `E0/E1`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance. The first failed theorem
gate is exact-target consistency. The statement must be repaired so metric existence is intrinsic
to the geometric structure, then statement, obligation, proof, and validation phases must rerun.
