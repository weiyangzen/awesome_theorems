# THM-M-1515 release decision handoff

## Exact verdict

`S56-M-1515-RELEASE` is `blocked`. Lifecycle remains `planned`, the accepted
root vector remains `[H1, M3, R3]`, and both `audit_complete` and
`theorem_complete` are false. There are no accepted receipt IDs and no
theorem-completion promotion.

The first failed gate is dependency acceptance. `S56-M-1515-VALIDATION` is
worker-self-tested evidence pending master acceptance, not an accepted
prerequisite. The next gate fails closed because provisional exact-root kernel
evidence conflicts with the authoritative typed graph, which still records an
open `M3` root and two open analytic packages. The weaker state controls.

## Reconciliation

The exact target, analytic proof packages, checked root composition, and direct
exact-type probe elaborate against pinned Lean 4.29.0/mathlib. Observed axioms
are `propext`, `Classical.choice`, and `Quot.sound`, and the scoped placeholder
scan passes. This is useful provisional machine evidence, but it used this
mutable clone and a shared warm dependency cache.

Human-source status remains H1 without accepted edition/page/errata and node
crosswalk review. Readability remains R3 without independently accepted R0.
Release evidence is absent for a clean immutable snapshot, cold empty-cache
network-denied build, offline restoration, complete TCB, SBOM/licenses,
protected CI, two independently provisioned signed runners, an independently
implemented minimal verifier, and a deterministic evidence bundle.

## Self-test recipe

Run from repository root:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1515
python3 Stage1_Instances/THM-M-1515/check_validation.py
python3 Stage1_Instances/THM-M-1515/check_release.py
python3 -m json.tool Stage1_Instances/THM-M-1515/release-decision.json
git diff --check -- Stage1_Instances/THM-M-1515 .stage1-worker-selftest.json
```

No dependency update, build, fetch, clone, or `.lake` mutation is part of this
recipe. It self-tests the negative release reconciliation only; master
acceptance and every remaining release gate stay open.
