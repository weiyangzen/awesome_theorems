# THM-M-0133 validation-phase result

Item `S56-M-0133-VALIDATION` was run against the integrated proof-phase snapshot. The narrow kernel,
source-hygiene, frozen-input, dependency-pin, and local provenance checks pass for the exact FLT
statement, the exponent-four proof, and the conditional root composition. This does not prove
Fermat's Last Theorem: both composition declarations consume the still-unproved all-odd-prime
exponent family.

## Exact result

The structured recipe in `validation-spec.json` was run from the worker clone on 2026-07-12
(Asia/Shanghai):

```text
python3 Stage1_Instances/THM-M-0133/check_validation.py
  exit 0
  validation ok: exact target and admitted conditional proof bodies re-elaborated
  validation ok: source hygiene, frozen hashes, and clean pinned mathlib checks passed
  root open: all-odd-prime premise remains; cut set M0133-L-MOD and M0133-L-LOWER
  blocked: cold hermetic replay and distinct-runner independent verification
```

The validator invokes `lake env lean` narrowly and copies the Lean modules into a fresh temporary
directory under `Formalizations/Lean`. Temporary compiled output is removed with that directory. It
checks that the existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch, or dependency mutation
was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborate against pinned Lean 4.29.0/mathlib. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the checked modules. |
| Axiom observation | provisional pass | Checked declarations report only `propext`, `Classical.choice`, and `Quot.sound`; the release foundation/TCB closure remains incomplete. |
| Local provenance | pass | Statement, registry, graph, audit, spec, and proof hashes are bound into the receipt; mathlib is at the pinned clean revision. |
| Exact root kernel closure | fail | `root_compose` and `exactTarget_of_oddPrimeCases` are conditional on all odd-prime exponent cases. The frozen cut is `M0133-L-MOD` and `M0133-L-LOWER`. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake` artifacts; no clean checkout, empty-cache cold build, offline restoration, SBOM/license closure, or complete executable/olean TCB inventory was available. |
| Independent verification | fail closed | This is one worker in one mutable clone, without a distinct independently provisioned runner, second signed attestation, or independently implemented release verifier. |

Additional preflight and structural checks also passed: `check_stage1_standard.py`, target manifest
validation, target lookup, `check_statement.py`, `check_anchor_audit.py`,
`check_obligation_tree.py`, and `check_proof.py`. Exact command results are preserved in the worker
self-test manifest.

This is a truthful negative theorem-validation result and positive self-test of the validation
phase. It grants no `M0-*`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release, independent-verification,
or master-acceptance credit. The root remains `M2` and `theorem_complete=false`.
