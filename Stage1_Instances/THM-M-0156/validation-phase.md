# THM-M-0156 validation-phase result

Item `S56-M-0156-VALIDATION` was run against the proof-phase snapshot. The exact
frozen rectangular target, conditional composition harness, canonical proof,
and a separately implemented local reconstruction elaborate against pinned
Lean 4.29.0 and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Lean reports exactly `propext`,
`Classical.choice`, and `Quot.sound` for the root declarations. The checked
local sources contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe`
declaration.

## Exact command and result

The structured recipe ran from repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0156/check_validation.py
  exit 0
  ok: exact proof and independently reconstructed root elaborated in a fresh temporary module directory
  ok: root declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, proof-receipt hashes, frozen denominator, and clean pinned mathlib checks passed
  stale: frozen graph predates proof closure and still reports root_closed=false
  blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner independent verification
```

The validator copies `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` into a fresh temporary module directory under
`Formalizations/Lean`, invokes only narrow `lake env lean` checks, and removes
the directory and generated `.olean` files. The pinned mathlib checkout was
clean and its divergence source hash matched the receipt. No update, build,
clone, fetch, network access, or dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact composition, proof, and local independent reconstruction elaborate. |
| Placeholder and unsafe scan | pass | No prohibited declaration or proof escape in the four local Lean modules. |
| Axiom observation | provisional pass | Root declarations report the allowed classical mathlib set only. |
| Local provenance | pass | Proof hashes, frozen denominator, mathlib revision, clean dependency tree, and source hash agree. |
| Root kernel closure | provisional pass | Canonical and independently reconstructed declarations inhabit the exact frozen target. |
| Structured-state freshness | fail closed | `typed-graphs.json` predates proof closure and still records `root_closed=false`. |
| Hermetic release replay | fail closed | Shared warm `.lake` is not empty-cache cold/offline replay and has no complete TCB/SBOM/license packet. |
| Independent verification | fail closed | The diverse probe used this checkout/cache; no distinct signed runner or second attestation exists. |

The first failed validation gate is structured-state freshness. This is
truthful provisional worker evidence only. It grants no accepted `M0-*`,
`AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
`audit_complete=false` and `theorem_complete=false`.
