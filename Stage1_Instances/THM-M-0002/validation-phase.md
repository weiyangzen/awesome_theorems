# THM-M-0002 validation-phase result

Item `S56-M-0002-VALIDATION` was run against the proof-phase snapshot. The exact frozen statement,
obligation composition module, local proof, and an independently implemented exact-root probe all
elaborate against pinned Lean 4.29.0 and mathlib `8a178386`. The local proof exposes both four-lemma
branches; the independent probe instead invokes mathlib's pinned five-lemma declaration.

## Commands and exact results

Commands ran from base revision `8471ab39f7e977656a7b5ba569063e635a17d5d5` on 2026-07-12
(receipt timestamp `2026-07-11T23:15:56Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0002
  exit 0: execution rank 97; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0002/check_validation.py
  exit 0: fresh temporary Statement/ObligationTree/Proof/Validation elaboration passed;
  exact-root independent reconstruction passed; hashes, placeholder scan, registry denominator,
  mathlib pin, and mathlib cleanliness passed; observed axioms were propext,
  Classical.choice, and Quot.sound
```

The validator invokes only narrow `lake env lean` elaborations. It copies the four modules into a
fresh temporary directory under `Formalizations/Lean`, writes temporary `.olean` files only there,
and removes that directory. No update, build, clone, fetch, or dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, composition, local proof, and independent probe elaborate. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs in checked code. |
| Axiom observation | provisional pass | Checked declarations report only `propext`, `Classical.choice`, and `Quot.sound`; no release TCB acceptance is inferred. |
| Local provenance | pass | Proof receipt input hashes agree; mathlib is clean at the manifest pin; the inspected four-lemma source hash agrees with the anchor audit. |
| Same-clone independent reconstruction | pass with boundary | `Validation.lean` reaches the exact target through the pinned five-lemma body without reusing `Proof.fiveLemma`. This is not a distinct runner. |
| Authoritative structured state | fail closed | The frozen graph predates the proof receipt and still reports `M0002-B-MONO` and `M0002-B-EPI` open. Workers cannot reconcile master state. |
| Hermetic release replay | fail closed | Shared writable warm `.lake` artifacts were reused; no clean checkout, empty-cache build, offline restoration, complete TCB/SBOM, or deterministic release bundle exists. |
| Independent verification | fail closed | No distinct verifier identity, independently provisioned runner, second signature, or protected independent result exists. |

This is truthful provisional worker validation, not theorem completion. `audit_complete=false` and
`theorem_complete=false`; H0/R0 review, state reconciliation, hermetic release, distinct-runner
verification, release, and master acceptance remain open.
