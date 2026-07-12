# THM-M-0986 validation-phase handoff

Item `S56-M-0986-VALIDATION` was validated from base revision
`e5e8ddc710ab4ddd81a74aa5045c846238ce9562` on `2026-07-12`.

The pinned Lean 4.29.0 kernel elaborated the exact statement and primary proof
in a temporary module directory. It also elaborated a separately written exact-root
reconstruction in `Validation.lean`. That probe imports only `Statement.lean`, not
`Proof.lean` or `ObligationTree.lean`, and directly applies the pinned
`ProbabilityTheory.strong_law_ae` and AE-to-in-measure bridge. Both routes report
only `propext`, `Classical.choice`, and `Quot.sound`.

`check_validation.py` fails closed on stale proof inputs, registry/typed-graph
identity drift, the frozen denominator, target drift, prohibited Lean constructs,
an accidental primary-proof import, the mathlib manifest/checkout revision, or a
dirty mathlib dependency. Source and `.olean` hashes for the terminal strong-law
module are recorded in `validation-receipt.json`.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0986
  exit 0: rank 266, planned, theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0986/check_proof.sh
  exit 0: Statement, ObligationTree, and Proof elaborated in a temporary
  directory; root and package axiom lists are propext, Classical.choice,
  and Quot.sound

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0986/check_validation.sh
  exit 0: Statement and the independent exact-root reconstruction elaborated
  in a separate temporary directory; axiom list is propext,
  Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0986/check_statement.py
  exit 0: four structural mutations killed; exact expression fingerprint passed

python3 Stage1_Instances/THM-M-0986/check_proof.py
  exit 0: exact root and both frozen proof packages have bodies

python3 Stage1_Instances/THM-M-0986/check_obligation_tree.py
  exit 0: frozen 11-obligation, 20-edge architecture passed; its pre-proof
  M3 observation remains unchanged

python3 Stage1_Instances/THM-M-0986/check_validation.py
  exit 0: proof freshness, frozen identity, pinned clean mathlib, independent
  reconstruction, trust boundary, and hygiene passed

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0986 --glob '*.lean'
  exit 1 with empty output: pass, no prohibited source token

git diff --check -- Stage1_Instances/THM-M-0986 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No Lake update/build, fetch, clone, network access, or `.lake` mutation occurred.
This is real local kernel, trust-boundary, provenance, and independent-reconstruction
evidence, but not release-grade hermetic or independent-runner evidence. It reused
the canonical warm `.lake` cache in this worker clone. The first failed release gate
is the cold empty-cache hermetic replay; source/readability acceptance and master
acceptance also remain open. Therefore `theorem_complete` remains false.
