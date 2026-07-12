# THM-M-1515 validation-phase result

Item `S56-M-1515-VALIDATION` was run against the proof-phase snapshot. The
exact frozen target, analytic proof packages, child-to-root composition, and an
exact-type validation probe elaborate against pinned Lean 4.29.0/mathlib. Lean
reports only `propext`, `Classical.choice`, and `Quot.sound` for every checked
proof and composition declaration. No placeholder, local axiom, or unsafe
declaration was found.

## Exact result

The structured recipe in `validation-spec.json` ran from repository root on
2026-07-12:

```text
python3 Stage1_Instances/THM-M-1515/check_validation.py
  exit 0
  ok: exact frozen target, composition, proof, and exact-type probe elaborated in a fresh temporary module directory
  ok: root and analytic declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, frozen hashes and denominator, toolchain pins, and clean pinned mathlib checks passed
  stale: frozen graph predates proof closure and still reports both analytic packages and root open
  blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` into a fresh temporary directory under `Formalizations/Lean`,
uses `lake env lean` narrowly, and removes the directory and its `.olean` files.
The existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch, or
dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, conditional composition, both analytic packages, root proof, and exact-type probe elaborate. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the four modules. |
| Axiom observation | provisional pass | Every checked declaration reports `propext`, `Classical.choice`, and `Quot.sound`; the complete release TCB inventory is absent. |
| Local provenance | pass | Frozen source hashes, statement/registry identity, denominator, toolchain files, clean mathlib tree, and mathlib revision agree. |
| Root kernel closure | provisional pass | `noether_first_theorem` has the exact frozen target and composes the two local analytic proof bodies through `root_of_derivative_packages`. |
| Structured state freshness | fail closed | The frozen graph predates proof closure and still records `root_closed=false` with both analytic packages open. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake`; no empty-cache cold build, offline restore, complete TCB inventory, SBOM/license archive, or deterministic bundle exists. |
| Independent verification | fail closed | The exact-type probe used the same mutable clone and cache and is not an independently implemented minimal verifier; no distinct runner, identity, signature, or second attestation exists. |

This is truthful provisional worker evidence only. It grants no `E0/E1`,
accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
`audit_complete=false` and `theorem_complete=false`.
