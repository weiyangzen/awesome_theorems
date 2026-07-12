# THM-M-1527 release decision handoff

## Exact verdict

`S56-M-1527-RELEASE` is `blocked`. Lifecycle remains `planned`, the accepted root vector remains
`[H2, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is dependency acceptance. `S56-M-1527-VALIDATION` is worker-self-tested
evidence pending master acceptance, not an accepted prerequisite. The next gate also fails closed:
the proof's provisional exact-target result conflicts with the authoritative typed graph, which
still records `root_closed=false` and `M3`. Under rev-5.6 the weaker authoritative state controls.

## Reconciliation

The frozen conditional proposition and a separately written direct proof both elaborate against
pinned Lean 4.29.0 and mathlib `8a178386`, with observed axioms `propext`, `Classical.choice`, and
`Quot.sound`. The proof projects the homogeneous and inhomogeneous equivalences from the explicit
`CoordinateDecomposition` premise and recombines conjunctions. It does not construct or prove that
geometric 3+1 decomposition, so this evidence must not be broadened into an unconditional formal
derivation of Maxwell's equations.

Human-source status remains `H2`: no accepted primary-source theorem/page, convention, assumption,
errata, and node crosswalk has independent review. Readability remains `R3`, without independently
accepted `R0`. Release evidence is absent for a clean immutable snapshot, cold empty-cache
network-denied build, offline restoration, complete TCB, SBOM/licenses, protected CI, two separately
provisioned signed runners, an independently implemented minimal verifier, and a deterministic
content-addressed bundle.

## Self-test

Commands run from base revision `446447c65190dc818b074bf543171f807e9b4651` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1527
  exit 0: rank 195; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-1527/check_validation.py
  exit 0: exact conditional proof and direct probe replayed; graph remains open; release gates blocked

python3 Stage1_Instances/THM-M-1527/check_release.py
  exit 0: blocked decision, unaccepted dependency, unchanged H2/M3/R3 root, and release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-1527/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1527 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No dependency update, build, fetch, clone, or `.lake` mutation was performed. This self-tests the
negative release reconciliation only. Retry requires master dependency acceptance and graph
reconciliation, accepted H0/R0 and trust evidence, then a separately provisioned hermetic and
independent release run.
