# THM-M-0001 validation-phase result

Item `S56-M-0001-VALIDATION` was run against the proof-phase snapshot. The
exact frozen target, canonical proof, child-to-root composition, and a separately
implemented local reconstruction elaborate against pinned Lean 4.29.0/mathlib.
Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for the root
wrappers and terminal exactness declarations. No placeholder, local axiom, or
unsafe declaration was found.

## Exact result

The structured recipe in `validation-spec.json` ran from repository root on
2026-07-12:

```text
python3 Stage1_Instances/THM-M-0001/check_validation.py
  exit 0
  ok: exact proof and independently reconstructed wrapper elaborated in a fresh temporary module directory
  ok: root and terminal declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, proof-receipt hashes, frozen denominator, and clean pinned mathlib checks passed
  stale: frozen graph predates proof closure and still reports the three exactness leaves open
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
| Narrow kernel replay | pass | Exact statement, composition, proof, and independent local reconstruction elaborate. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration in the four modules. |
| Axiom observation | provisional pass | Root wrappers and terminal exactness declarations report `propext`, `Classical.choice`, and `Quot.sound`. |
| Local provenance | pass | Proof-receipt source hashes, frozen denominator, mathlib revision/source hash, and clean dependency tree agree. |
| Root kernel closure | provisional pass | Both root wrappers close the exact frozen target; the proof receipt identifies the three exactness bodies. |
| Structured state freshness | fail closed | The frozen graph predates proof closure and still records `root_closed=false` with the three exactness leaves open. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake`; no empty-cache cold build, offline restore, complete TCB inventory, or SBOM exists. |
| Independent verification | fail closed | The independent implementation used this same worker checkout/cache; no distinct runner, identity, signature, or second attestation exists. |

This is truthful provisional worker evidence only. It grants no `E0/E1`,
accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
`audit_complete=false` and `theorem_complete=false`.
