# THM-M-0418 validation-phase result

Item `S56-M-0418-VALIDATION` was run against the proof-phase snapshot. The
exact root, checked composition, a separately implemented reconstruction, the
pinned mathlib revision and terminal source file, local placeholder scan, and
observed axiom set pass the narrow worker validation.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root
on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0418/check_validation.py
  exit 0
  ok: exact root and separate reconstruction elaborate in a fresh temporary module directory
  ok: composition, proof root, and separate root report only propext, Classical.choice, and Quot.sound
  ok: frozen hashes, placeholder scan, clean pinned mathlib, and terminal source provenance checks passed
  blocked: release-grade cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies all four Lean modules into a fresh temporary directory
under `Formalizations/Lean`, elaborates them with `lake env lean`, and deletes
the directory. It checks mathlib is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch,
network access, or dependency mutation is performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel root | pass provisionally | `minkowskiIdealClassBound_proof` elaborates at the frozen target type. |
| Composition | pass provisionally | `minkowskiIdealClassBound_obligationRoot` elaborates and reports its axiom closure. |
| Separate local proof | pass provisionally | `Validation.independentMinkowskiIdealClassBound` reconstructs the root directly without importing `Proof` or `ObligationTree`. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the four checked modules. |
| Trust observation | pass locally | All three root-relevant axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; this is not a complete release TCB inventory. |
| Pinned provenance | pass locally | The mathlib checkout is clean at the manifest pin, and the terminal source file hash plus declaration boundary are checked. |
| Hermetic release replay | fail closed | The run reused warm `.lake` artifacts; it did not use a clean checkout with empty caches or test offline archive restoration and SBOM/licenses. |
| Independent release verification | fail closed | The alternate proof ran in the same clone and cache, without a distinct runner identity, second signature, or independently implemented release verifier. |

This validation node is genuinely self-tested, but the receipt is explicitly
nonrelease and provisional. It grants no `E0/E1`, `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, release, or master-acceptance credit. The machine root cut set is
empty for the checked proof snapshot; the release cut set remains hermetic
reproduction, full provenance/TCB and supply-chain closure, distinct-runner
verification, independent source/readability reviews, and master acceptance.
