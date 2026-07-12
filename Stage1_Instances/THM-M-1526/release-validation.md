# THM-M-1526 release decision handoff

## Exact verdict

`S56-M-1526-RELEASE` is `blocked`. Lifecycle remains `planned`, the accepted root vector remains
`[H2, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is dependency acceptance. `S56-M-1526-VALIDATION` is worker-self-tested
evidence pending master acceptance, not an accepted prerequisite. The next gate also fails closed:
the proof's provisional exact-target result conflicts with the authoritative typed graph, which
still records `M3` and the cut set `M1526-N-PRODUCT`, `M1526-L-SLASH-SQUARE`. The weaker structured
state controls.

## Reconciliation

The frozen conditional algebraic proposition and a separately written direct proof elaborate
against pinned Lean 4.29.0 and mathlib `8a178386`, with observed axioms `propext`,
`Classical.choice`, and `Quot.sound`. This proves the exact finite constant-coefficient operator
target from its explicit Clifford and commutation fields. It does not supply a concrete analytic
spinor model, unbounded differential-operator domains, regularity, self-adjointness, or historical
source fidelity, so it must not be broadened into a full analytic Dirac-equation formalization.

Human-source status remains `H2`: no accepted primary-source equation/page, conventions,
assumptions, errata, and node crosswalk has independent review. Readability remains `R3`, without
independently accepted `R0`. Release evidence is absent for a clean immutable snapshot, cold
empty-cache network-denied build, offline restoration, complete TCB, SBOM/licenses, protected CI,
two separately provisioned signed runners, an independently implemented minimal verifier, and a
deterministic content-addressed bundle.

## Self-test

Commands run from base revision `cb017427b2aed4af4881826839e21a102a224cbf` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1526
python3 Stage1_Instances/THM-M-1526/check_validation.py
python3 Stage1_Instances/THM-M-1526/check_release.py
python3 -m json.tool Stage1_Instances/THM-M-1526/release-decision.json
git diff --check -- Stage1_Instances/THM-M-1526 .stage1-worker-selftest.json
```

Exact exit codes and output summaries are recorded in `.stage1-worker-selftest.json`. No dependency
update, build, fetch, clone, or `.lake` mutation was performed. This self-tests the negative release
reconciliation only; retry requires master dependency acceptance and graph reconciliation,
accepted H0/R0 and trust evidence, then a separately provisioned hermetic and independent release
run.
