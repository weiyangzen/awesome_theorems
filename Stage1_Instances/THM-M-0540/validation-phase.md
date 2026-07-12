# THM-M-0540 validation-phase result

Item `S56-M-0540-VALIDATION` was run against the integrated proof-phase snapshot. The narrow
kernel, trust observation, placeholder, dependency-pin, local receipt linkage, and terminal-source
provenance gates pass for the exact frozen construction target. The exact root re-elaborates from
the local `rfl` terminal body and explicit child-to-root composition.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0540/check_validation.py
  exit 0
  ok: exact statement, conditional composition, terminal equation, and root replayed with fresh temporary outputs
  ok: checked proof and composition declarations report exactly propext, Classical.choice, and Quot.sound
  ok: placeholder scan, receipt/hash linkage, frozen denominator, pinned clean mathlib, and terminal source provenance passed
  blocked: shared warm .lake artifacts are not a cold empty-cache hermetic release replay
  blocked: this single mutable worker is not a distinct independently provisioned verifier
  open: H0, R0, AUDIT-Z, THEOREM-Z, release, and master acceptance
```

The validator copies `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` into a fresh temporary
directory under `Formalizations/Lean`, emits `.olean` outputs only there, and removes the directory.
It checks the automation-provided shared mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch, or dependency mutation
is performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, conditional composition, terminal equation, and root elaborate against pinned Lean 4.29.0/mathlib with fresh temporary outputs. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the three checked modules. |
| Axiom observation | provisional pass | The printed declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`, matching the proof receipt. This is not a complete release TCB audit. |
| Local provenance | pass | Statement/proof receipt hashes, frozen denominator, toolchain/manifest hashes, clean mathlib pin, exact source hash, and the body shape of `singularHomologyFunctor` agree. |
| Exact root kernel closure | pass provisionally | `integralSingularHomology_eq_homology` consumes the locally checked `unfoldingEquation`; all six frozen machine obligations are listed in the bound proof receipt. Master acceptance remains absent. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake` artifacts; it did not perform a clean checkout, empty-cache cold build, offline restoration, complete TCB/SBOM/license closure, or deterministic release bundle build. |
| Independent verification | fail closed | This is one mutable worker clone without a distinct verifier identity, independently provisioned clean runner, second signed attestation, or independently implemented minimal verifier. |

This is a self-tested validation-phase handoff, not theorem completion. `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, release, and master acceptance remain open; the authoritative pre-proof structured graph
may be reconciled only by the integration lane after accepting the receipts.
