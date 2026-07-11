# THM-M-0088 validation-phase result

Item `S56-M-0088-VALIDATION` was run against the proof-phase snapshot. The exact frozen target,
local proof, checked composition constructor, and a proof-independent direct use of the pinned
mathlib anchor elaborate with Lean 4.29.0. Lean reports only `propext`, `Classical.choice`, and
`Quot.sound` for the checked declarations. No placeholder, local axiom, or unsafe declaration was
found.

## Exact result

The structured recipe in `validation-spec.json` ran from repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0088/check_validation.py
  exit 0
  ok: exact local proof and proof-independent pinned anchor elaborated in a fresh temporary module directory
  ok: root, composition, and anchor declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, proof-receipt hashes, frozen denominator, and clean pinned mathlib checks passed
  stale: frozen graph predates proof closure and still reports three machine obligations open
  blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean`
into a fresh temporary directory, uses `lake env lean` narrowly, and removes the directory and its
`.olean` files. The existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; its tree and Yoneda source hash also agree with the
record. No update, build, clone, fetch, network access, or dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, composition constructor, local proof, and proof-independent anchor elaborate. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration in the four modules. |
| Axiom observation | provisional pass | Checked declarations report `propext`, `Classical.choice`, and `Quot.sound`. |
| Local provenance | pass | Proof receipt hashes, frozen denominator, mathlib revision/tree/source hash, and clean dependency tree agree. |
| Root kernel closure | provisional pass | The local proof and independent pinned anchor both inhabit the exact frozen data-valued target. |
| Structured state freshness | fail closed | The frozen graph predates proof closure and still records `root_closed=false` with three obligations open. |
| Human source and readability | fail closed | The dossier remains `H1/R3`; no pinpoint H0 audit or independently reviewed R0 reconstruction exists. |
| Hermetic release replay | fail closed | Shared writable warm `.lake` was reused; no empty-cache cold build, offline restore, complete TCB inventory, or SBOM exists. |
| Independent verification | fail closed | The independent implementation used this same worker checkout/cache; no distinct runner, identity, signature, or second attestation exists. |

This is truthful provisional worker evidence only. It grants no `E0/E1`, accepted `M0-*`,
`AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit. `audit_complete=false` and
`theorem_complete=false`.
