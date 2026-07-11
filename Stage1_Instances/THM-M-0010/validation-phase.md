# THM-M-0010 validation-phase result

Item `S56-M-0010-VALIDATION` was run against the proof-phase snapshot. The
exact frozen target, conditional composition probe, canonical proof, and a
separately written local reconstruction elaborate against pinned Lean
4.29.0/mathlib. Lean reports only `propext`, `Classical.choice`, and
`Quot.sound`. No placeholder, local axiom, or unsafe declaration was found.

## Exact result

The structured recipe ran from repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0010/check_validation.py
  exit 0
  PASS THM-M-0010 narrow validation
  kernel: exact proof, composition probe, and independently written exact-target probe elaborated
  trust: reported axioms are within propext, Classical.choice, Quot.sound
  provenance: proof receipt hashes, frozen denominator, and clean pinned mathlib source agree
  hygiene: no local sorry/admit/axiom/unsafe token
  stale: frozen typed graph predates proof closure and still reports root_closed=false
  blocked: warm shared cache; cold hermetic replay and distinct-runner verification remain open
```

The validator copies the four Lean modules into a fresh temporary directory
under `Formalizations/Lean`, invokes only `lake env lean`, and removes the
directory and generated `.olean`. The existing mathlib checkout is clean and
pinned at `8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build,
clone, fetch, or dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, composition, proof, and independent local reconstruction elaborate. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration in the four modules. |
| Axiom observation | provisional pass | All three checked declarations report only `propext`, `Classical.choice`, and `Quot.sound`. |
| Local provenance | pass | Proof-receipt source hashes, frozen denominator, mathlib revision/source hash, and clean dependency tree agree. |
| Root kernel closure | provisional pass | Both root wrappers close the exact frozen target. |
| Structured state freshness | fail closed | The frozen graph predates proof closure and still records `root_closed=false`. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake`; no empty-cache cold build, offline restore, complete TCB inventory, or SBOM exists. |
| Independent verification | fail closed | The independent implementation used this same worker checkout/cache; no distinct runner, identity, signature, or second attestation exists. |

This is truthful provisional worker evidence only. It grants no `E0/E1`,
accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
`audit_complete=false` and `theorem_complete=false`.
