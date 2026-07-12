# THM-M-0646 validation-phase result

Item: `S56-M-0646-VALIDATION`. Base revision:
`734cdf53ab1cc41c766d2a40058a1929f6e1311a`.

The exact local Loewenheim-Skolem root and a separately written direct probe both elaborate against
the pinned mathlib terminal declaration. Both report exactly `propext`, `Classical.choice`, and
`Quot.sound`. The verifier confirms proof-receipt freshness, registry/graph identity, a clean
mathlib source checkout at the manifest revision, local hygiene, and source/olean provenance.

## Commands and results

All commands ran on 2026-07-12 in this worker clone. Existing pinned `.lake` artifacts were reused;
no update, build, clone, fetch, or dependency mutation was performed.

```text
bash Stage1_Instances/THM-M-0646/check_proof.sh
  exit 0: exact root, statement adapter, and seven terminal declarations elaborated;
  all nine axiom reports were [propext, Classical.choice, Quot.sound]

cd Formalizations/Lean
lake env lean ../../Stage1_Instances/THM-M-0646/Validation.lean
  exit 0: independently reconstructed root elaborated directly from the pinned terminal;
  terminal and independent root reported [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0646/check_validation.py
  exit 0: fresh proof receipt, graph identity, clean pin, provenance, and hygiene;
  both source hashes and both olean hashes matched the proof receipt

python3 Stage1_Instances/THM-M-0646/check_obligation_tree.py
  exit 0: 13 obligations, 36 typed edges, denominator valid; frozen root remains open

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0646
  exit 0: rank 692, planned, theorem_complete=false
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact proof wrapper and direct validation probe elaborate under pinned Lean/mathlib. |
| Placeholder/unsafe scan | pass | No forbidden local construct occurs on the checked surface. |
| Trust observation | provisional pass | Both routes report only the three recorded axioms; full release TCB closure is absent. |
| Provenance and freshness | pass | Proof hashes agree; mathlib source is clean/pinned; source and olean hashes agree. |
| Authoritative graph reconciliation | master-only | The frozen graph predates proof acceptance and still records the root open. |
| Hermetic release replay | fail closed | Shared warm artifacts were reused; no cold empty-cache offline replay or SBOM/license closure occurred. |
| Independent verification | fail closed | The separate probe ran in this clone/cache, not on a distinct signed runner. |

This is provisional validation-phase evidence, not release evidence. `audit_complete=false` and
`theorem_complete=false`; source/H0, R0, release assurance, and master acceptance remain open.
