# THM-M-0416 validation-phase result

Item `S56-M-0416-VALIDATION` was run against the proof-phase snapshot. The
exact root, checked child composition, a direct independent reconstruction,
the pinned mathlib revision and terminal source file, local placeholder scan,
and observed axiom set all pass the narrow worker validation.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root
on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0416/check_validation.py
  exit 0
  ok: exact root and independent reconstruction elaborate in a fresh temporary module directory
  ok: composition, proof root, and independent root report only propext, Classical.choice, and Quot.sound
  ok: frozen hashes, placeholder scan, clean pinned mathlib, and terminal source provenance checks passed
  blocked: release-grade cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies all four Lean modules into a fresh temporary directory
under `Formalizations/Lean`, elaborates them with `lake env lean`, and deletes
the directory. It checks mathlib is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch,
or dependency mutation is performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel root | pass provisionally | `Proof.dirichletUnitTheorem` elaborates at the frozen target type. |
| Composition | pass provisionally | `ObligationTree.root_of_packages` elaborates and reports its axiom closure. |
| Independent local proof | pass provisionally | `Validation.independentDirichletUnitTheorem` reconstructs the root directly without importing `Proof` or `ObligationTree`. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs in the four checked modules. |
| Trust observation | pass locally | All three root-relevant axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; this is not a complete release TCB inventory. |
| Pinned provenance | pass locally | The mathlib checkout is clean at the manifest pin, and the terminal source file hash plus four source declaration boundaries are checked. |
| Hermetic release replay | fail closed | The run reused warm `.lake` artifacts; it did not use a clean checkout with empty caches or test offline archive restoration and SBOM/licenses. |
| Independent release verification | fail closed | The alternate proof ran in the same clone and cache, without a distinct runner identity, second signature, or independently implemented release verifier. |

This validation node is genuinely self-tested, but the receipt is explicitly
nonrelease and provisional. It grants no `E0/E1`, `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, release, or master-acceptance credit. The machine root cut set is
empty for the checked proof snapshot; the release cut set remains hermetic
reproduction, full provenance/TCB and supply-chain closure, distinct-runner
verification, independent source/readability reviews, and master acceptance.
