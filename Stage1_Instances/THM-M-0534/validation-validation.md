# THM-M-0534 validation-phase result

Item `S56-M-0534-VALIDATION` was validated against the integrated proof-phase
snapshot at base revision `1ac55f7931193041e713b9f32687bf61525e9331` on
2026-07-12. The exact proof root and its frozen composition route elaborate in
an isolated temporary module directory. `Validation.lean` independently
reconstructs the same frozen proposition without importing `Proof.lean` or
`ObligationTree.lean`.

All three checked roots terminate at pinned mathlib's
`ShortExact.homology_exact1`, `homology_exact2`, and `homology_exact3` family.
Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`,
`admit`, local axiom, unsafe declaration, or oracle is present in the checked
target modules, and the directly audited mathlib source is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Structured command result

The recorded recipe was run from the repository root:

```text
python3 Stage1_Instances/THM-M-0534/check_validation.py
  exit 0
  PASS S56-M-0534-VALIDATION: exact proof and independent root reconstruction kernel-replayed
  PASS pinned clean mathlib source, source hashes, placeholder policy, and classical axiom observation
  FAIL-CLOSED authoritative graph freshness, cold hermetic replay, complete transitive TCB/provenance, and distinct-runner independence remain open
```

The validator obtains the existing executable through `lake env`, copies
`Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean`
into a fresh temporary directory under `Formalizations/Lean`, writes temporary
oleans only there, and removes the directory. It checks all receipt-bound input
hashes, structured recipe fields, statement/registry identity, the frozen
denominator, the clean dependency pin, the direct terminal source hash,
placeholder policy, and exact axiom output. No update, build, dependency
clone/fetch, network request, or `.lake` mutation is performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact direct root, composition route, and independent exact root elaborate with pinned Lean 4.29.0/mathlib. |
| Placeholder and unsafe scan | pass | Target modules and the directly audited mathlib terminal source contain no prohibited mechanism. |
| Axiom observation | provisional pass | All checked root declarations report `propext`, `Classical.choice`, and `Quot.sound`. |
| Local provenance | provisional pass | Source and dependency hashes and the clean immutable mathlib revision agree; complete transitive declaration/body and compiled-artifact closure is not inventoried. |
| Structured state freshness | fail closed | `typed-graphs.json` is intentionally the pre-proof frozen snapshot and still records `root_closed=false` and `M1`; a worker may not rewrite master state. |
| Dependency acceptance | fail closed | `S56-M-0534-PROOF` has a provisional worker receipt but no master acceptance established in this clone. |
| Hermetic reproduction | fail closed | This run reused the shared warm `.lake` symlink; it is not an empty-cache cold build, network-isolated verification, or offline restoration. |
| Independent verification | fail closed | The independently written Lean probe ran in this same mutable checkout and shared cache, without a second identity, clean runner, signature, or independent release verifier. |

This is truthful provisional validation evidence, not release evidence. It
does not grant `E0/E1`, accepted `M0-W`, `AUDIT-Z`, `THEOREM-Z`, release, or
master acceptance. `audit_complete=false` and `theorem_complete=false` remain
mandatory. The first failed node gate is proof-dependency master acceptance;
the first failed release gate is cold hermetic replay.
