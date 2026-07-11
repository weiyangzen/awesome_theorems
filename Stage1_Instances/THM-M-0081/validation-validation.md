# THM-M-0081 validation-phase handoff

Validation ran from base revision `03523e6728e323f2844994a3e6a20ac7c269c6eb`. The pinned Lean
4.29.0 kernel elaborated the exact canonical statement, the primary proof, and a separately written
exact-root reconstruction in `Validation.lean`. The reconstruction does not import `Proof.lean` and
uses `Yoneda.fullyFaithful.isoEquiv`, rather than repeating the primary module's separate
`preimageIso` and `mapIso` proof. Every proof declaration reported only `propext`,
`Classical.choice`, and `Quot.sound`.

The fail-closed verifier checks proof-receipt freshness, the frozen 11-obligation denominator and
typed-graph identity, exact root scope, absence of prohibited constructs, the pinned mathlib
manifest and checkout revision, and cleanliness of the mathlib dependency. Source and `.olean`
hashes for the terminal Yoneda and fully-faithful modules are recorded in
`validation-receipt.json`.

This is real kernel, provenance, trust-boundary, and local independent-reconstruction evidence, but
it is not release-grade hermetic or independent verification. It reused the canonical warm `.lake`
cache in this checkout. There is no empty-cache network-denied replay, separately provisioned signed
runner, H0/R0 acceptance, complete transitive TCB closure, supply-chain archive, deterministic
release bundle, or master acceptance. Accordingly `theorem_complete` remains false; the first
failed release gate is the hermetic cold-build gate.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0081
  exit 0: rank 138, planned, theorem_complete=false

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0081/CanonicalStatement.lean &&
  lake env lean ../../Stage1_Instances/THM-M-0081/Proof.lean &&
  lake env lean ../../Stage1_Instances/THM-M-0081/Validation.lean
  exit 0: exact statement and both exact-root implementations elaborated;
  #print axioms reported propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0081/check_validation.py
  exit 0: 11-node identity, proof freshness, pinned clean mathlib, exact-root independent
  reconstruction, trust boundary, and hygiene verified

python3 Stage1_Instances/THM-M-0081/check_obligation_tree.py
  exit 0: frozen 11-obligation, 21-edge pre-proof architecture and denominator passed

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0081 --glob '*.lean'
  exit 1 with empty output: pass, no prohibited source token

git diff --check -- Stage1_Instances/THM-M-0081
  exit 0: no whitespace errors
```

No update, build, clone, fetch, network access, or mutation of `.lake` was performed.
